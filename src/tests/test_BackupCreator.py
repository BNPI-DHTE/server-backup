import os
from datetime import datetime

from src.core.BackupCreator import BackupCreator

path = os.path.dirname(__file__)


def test_init_with_minimal_parameters():
    creator = BackupCreator('data', path, 'data', 'backup')
    assert creator.filters == ['*']
    assert creator.archive_type == 'bz2'


def test_init_with_all_parameters():
    creator = BackupCreator('data', path, 'data', 'backup', ['json'], 'xz')
    assert creator.filters.__len__() == 1
    assert creator.archive_type == 'xz'


def test_generate_archive_file_name():
    creator = BackupCreator('data', path, 'data', 'backup')
    current_time = datetime(2022, 2, 15, 11, 10, 15, 121234)
    filename = creator.generate_archive_filename(current_time)
    assert filename == 'data_backup_2022_02_15_11_10_15.tar.bz2'


def test_filter_file_list():
    creator = BackupCreator('data', path, 'data', 'backup', ['gpkg', 'gpkg-shm', 'gpkg-wal'], 'xz')
    contents = ['users/johndoe/database.sqlite',
                'users/johndoe/project.zip',
                'users/johndoe/project.qgs',
                'users/johndoe/database.qgz',
                'users/johndoe/database.gpkg-wal',
                'users/johndoe/database.gpkg-shm',
                'users/johndoe/database.gpkg',
                'users/johndoe/another_database.GPKG',
                'users/johndoe/another_database.GPKG-WAL',
                'users/johndoe/another_database.GPKG-SHM'
                ]
    assert creator.filter_file_list(contents).__len__() == 6
