from BackupCreator import BackupCreator
from SettingsReader import SettingsReader
import sys
from ArchiveTypes import ArchiveTypes

# TODO: Logging
# TODO: Docker image
# TODO: Tests

list_of_settings = {}
try:
    settings_reader = SettingsReader(sys.argv[1])
    list_of_settings = settings_reader.read_settings()
except IndexError as index_error:
    print('You have to enter a configuration json file as argument in command line! '
          'Read the documentation for more info!')


def is_valid_archive_type(type_string: str):
    archive_types = [member.value for member in ArchiveTypes]
    if archive_types.__contains__(type_string):
        return True
    print('Warning! Invalid archive type: ' + type_string + '.\nThe default value ("bz2") will be used!')
    return False


def set_archive_type(options: dict):
    archive_type = 'bz2'
    if ('archive_type' in options) & (is_valid_archive_type(options['archive_type'])):
        archive_type = options['archive_type']
    return archive_type


def set_extensions(options: dict):
    extensions = ['*']
    if 'extensions' in options:
        extensions = options['extensions']
    return extensions


for settings in list_of_settings:
    backup = BackupCreator(settings['backup_type'],
                           settings['root_folder'],
                           settings['data_folder'],
                           settings['backup_folder'],
                           archive_type=set_archive_type(settings),
                           extensions=set_extensions(settings))

    backup.make_tarfile()
