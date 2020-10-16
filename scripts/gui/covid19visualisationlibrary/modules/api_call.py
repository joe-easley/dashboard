from requests import get
from json import dumps


class APICaller:

    def set_params(self, area_type, area_name, data_type, data_requested, frequency):
        """

        :param frequency: str
        :param data_requested: str
        :param data_type: str
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
        endpoint = "https://api.coronavirus.data.gov.uk/v1/data"

        response = get(endpoint, params=api_params, timeout=10)

        if response.status_code >= 400:
            raise RuntimeError(f'Request failed: { response.text }')

        if response.status_code >= 204:
            raise RuntimeError("Request failed: The request was successfully processed, but there were no records "
                               "matching the requested criteria. }")

        return response

    def api_runner(self, params):

        area_type = params["area_type"]
        area_name = params["area_name"]
        duration = params["duration"]
        data_type = params["data_type"]
        data_requested = params["data_requested"]
        frequency = params["frequency"]

        api_params = self.set_params(area_type, area_name, data_type, data_requested, frequency)

        api_response = self.make_api_call(api_params)

        return api_response
