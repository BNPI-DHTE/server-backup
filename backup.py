from BackupCreator import BackupCreator
from SettingsReader import SettingsReader
import sys

# TODO: Error handling
# TODO: Logging
# TODO: Docker image
# TODO: Tests

settings_reader = SettingsReader(sys.argv[1])
list_of_settings = settings_reader.read_settings()


def set_archive_type(options: dict):
    archive_type = 'bz2'
    if 'archive_type' in options:
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
