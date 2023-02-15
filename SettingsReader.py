import json
import logging
from json import JSONDecodeError


class SettingsReader:

    def __init__(self, path_of_settings_json: str):
        self.settings_path = path_of_settings_json

    def read_settings(self):
        try:
            with open(self.settings_path, 'r') as settings:
                logging.debug('Configuration file ' + self.settings_path + ' opened successfully.')
                dict_of_conf_values = json.load(settings)
                logging.debug('Configuration loaded successfully: ' + str(dict_of_conf_values))
                return dict_of_conf_values
        except OSError as os_error:
            logging.critical('Unable to open configuration file: ' + self.settings_path + '\n' + str(os_error))
        except JSONDecodeError as json_error:
            logging.critical('Invalid json string in configuration file: ' + self.settings_path + '\n'
                             + str(json_error))
