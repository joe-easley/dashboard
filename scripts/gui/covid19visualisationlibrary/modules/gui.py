import PySimpleGUI as sg


class GUI:

    def gui_greeeting(self):
        """

        :return:
        """
        layout = [[sg.Text("Do you wish to search for case or death data?")],
                  [sg.Listbox(enable_events=True, values=["cases", 'deaths'], size=(30, 6))]]
        window = sg.Window('Covid19 Data Analyser', layout)
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                # User closed the Window or hit the Cancel button
                break

            data_searched = values.get(0)
            window.close()

        return data_searched

    def gui_cases_or_deaths(self, data_searched):
        """

        :param data_type:
        :return:
        """
        death_data_types = ["newDeaths28DaysByDeathDate", "cumDeaths28DaysByDeathDate",
                            "cumDeaths28DaysByDeathDateRate"]
        cases_data_types = ["newCasesBySpecimenDate", "cumCasesBySpecimenDateRate", "newPillarOneTestsByPublishDate",
                            "newPillarTwoTestsByPublishDate", "newPillarTwoTestsByPublishDate",
                            "newPillarFourTestsByPublishDate"]
        if data_searched == "cases":

            layout = [[sg.Text(f"Please select type of {data_searched} data")],
                      [sg.Listbox(enable_events=True, values=cases_data_types, size=(30, 6))]]

            window = sg.Window('Covid19 Data Analyser', layout)

            while True:

                event, values = window.read()

                if event in (None, 'Cancel'):

                    break

                data_type = values.get(0)

                window.close()

                return data_type[0]

        elif data_searched == "deaths":

            layout = [[sg.Text(f"Please select type of {data_searched} data")],
                      [sg.Listbox(enable_events=True, values=death_data_types, size=(30, 6))]]

            window = sg.Window('Covid19 Data Analyser', layout)

            while True:

                event, values = window.read()

                if event in (None, 'Cancel'):
                    break

                data_type = values.get(0)

                window.close()

                return data_type[0]

    def gui_duration(self):
        """

        :return:
        """

        possible_timeframes = ["fortnight", "month", "allTime", "custom"]
        layout = [[sg.Text(f"Please select time period for data")],
                  [sg.Listbox(enable_events=True, values=possible_timeframes, size=(30, 6))]]

        window = sg.Window('Covid19 Data Analyser', layout)

        while True:

            event, values = window.read()

            if event in (None, 'Cancel'):
                break

            duration = values.get(0)

            window.close()

        preset_times = ["fortnight", "month", "allTime"]
        if duration[0] in preset_times:

            return duration[0]

        elif duration[0] == "custom":

            layout = [[sg.Text(f"Please input desired number of days"), sg.InputText()],
                      [sg.Button('OK'), sg.Button('Cancel')]]

            window = sg.Window('Covid19 Data Analyser', layout)

            while True:

                event, values = window.read()

                if event in (None, 'Cancel'):
                    break
                duration = values.get(0)

                window.close()

            return duration
        print("Failure in setting duration")

    def gui_area_type(self):

        area_type = ["ltla", "utla", "nation", "region"]
        layout = [[sg.Text(f"Please select level: ")],
                  [sg.Listbox(enable_events=True, values=area_type, size=(30, 6))]]

        window = sg.Window('Covid19 Data Analyser', layout)

        while True:

            event, values = window.read()

            if event in (None, 'Cancel'):
                break

            area_type = values.get(0)

            window.close()

            return area_type[0]

    def gui_area_name(self, area_type):

        layout = [[sg.Text(f"Please input desired location name for {area_type}"), sg.InputText()],
                  [sg.Button('OK'), sg.Button('Cancel')]]

        window = sg.Window('Covid19 Data Analyser', layout)

        while True:

            event, values = window.read()

            if event in (None, 'Cancel'):
                break
            area_name = values.get(0)

            window.close()

        return area_name

    def gui_check_if_more_data_required(self):
        layout = [[sg.Text(f"Would you like to access more data?")],
                  [sg.Listbox(enable_events=True, values=["Yes", "No"], size=(30, 6))]]

        window = sg.Window('Covid19 Data Analyser', layout)

        while True:

            event, values = window.read()

            if event in (None, 'Cancel'):
                break

            proceed_or_kill = values.get(0)

            if proceed_or_kill == "Yes":
                window.close()
                return True

            elif proceed_or_kill == "No":
                window.close()
                return False



            window.close()

        return True


    def gui_runner(self):
        """

        :return:
        """

        params = {}

        data_searched = self.gui_greeeting()

        params["data_type"] = self.gui_cases_or_deaths(data_searched[0])

        params["duration"] = self.gui_duration()

        params["area_type"] = self.gui_area_type()

        params["area_name"] = self.gui_area_name(params["area_type"])

        return params