import os

from BackupCreator import BackupCreator

path = os.path.dirname(__file__)


def test_init_with_minimal_parameters():
    creator = BackupCreator('data', path, 'data', 'backup')
    assert creator.extensions == ['*']
    assert creator.archive_type == 'bz2'


def test_init_with_all_parameters():
    creator = BackupCreator('data', path, 'data', 'backup', ['json'], 'xz')
    assert creator.extensions.__len__() == 1
