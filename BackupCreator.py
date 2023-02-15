import logging
import tarfile
from datetime import datetime
from glob import glob
from os import mkdir, chdir, walk, path


def create_missing_folder(folder: str):
    try:
        if glob(folder).__len__() == 0:
            mkdir(folder)
            logging.warning('No backup folder with name: ' + folder + '! It has been created successfully.')
    except FileNotFoundError as fnf_error:
        logging.critical('Unable to create missing backup directory: ' + folder + '\n' + str(fnf_error))


class BackupCreator:

    def __init__(self,
                 backup_type: str,
                 root_folder: str,
                 data_relative_path: str,
                 backup_folder: str,
                 extensions=None,
                 archive_type='bz2'):
        if extensions is None:
            extensions = ['*']
        self.backup_type = backup_type
        self.root_folder = root_folder
        self.data_relative_path = data_relative_path
        self.backup_folder = backup_folder
        self.extensions = extensions
        self.archive_type = archive_type

    def make_tarfile(self):
        try:
            chdir(self.root_folder)
            logging.debug('Current working folder is: ' + self.root_folder)
        except OSError as os_error:
            logging.critical('Unable to open folder: ' + self.root_folder + '\n' + str(os_error))
        filename = path.join(self.root_folder, self.backup_folder, self.backup_type, self.generate_archive_filename())
        create_missing_folder(self.backup_folder)
        create_missing_folder(path.join(self.backup_folder, self.backup_type))
        files = self.create_file_list_to_archive()
        logging.debug('Files to archive:\n' + str(files))
        logging.info('Number of files to archive: ' + str(files.__len__()))
        try:
            chdir(path.join(self.root_folder, self.data_relative_path))
            logging.debug('Current working folder is: ' + str(path.join(self.root_folder, self.data_relative_path)))
        except OSError as os_error:
            logging.critical('Unable to open folder: '
                             + path.join(self.root_folder, self.data_relative_path) + '\n' + str(os_error))
        self.write_tarfile(filename, files)
        logging.info('Archive saved successfully: ' + filename)

    def write_tarfile(self, filename: str, files: [str]):
        try:
            with tarfile.open(filename, 'w:' + self.archive_type) as tar:
                for file in files:
                    logging.debug('Add file ' + str(file) + ' to archive ' + str(filename))
                    tar.add(file)
        except OSError as os_error:
            logging.critical('Unable to use tarfile: ' + filename + '\n' + str(os_error))
        except tarfile.TarError as tar_error:
            logging.critical('Unable to compress files to tarfile: ' + filename + '\n' + str(tar_error))

    def generate_archive_filename(self):
        current_time = datetime.now()
        date = current_time.strftime('%Y_%m_%d_%H_%M_%S')
        return self.backup_type + '_backup_' + date + '.tar.' + self.archive_type

    def create_file_list_to_archive(self):
        contents = self.create_list_of_all_files()
        if not self.extensions.__contains__('*'):
            logging.debug('Filtering files with extensions: ' + str(self.extensions))
            return self.filter_file_list(contents)
        logging.debug('Does not has an effective extension filter, archive all files in data folder.')
        return contents

    def create_list_of_all_files(self):
        data_folder = path.join(self.root_folder, self.data_relative_path)
        contents = []
        try:
            for dir_path, dirs, files in walk(data_folder):
                dir_relative_path = dir_path.replace(data_folder, '')
                for file in files:
                    if dir_relative_path:
                        contents.append(path.join(dir_relative_path, file))
                    else:
                        contents.append(file)
        except OSError as os_error:
            logging.critical('Unable to read folder: ' + data_folder + '\n' + str(os_error))
        logging.debug('All files in data folder: ' + str(contents))
        return contents

    def filter_file_list(self, contents):
        filtered_content = []
        for extension in self.extensions:
            for content in contents:
                if content.endswith(extension):
                    filtered_content.append(content)
        logging.debug('Filtered file list: ' + str(filtered_content))
        return filtered_content
