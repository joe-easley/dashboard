from pandas import DataFrame
import matplotlib.pyplot as pyplot


class PlotData:

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
            df = DataFrame(date_and_cases[-28:], columns=["Date", "CasesBySpecimenDate"])
            return df

        elif duration == "fortnight":
            df = DataFrame(date_and_cases[-14:], columns=["Date", "CasesBySpecimenDate"])
            return df

        elif duration == "week":
            df = DataFrame(date_and_cases[-7:], columns=["Date", "CasesBySpecimenDate"])
            return df

        else:
            try:
                duration_as_int = int(duration)
                df = DataFrame(date_and_cases[-duration_as_int:], columns=["Date", "CasesBySpecimenDate"])
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

        pyplot.show(block=False)
        pyplot.figure()

    def runner(self, api_response, data_requested, frequency, duration, area_name):
        """

        :param params: dict
        :return:
        """

        filtered_response = self.filter_data(api_response, data_requested, frequency)

        dataframe = self.build_dataframe(filtered_response, duration)

        complete_dataframe = self.calculate_moving_average(dataframe)

        self.plot_data(complete_dataframe, area_name, data_requested)