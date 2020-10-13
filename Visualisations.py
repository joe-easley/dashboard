from requests import get
from json import dumps
from pandas import DataFrame
import matplotlib.pyplot as pyplot
import optparse


class APICaller:

    def set_params(self, area_type, area_name, data_type, data_requested, frequency):
        """

        :param area_type: str
        :param area_name: str
        :return: api_params: str
        """

        filters = [
            f"areaType={area_type}",
            f"areaName={area_name}"
        ]

        structure = {
            "date": "date",
            "name": "areaName",
            "code": "areaCode",
            data_requested: {
                frequency: data_type
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

        if response.status_code >= 204:
            raise RuntimeError("Request failed: The request was successfully processed, but there were no records matching the requested criteria. }")

        return response

    def filter_data(self, response, data_requested, frequency):
        """

        :param response: json
        :return: date_and_cases: list
        """

        data = response.json()

        all_data = data["data"]
        print(all_data)
        date_and_cases = []

        for day in all_data:
            date = day.get("date")
            cases = day.get(data_requested)
            daily_cases = cases.get(frequency)
            if daily_cases is None:
                daily_cases = 0
            elif type(daily_cases) is int:
                date_and_cases.append([date, daily_cases])
            else:
                print(f"Number data type is {type(daily_cases)}")

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

        else:
            try:
                duration_as_int = int(duration)
                df = DataFrame(date_and_cases[:duration_as_int], columns=["Date", "CasesBySpecimenDate"])
                return df
            except:
                print("Date could not be consumed, check value is int")
                exit()


    def calculate_moving_average(self, dataframe):
        """

        :param dataframe: dataframe obj
        :return: dataframe obj
        """
        dataframe['rollingaverage'] = dataframe.CasesBySpecimenDate.rolling(14, min_periods=1).mean()

        print(dataframe.head())

        return dataframe

    def plot_data(self, df, area_name, data_requested):
        """

        :param area_name: str
        :param df: dataframe obj
        :return: graphical plot
        """
        pyplot.plot("Date", "CasesBySpecimenDate", data=df)
        pyplot.plot("Date", "rollingaverage", data=df)
        pyplot.xticks(fontsize=14)
        pyplot.yticks(fontsize=14)
        pyplot.legend(labels=[f'Daily {data_requested.capitalize()}', '7 day moving average'], fontsize=14)

        # title and labels

        pyplot.title(f'Number of {data_requested} by date in {area_name.capitalize()}', fontsize=20)
        pyplot.xlabel('Date', fontsize=16)
        pyplot.ylabel(f'Number of {data_requested}', fontsize=16)

        pyplot.show()

    def runner(self, params):
        """

        :param params: dict
        :return:
        """

        area_type = params["area_type"]
        area_name = params["area_name"]
        duration = params["duration"]
        data_type = params["data_type"]

        death_data_types = ["newDeaths28DaysByDeathDate", "cumDeaths28DaysByDeathDate",
                            "cumDeaths28DaysByDeathDateRate"]
        cases_data_types = ["newCasesBySpecimenDate", "cumCasesBySpecimenDateRate", "newPillarOneTestsByPublishDate",
                            "newPillarTwoTestsByPublishDate", "newPillarTwoTestsByPublishDate",
                            "newPillarFourTestsByPublishDate"]

        if data_type in cases_data_types:
            data_requested = "cases"

        elif data_type in death_data_types:
            data_requested = "deaths"

        else:
            print(f"Data type ({data_type}) not supported")
            exit()

        if data_type.startswith("new") is True:
            frequency = "daily"

        elif data_type.startswith("cum") is True:
            frequency = "cumulative"

        else:
            print("cannot determine requested frequency")
            exit()

        api_params = self.set_params(area_type, area_name, data_type, data_requested, frequency)

        api_response = self.make_api_call(api_params)

        filtered_response = self.filter_data(api_response, data_requested, frequency)

        dataframe = self.build_dataframe(filtered_response, duration)

        complete_dataframe = self.calculate_moving_average(dataframe)

        self.plot_data(complete_dataframe, area_name, data_requested)


if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option("--dataType", dest="data_type", default=" ", help="See readme for different options")
    parser.add_option("--areaType", dest="area_type", default=" ", help="Options are: nation, utla, ltla")
    parser.add_option("--areaName", dest="area_name", default=" ", help="Name of area, must be lower case, eg england")
    parser.add_option("--duration", dest="duration", default=" ", help="Options are: allTime, month, fortnight or week")

    options, args = parser.parse_args()

    params = {"data_type": options.data_type,
              "area_type": options.area_type,
              "area_name": options.area_name,
              "duration": options.duration}

    run_script = APICaller()

    run_script.runner(params)
