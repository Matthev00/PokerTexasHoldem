from ranking_io import read_file, write_to_file
from ranking_io import MalformedRecordDataError
from io import StringIO
import pytest


def test_read_file():
    data = 'place,name,score\n1,name1,10000\n'
    file_handle = StringIO(data)
    ranking = read_file(file_handle)
    assert len(ranking) == 1
    assert ranking[0][0] == '1'


def test_read_file_missing_column():
    data = 'place,name,score\n1,name110000\n'
    file_handle = StringIO(data)
    with pytest.raises(MalformedRecordDataError):
        read_file(file_handle)


def test_write_to_file():
    ranking = [['1', 'name1', 10000], ['2', 'name2', 1000]]
    with open('ranking2.txt', 'w') as file_handle:
        write_to_file(file_handle, ranking)
    with open('ranking2.txt', 'r') as file_handle:
        ranking2 = read_file(file_handle)
    assert ranking == ranking2