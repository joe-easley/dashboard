from requests import get
from json import dumps
from pandas import DataFrame
import matplotlib.pyplot as pyplot
import optparse


class APICaller:

    def set_params(self, area_type, area_name):
        """

        :param area_type: str
        :param area_name: str
        :return: api_params: str
        """

        filters = [
            f"areaType={ area_type }",
            f"areaName={ area_name }"
        ]

        structure = {
            "date": "date",
            "name": "areaName",
            "code": "areaCode",
            "cases": {
                "daily": "newCasesBySpecimenDate"
            },
            "deaths": {
                "daily": "newDeathsByDeathDate",
                "cumulative": "cumDeathsByDeathDate"
            }
        }

        api_params = {
            "filters": str.join(";", filters),
            "structure": dumps(structure, separators=(",", ":"))
        }

        return api_params

    def make_api_call(self, api_params):
        """

        :param api_params:
        :return: response: json
        """
        ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"

        response = get(ENDPOINT, params=api_params, timeout=10)

        if response.status_code >= 400:
            raise RuntimeError(f'Request failed: { response.text }')

        return response

    def filter_data(self, response):
        """

        :param response: json
        :return: date_and_cases: list
        """

        data = response.json()

        all_data = data["data"]

        date_and_cases = []

        for day in all_data:
            date = day.get("date")
            cases = day.get("cases")
            daily_cases = cases.get("daily")
            date_and_cases.append([date, daily_cases])

        date_and_cases.reverse()

        return date_and_cases

    def build_dataframe(self, date_and_cases, duration):
        """

        :param date_and_cases: str
        :param duration: str
        :return: df: dataframe obj
        """
        if duration == "allTime":

            df = DataFrame(date_and_cases, columns=["Date", "CasesBySpecimenDate"])
            return df

        elif duration == "month":
            df = DataFrame(date_and_cases[:28], columns=["Date", "CasesBySpecimenDate"])
            return df

        elif duration == "fortnight":
            df = DataFrame(date_and_cases[:14], columns=["Date", "CasesBySpecimenDate"])
            return df

        elif duration == "week":
            df = DataFrame(date_and_cases[:7], columns=["Date", "CasesBySpecimenDate"])
            return df

    def calculate_moving_average(self, dataframe):
        """

        :param dataframe: dataframe obj
        :return: dataframe obj
        """
        dataframe['rollingaverage'] = dataframe.CasesBySpecimenDate.rolling(14, min_periods=1).mean()

        print(dataframe.head())

        return dataframe

    def plot_data(self, df, area_name):
        """

        :param area_name: str
        :param df: dataframe obj
        :return: graphical plot
        """
        df.plot()
        pyplot.xticks(fontsize=14)
        pyplot.yticks(fontsize=14)
        pyplot.legend(labels=['Daily Cases', '7 day moving average'], fontsize=14)

        # title and labels
        pyplot.title(f'The number of cases by specimen date in {area_name.capitalize()}', fontsize=20)
        pyplot.xlabel('Date', fontsize=16)
        pyplot.ylabel('Number of cases', fontsize=16)

        pyplot.show()

    def runner(self, params):
        """

        :param params: dict
        :return:
        """

        area_type = params["area_type"]
        area_name = params["area_name"]
        duration = params["duration"]

        api_params = self.set_params(area_type, area_name)

        api_response = self.make_api_call(api_params)

        filtered_response = self.filter_data(api_response)

        dataframe = self.build_dataframe(filtered_response, duration)

        complete_dataframe = self.calculate_moving_average(dataframe)

        self.plot_data(complete_dataframe, area_name)


if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option("--areaType", dest="area_type", default=" ", help="Options are: nation, utla, ltla")
    parser.add_option("--areaName", dest="area_name", default=" ", help="Name of area, must be lower case, eg england")
    parser.add_option("--duration", dest="duration", default=" ", help="Options are: allTime, month, fortnight or week")

    options, args = parser.parse_args()

    params = {"area_type": options.area_type,
              "area_name": options.area_name,
              "duration": options.duration}

    run_script = APICaller()

    run_script.runner(params)
