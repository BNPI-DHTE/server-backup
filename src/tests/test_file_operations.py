import os
from glob import glob
from os import path

import pytest
from testfixtures import tempdir

from src.BackupCreator import BackupCreator

file_content = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer convallis lacinia diam, et finibus ' \
               b'metus laoreet ac. In bibendum dui et nibh dictum vestibulum. Nullam ac erat at tellus elementum ' \
               b'scelerisque. Aenean sit amet felis vulputate, dignissim mi eget, dignissim risus. Suspendisse ' \
               b'condimentum leo sit amet quam dapibus, eget maximus ipsum ultricies. Pellentesque ultricies sapien ' \
               b'id enim finibus, id condimentum nibh fermentum. Lorem ipsum dolor sit amet, consectetur adipiscing ' \
               b'elit. Aliquam erat volutpat. Orci varius natoque penatibus et magnis dis parturient montes, ' \
               b'nascetur ridiculus mus. Pellentesque elit augue, pellentesque et massa nec, scelerisque volutpat ' \
               b'magna.'

temp_initials = ['aa', 'ab', 'bb', 'bc']


def init_temp_file_system(temp_folder):
    for temp_initial in temp_initials:
        temp_folder.write(('data', temp_initial, temp_initial + '_text.TXT'), file_content)
        temp_folder.write(('data', temp_initial, temp_initial + '_gpkg.db'), file_content)
        temp_folder.write(('data', temp_initial, temp_initial + '_db.GPKG'), file_content)
        temp_folder.write(('data', temp_initial, temp_initial + '_db.gpkg-wal'), file_content)
        temp_folder.write(('data', temp_initial, temp_initial + '_db.GPKG-shm'), file_content)
        temp_folder.write(('project', temp_initial, temp_initial + '_project.qgs'), file_content)
        temp_folder.write(('project', temp_initial, temp_initial + '_project.QGZ'), file_content)
    return temp_folder.path


@tempdir()
def test_make_tarfile(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    creator = BackupCreator(
        'data',
        root_folder,
        'data',
        'backup',
        ['gpkg', 'gpkg-wal', 'gpkg-shm'],
        'xz'
    )

    creator.make_tarfile()

    result_tarfile_path = glob(path.join(root_folder, 'backup', 'data', '*'))[0]
    result_tarfile_name = result_tarfile_path.replace(path.join(root_folder, 'backup', 'data') + '/', '')
    assert path.isdir(path.join(root_folder, 'backup', 'data'))
    assert path.isfile(result_tarfile_path)
    assert result_tarfile_name.startswith('data_backup_')
    assert result_tarfile_name.endswith('.tar.xz')


@tempdir()
def test_create_list_of_all_files(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    files_to_check = ['project/aa/aa_project.qgs',
                      'data/aa/aa_gpkg.db',
                      'data/ab/ab_text.TXT',
                      'data/ab/ab_db.GPKG',
                      'project/bb/bb_project.QGZ',
                      'data/bb/bb_db.gpkg-wal',
                      'data/bc/bc_db.GPKG-shm']
    creator = BackupCreator('data',
                            root_folder,
                            root_folder,
                            'backup',
                            ['gpkg', 'gpkg-wal', 'gpkg-shm'],
                            'xz')

    all_files = creator.create_list_of_all_files()

    assert (all_files.__len__() == 28)
    for file in files_to_check:
        assert file in all_files
    assert 'project/bb' not in all_files


@tempdir()
def test_filter_file_list(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    files_to_check = ['data/aa/aa_db.GPKG',
                      'data/ab/ab_db.gpkg-wal',
                      'data/bb/bb_db.GPKG-shm']
    creator = BackupCreator('data',
                            root_folder,
                            root_folder,
                            'backup',
                            ['gpkg', 'gpkg-wal', 'gpkg-shm'],
                            'xz')

    all_files = creator.create_list_of_all_files()
    filtered_files = creator.filter_file_list(all_files)

    assert filtered_files.__len__() == 12
    for file in files_to_check:
        assert file in filtered_files
    assert 'data/bc/bc_test.TXT' not in filtered_files
    assert 'data/aa/aa_gpkg.db' not in filtered_files


@tempdir()
def test_create_file_list_to_archive(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    files_to_check = ['project/aa/aa_project.qgs',
                      'project/bc/bc_project.QGZ']
    creator = BackupCreator('project',
                            root_folder,
                            root_folder,
                            'backup',
                            ['qgs', 'qgz'],
                            'gz')

    files_to_archive = creator.create_file_list_to_archive()

    assert files_to_archive.__len__() == 8
    for file in files_to_check:
        assert file in files_to_archive
    assert 'data/ab/ad_db.GPKG' not in files_to_archive


@tempdir()
def test_system_exit_when_data_folder_does_not_exist(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    creator = BackupCreator('project',
                            root_folder,
                            'invalid_data_folder',
                            'backup',
                            ['qgs', 'qgz'],
                            'gz')

    with pytest.raises(SystemExit) as system_exit:
        creator.create_list_of_all_files()

    assert str(system_exit.value) == 'The data folder ' + path.join(root_folder, creator.data_relative_path) + \
           '/ is empty or does not exist! Check the relative data path you entered in the config file! Exiting!'


@tempdir()
def test_system_exit_when_data_folder_is_empty(temp_folder):
    root_folder = init_temp_file_system(temp_folder)
    os.mkdir(path.join(root_folder, 'empty_data_folder'))

    creator = BackupCreator('project',
                            root_folder,
                            'empty_data_folder',
                            'backup',
                            ['qgs', 'qgz'],
                            'gz')

    with pytest.raises(SystemExit) as system_exit:
        creator.create_list_of_all_files()

    assert str(system_exit.value) == 'The data folder ' + path.join(root_folder, creator.data_relative_path) + \
           '/ is empty or does not exist! Check the relative data path you entered in the config file! Exiting!'
