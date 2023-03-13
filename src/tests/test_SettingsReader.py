import os

import pytest

from src.core.SettingsReader import SettingsReader

path = os.path.dirname(__file__)


def test_read_settings():
    settings_reader = SettingsReader(os.path.join(path, 'test_correct_settings.json'))
    settings = settings_reader.read_settings()
    assert settings[0].__len__() == 6
    assert settings[0]['backup_folder'] == 'backup/'


def test_wrong_json_causes_system_exit():
    reader = SettingsReader(os.path.join(path, 'fixtures/invalid_json_settings.json'))
    with pytest.raises(SystemExit) as system_exit:
        reader.read_settings()
    assert system_exit.type == SystemExit
    assert str(system_exit.value) == \
           ('Invalid json string in configuration file: ' + os.path.join(path, 'fixtures/invalid_json_settings.json')
            + '\nExpecting \',\' delimiter: line 4 column 5 (char 36)')


def test_wrong_settings_path_causes_system_exit():
    reader = SettingsReader('.file_does_not_exists.json')
    with pytest.raises(SystemExit) as system_exit:
        reader.read_settings()
    assert system_exit.type == SystemExit
    assert (str(system_exit.value)) == '[Errno 2] No such file or directory: \'.file_does_not_exists.json\''
