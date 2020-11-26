class CovidDataRunner:

    def __init__(self):

        self.params = {}

        self.api_response = object

    def runner(self):
        """

        :return:
        """

        from .modules import GUI
        from .modules import APICaller
        from .modules import PlotData

        loop = True

        while loop is True:

            self.params = GUI().gui_runner()

            self.create_more_params()

            self.api_response = APICaller().api_runner(self.params)

            PlotData().runner(self.api_response, self.params["data_requested"], self.params["frequency"],
                              self.params["duration"], self.params["area_name"])

            loop = GUI().gui_check_if_more_data_required()

        exit()

    def create_more_params(self):

        death_data_types = ["newDeaths28DaysByDeathDate", "cumDeaths28DaysByDeathDate",
                            "cumDeaths28DaysByDeathDateRate"]
        cases_data_types = ["newCasesBySpecimenDate", "cumCasesBySpecimenDateRate", "newPillarOneTestsByPublishDate",
                            "newPillarTwoTestsByPublishDate", "newPillarTwoTestsByPublishDate",
                            "newPillarFourTestsByPublishDate"]

        if self.params.get("data_type") in cases_data_types:
            self.params["data_requested"] = "cases"

        elif self.params.get("data_type") in death_data_types:
            self.params["data_requested"] = "deaths"

        else:
            print(f"Data type ({self.params.get('data_type')}) not supported")
            exit()

        if self.params.get('data_type').startswith("new") is True:
            self.params["frequency"] = "daily"

        elif self.params.get('data_type').startswith("cum") is True:
            self.params["frequency"] = "cumulative"

        else:
            print("Cannot determine requested frequency")
            exit()

        return self.params
