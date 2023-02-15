import logging
import sys

from ArchiveTypes import ArchiveTypes
from BackupCreator import BackupCreator
from SettingsReader import SettingsReader


# TODO: Tests
# TODO: Docker image


def main():
    logging.basicConfig(format='%(asctime)s:(%(levelname)s) %(message)s',
                        filename='backup_log.log',
                        encoding='utf-8',
                        level=logging.INFO)
    logging.debug("Starting backup.")
    dict_of_settings = define_configuration()
    do_backup(dict_of_settings)
    logging.debug("Backup finished.")


def do_backup(dict_of_settings: dict):
    for settings in dict_of_settings:
        try:
            print('Backup type \'' + str(settings['backup_type']) + '\' started.')
            logging.info('Backup type: ' + str(settings['backup_type']))
            backup = BackupCreator(settings['backup_type'],
                                   settings['root_folder'],
                                   settings['data_folder'],
                                   settings['backup_folder'],
                                   archive_type=set_archive_type(settings),
                                   extensions=set_extensions(settings))
            backup.make_tarfile()
            print('Backup type \'' + str(settings['backup_type']) + '\' finished.')
        except IndexError as index_error:
            logging.critical('Necessary option missing from configuration file!\n' + str(index_error))
            # A validation of configuration file should be useful.


def define_configuration():
    list_of_settings = ()
    try:
        settings_reader = SettingsReader(sys.argv[1])
        logging.debug('Configuration file ' + sys.argv[1] + ' from CLI argument read successfully.')
        list_of_settings = settings_reader.read_settings()
    except IndexError as index_error:
        logging.critical('You have to enter a configuration json file as argument in command line! '
                         'Read the documentation for more info!\n' + str(index_error))
    return list_of_settings


def is_valid_archive_type(type_string: str):
    archive_types = [member.value for member in ArchiveTypes]
    if archive_types.__contains__(type_string):
        return True
    logging.warning('Invalid archive type: ' + type_string + '. The default value ("bz2") will be used!')
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


if __name__ == '__main__':
    main()
