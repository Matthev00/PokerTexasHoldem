from database import Database, RankingPathNotFound
import pytest


def test_load_from_file_not_found():
    database = Database()
    with pytest.raises(RankingPathNotFound):
        database.load_from_file('xyz')
