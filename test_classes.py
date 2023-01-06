from classes import Player, Card, ComputerPlayer, HumanPlayer, Table, Game
from classes import NegativeValueError, OutOfRangeError
from classes import create_deck
import pytest


def test_player():
    player = Player()
    assert player.chips == 10000
    assert player.cards == []


def test_player_add_chips_typical():
    player = Player()
    player.add_chips(1000)
    player.chips == 11000


def test_player_add_chips_negative():
    player = Player()
    with pytest.raises(NegativeValueError):
        player.add_chips(-1000)


def test_player_add_cards():
    player = Player()
    card1 = Card(3, 4)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert len(player.cards) == 2


def test_player_print_cards_points():
    player = Player()
    card1 = Card(3, 4)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.points() == (5, 1)


def test_player_fold():
    player = Player()
    assert player.fold() == (1, 0)


def test_player_call():
    player = Player()
    assert player.call(150) == (2, 150)


def test_computer_player():
    player = ComputerPlayer(2)
    assert player.chips == 10000
    assert player.cards == []
    assert player.id == 2
    assert player.name == 'Computer2'


def test_computer_player_negative_id():
    with pytest.raises(NegativeValueError):
        ComputerPlayer(-2)


def test_computer_player_raisee_typical(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    assert player.chips == 10000
    assert player.raisee(100, 1) == (3, 250)
    assert player.chips == 9750


def test_computer_player_raisee_phase_out_of_range():
    player = ComputerPlayer(2)
    with pytest.raises(OutOfRangeError):
        player.raisee(100, 5)


def test_computer_player_make_decision_points_lower_then_8():
    player = ComputerPlayer(2)
    card1 = Card(3, 7)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 200, 500) == (1, 0)


def test_computer_player_make_decision_minbet_too_high():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 11000, 500) == (1, 0)


def test_computer_player_make_decision_hight_min_bet():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 400, 2100) == (2, 400)


def test_computer_player_make_decision_bet_higher_then_player_chips():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 10001, 10001) == (1, 0)
    assert player.make_decision(2, 10001, 10001) == (1, 0)
    assert player.make_decision(3, 10001, 10001) == (1, 0)
    assert player.make_decision(4, 10001, 10001) == (1, 0)


def test_computer_player_make_decision_phase_1_raisee(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 200, 500) == (3, 350)


def test_computer_player_make_decision_phase_2_low_cards():
    player = ComputerPlayer(2)
    card1 = Card(3, 14)
    card2 = Card(1, 7)
    card3 = Card(3, 2)
    card4 = Card(1, 3)
    card5 = Card(3, 4)
    cards = [card1, card2, card3, card4, card5]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(2, 1500, 2000) == (1, 0)


def test_computer_player_make_decision_phase_2_raisee_pair(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 2)
    card3 = Card(3, 2)
    card4 = Card(1, 3)
    card5 = Card(3, 4)
    cards = [card1, card2, card3, card4, card5]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(2, 400, 500) == (3, 550)


def test_computer_player_make_decision_phase_3_raisee_pair(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 7)
    card3 = Card(3, 7)
    card4 = Card(1, 3)
    card5 = Card(3, 4)
    card6 = Card(2, 7)
    cards = [card1, card2, card3, card4, card5, card6]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(3, 400, 500) == (3, 550)


def test_computer_player_make_decision_phase_4_raisee_2_pair(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    card1 = Card(3, 5)
    card2 = Card(1, 4)
    card3 = Card(3, 3)
    card4 = Card(1, 2)
    card5 = Card(3, 2)
    card6 = Card(2, 10)
    card7 = Card(1, 10)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(4, 400, 500) == (3, 550)


def test_computer_player_make_decision_phase_1_call():
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 200, 2050) == (2, 200)


def test_computer_player_make_decision_phase_2_call_pair():
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 2)
    card3 = Card(3, 2)
    card4 = Card(1, 3)
    card5 = Card(3, 4)
    cards = [card1, card2, card3, card4, card5]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(2, 400, 4050) == (2, 400)


def test_computer_player_make_decision_phase_3_call_pair():
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 7)
    card3 = Card(3, 7)
    card4 = Card(1, 3)
    card5 = Card(3, 4)
    card6 = Card(2, 7)
    cards = [card1, card2, card3, card4, card5, card6]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(3, 400, 5050) == (2, 400)


def test_computer_player_make_decision_phase_4_call_2_pair(monkeypatch):
    def fake(t, f):
        return 3
    monkeypatch.setattr('classes.randint', fake)
    player = ComputerPlayer(2)
    card1 = Card(3, 5)
    card2 = Card(1, 4)
    card3 = Card(3, 3)
    card4 = Card(1, 2)
    card5 = Card(3, 2)
    card6 = Card(2, 9)
    card7 = Card(1, 9)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(3, 400, 5050) == (2, 400)


def test_human_player_typical():
    player = HumanPlayer('Jurek Ogórek')
    assert player.name == 'Jurek Ogórek'
    assert player.id == 0
    assert player.chips == 10000
    assert player.cards == []


def test_human_player_empty_name():
    player = HumanPlayer()
    assert player.name == 'Player'
    assert player.id == 0
    assert player.chips == 10000
    assert player.cards == []


def test_human_player_praise_typical():
    player = HumanPlayer()
    assert player.chips == 10000
    assert player.p_raise(100) == (3, 100)
    assert player.chips == 9900


def test_human_player_praise_bet_higher_then_chips():
    player = HumanPlayer()
    assert player.chips == 10000
    with pytest.raises(OutOfRangeError):
        player.p_raise(10001)


def test_human_player_praise_negative_bet():
    player = HumanPlayer()
    assert player.chips == 10000
    with pytest.raises(NegativeValueError):
        player.p_raise(-50)


def test_human_player_play_call(monkeypatch):
    player = HumanPlayer()
    assert player.chips == 10000
    monkeypatch.setattr('builtins.input', lambda _: "2")
    assert player.play(200) == (2, 200)
    assert player.chips == 9800


def test_human_player_play_fold(monkeypatch):
    player = HumanPlayer()
    assert player.chips == 10000
    monkeypatch.setattr('builtins.input', lambda _: "3")
    assert player.play(200) == (1, 0)
    assert player.chips == 10000


def test_card():
    card = Card(3, 8)
    assert card.suit == 3
    assert card.rank == 8
    assert card.__str__() == 'Eight of hearts'


def test_table():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    assert table.players == players
    assert table._pot == 0
    assert table._calls == []
    assert table._bets == []
    assert table._folded == []
    assert len(table._deck) == 52
    assert table._small_blind == 2
    assert table._big_blind == 0


def test_table_potential_end_true():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [True, True, False, True]
    assert table.potential_end() is True


def test_table_potential_end_false():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [True, False, False, True]
    assert table.potential_end() is False


def test_table_everyone_called_true():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._calls = [True, True, False, True]
    assert table.everyone_called() is True


def test_table_everyone_called_false():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._calls = [True, False, False, True]
    assert table.everyone_called() is False


def test_table_first_phase(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    monkeypatch.setattr('classes.score', lambda _: (0, 1))
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table.first_phase()
    for player in players:
        assert len(player.cards) == 2
    assert table._bets[2] == 50
    assert table._bets[0] == 100
    assert table._pot == 150


def test_table_flop(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    monkeypatch.setattr('classes.score', lambda _: (0, 1))
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table.first_phase()
    table.flop()
    for player in players:
        assert len(player.cards) == 5
    assert len(table._cards_on_table) == 3


def test_table_river(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    monkeypatch.setattr('classes.score', lambda _: (0, 1))
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table.first_phase()
    table.flop()
    table.river()
    for player in players:
        assert len(player.cards) == 6
    assert len(table._cards_on_table) == 4


def test_table_turn(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3")
    monkeypatch.setattr('classes.score', lambda _: (0, 1))
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table.first_phase()
    table.flop()
    table.river()
    table.turn()
    for player in players:
        assert len(player.cards) == 7
    assert len(table._cards_on_table) == 5


def test_table_who_wins_equal_point_dif_col():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [False, False, False]
    player._cards = [Card(3, 14), Card(2, 12)]
    com1._cards = [Card(2, 14), Card(1, 12)]
    com2._cards = [Card(4, 14), Card(3, 12)]
    assert table.who_wins() == com2


def test_table_who_wins_typical():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [False, False, False]
    player._cards = [Card(3, 14), Card(2, 12)]
    com1._cards = [Card(2, 13), Card(1, 12)]
    com2._cards = [Card(4, 12), Card(3, 11)]
    assert table.who_wins() == player


def test_game():
    game = Game(5, 'Stefan')
    assert game._player.name == 'Stefan'
    assert len(game._players) == 6


def test_create_deck():
    deck = create_deck()
    assert len(deck) == 52
    assert type(deck[1]) == Card
    