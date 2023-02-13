import json
from json import JSONDecodeError


class SettingsReader:

    def __init__(self, path_of_settings_json: str):
        self.settings_path = path_of_settings_json

    def read_settings(self):
        try:
            with open(self.settings_path, 'r') as settings:
                return json.load(settings)
        except OSError as os_error:
            print('Unable to open configuration file: ' + self.settings_path + '\n' + str(os_error))
        except JSONDecodeError as json_error:
            print('Invalid json string in configuration file: ' + self.settings_path + '\n' + str(json_error))
