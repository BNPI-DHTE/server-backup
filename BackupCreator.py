from datetime import datetime
from os import mkdir, chdir, walk, path
from glob import glob
import tarfile


def create_missing_folder(folder: str):
    if glob(folder).__len__() == 0:
        mkdir(folder)


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
        chdir(self.root_folder)
        filename = path.join(self.root_folder, self.backup_folder, self.backup_type, self.generate_archive_filename())
        create_missing_folder(self.backup_folder)
        create_missing_folder(path.join(self.backup_folder, self.backup_type))
        files = self.filter_file_list()
        chdir(path.join(self.root_folder, self.data_relative_path))
        with tarfile.open(filename, 'w:' + self.archive_type) as tar:
            for file in files:
                tar.add(file)

    def generate_archive_filename(self):
        current_time = datetime.now()
        date = current_time.strftime('%Y_%m_%d-%H_%M_%S')
        return self.backup_type + '_' + date + '.tar.' + self.archive_type

    def create_file_list(self):
        contents = []
        data_folder = self.root_folder + self.data_relative_path
        for dir_path, dirs, files in walk(data_folder):
            dir_relative_path = dir_path.replace(data_folder, '')
            for file in files:
                contents.append(path.join(dir_relative_path, file))
        return contents

    def filter_file_list(self):
        contents = self.create_list_of_files()
        if not self.extensions.__contains__('*'):
            filtered_content = []
            for extension in self.extensions:
                for content in contents:
                    if content.endswith(extension):
                        filtered_content.append(content)
            return filtered_content
        return contents

    def create_list_of_files(self):
        data_folder = path.join(self.root_folder, self.data_relative_path)
        contents = []
        for dir_path, dirs, files in walk(data_folder):
            dir_relative_path = dir_path.replace(data_folder, '')
            for file in files:
                if dir_relative_path:
                    contents.append(path.join(dir_relative_path, file))
                else:
                    contents.append(file)
        return contents
