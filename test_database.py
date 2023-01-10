from database import Database, RankingPathNotFound
import pytest


def test_load_from_file():
    database = Database()
    database.load_from_file()
    assert len(database.ranking) == 6


def test_load_from_file_not_found():
    database = Database()
    with pytest.raises(RankingPathNotFound):
        database.load_from_file('xyz')


def test_save_to_file():
    database = Database()
    database.load_from_file()
    database.save_to_file('ranking2.txt')
    database.load_from_file('ranking2.txt')
    assert len(database.ranking) == 6


def test_addd_to_ranking():
    database = Database()
    database.add_to_ranking(('name1', 100))
    assert len(database.ranking) == 7
