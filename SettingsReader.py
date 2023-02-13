import json


class SettingsReader:

    def __init__(self, path_of_settings_json: str):
        self.settings_path = path_of_settings_json

    def read_settings(self):
        try:
            with open(self.settings_path, 'r') as settings:
                return json.load(settings)
        except OSError as error:
            print('Unable to open configuration file: ' + self.settings_path + '\n' + str(error))
