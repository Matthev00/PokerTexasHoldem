from classes import Player, Card, ComputerPlayer, HumanPlayer, Table, Game
from classes import NegativeValueError, OutOfRangeError
from classes import create_deck, score
import pytest


def test_player():
    player = Player()
    assert player.chips == 10000
    assert player.cards == []


def test_player_add_chips_typical():
    player = Player()
    player.add_chips(1000)
    assert player.chips == 11000


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
    assert player.points() == (5.04, 1)


def test_player_fold():
    player = Player()
    assert player.fold() == (1, 0)


def test_player_call():
    player = Player()
    assert player.call(150) == (2, 150)


def test_player_all_in():
    player = Player()
    assert player.all_in() == (4, 10000)


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
    assert player.make_decision(1, 200, 500, False) == (1, 0,)


def test_computer_player_make_decision_minbet_too_high():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 11000, 500, False) == (1, 0)


def test_computer_player_make_decision_hight_min_bet():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 400, 2100, False) == (2, 400)


def test_computer_player_make_decision_bet_higher_then_player_chips():
    player = ComputerPlayer(2)
    card1 = Card(3, 10)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 10001, 10001, False) == (1, 0)
    assert player.make_decision(2, 10001, 10001, False) == (1, 0)
    assert player.make_decision(3, 10001, 10001, False) == (1, 0)
    assert player.make_decision(4, 10001, 10001, False) == (1, 0)


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
    assert player.make_decision(1, 200, 500, False) == (3, 350)


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
    assert player.make_decision(2, 1500, 2000, False) == (1, 0)


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
    assert player.make_decision(2, 400, 500, False) == (3, 550)


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
    assert player.make_decision(3, 400, 500, False) == (3, 550)


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
    assert player.make_decision(4, 400, 500, False) == (3, 550)


def test_computer_player_make_decision_phase_1_call():
    player = ComputerPlayer(2)
    card1 = Card(3, 8)
    card2 = Card(1, 5)
    cards = [card1, card2]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(1, 200, 2050, False) == (2, 200)


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
    assert player.make_decision(2, 400, 4050, False) == (2, 400)


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
    assert player.make_decision(3, 400, 5050, False) == (2, 400)


def test_computer_player_make_decision_phase_3_all_in_three_of_kind():
    player = ComputerPlayer(2)
    card1 = Card(3, 5)
    card2 = Card(1, 4)
    card3 = Card(3, 3)
    card4 = Card(1, 2)
    card5 = Card(3, 6)
    card6 = Card(2, 9)
    card7 = Card(1, 9)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(3, 11000, 5050, False) == (4, 10000)


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
    assert player.make_decision(4, 400, 5050, False) == (2, 400)


def test_computer_player_make_decision_phase_4_all_in_three_of_kind():
    player = ComputerPlayer(2)
    card1 = Card(3, 5)
    card2 = Card(1, 4)
    card3 = Card(3, 3)
    card4 = Card(1, 2)
    card5 = Card(3, 6)
    card6 = Card(2, 9)
    card7 = Card(1, 9)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert player.cards == []
    player.add_cards(cards)
    assert player.make_decision(4, 11000, 5050, False) == (4, 10000)


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


def test_human_player_play_all_in(monkeypatch):
    player = HumanPlayer()
    assert player.chips == 10000
    monkeypatch.setattr('builtins.input', lambda _: "4")
    assert player.play(200) == (4, 10000)
    assert player.chips == 0


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
    table._all_in = [False, False, False]
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
    table._all_in = [False, False, False]
    player._cards = [Card(3, 14), Card(2, 12)]
    com1._cards = [Card(2, 13), Card(1, 12)]
    com2._cards = [Card(4, 12), Card(3, 11)]
    assert table.who_wins() == player


def test_table_who_wins_high_card():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [False, False, False]
    table._all_in = [False, False, False]
    cards = [Card(2, 14), Card(2, 13), Card(3, 7), Card(1, 2), Card(3, 4)]
    player._cards = [Card(3, 12), Card(2, 11)] + cards
    com1._cards = [Card(2, 11), Card(1, 10)] + cards
    com2._cards = [Card(4, 10), Card(3, 9)] + cards
    assert table.who_wins() == player


def test_table_who_wins_all_in():
    player = HumanPlayer()
    com1 = ComputerPlayer(1)
    com2 = ComputerPlayer(2)
    players = [player, com1, com2]
    table = Table(1, players)
    table._folded = [False, True, True]
    table._all_in = [True, False, False]
    table._bets = [10000, 15000, 400]
    com1._chips = 0
    player._chips = 0
    player._cards = [Card(3, 14), Card(2, 12)]
    com1._cards = [Card(2, 14), Card(1, 12)]
    com2._cards = [Card(4, 14), Card(3, 12)]
    assert table.who_wins() == player
    assert com1.chips == 5000
    assert player.chips == 20400


def test_game():
    game = Game(5, 'Stefan')
    assert game._player.name == 'Stefan'
    assert len(game._players) == 6


def test_create_deck():
    deck = create_deck()
    assert len(deck) == 52
    assert type(deck[1]) == Card


def test_score_high_card_two_card():
    card1 = Card(2, 8)
    card2 = Card(2, 7)
    cards = [card1, card2]
    assert score(cards) == (8.07, 2)


def test_score_high_card_seven_cards():
    card1 = Card(2, 14)
    card2 = Card(3, 11)
    card3 = Card(4, 9)
    card4 = Card(1, 7)
    card5 = Card(2, 5)
    card6 = Card(4, 3)
    card7 = Card(2, 4)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (14.11, 2)


def test_score_pair_in_2_cards():
    card1 = Card(2, 11)
    card2 = Card(3, 11)
    cards = [card1, card2]
    assert score(cards) == (110, 3)


def test_score_pair_in_seven_cards():
    card1 = Card(2, 11)
    card2 = Card(3, 11)
    card3 = Card(4, 9)
    card4 = Card(1, 7)
    card5 = Card(2, 5)
    card6 = Card(4, 3)
    card7 = Card(2, 4)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (110.90705, 3)


def test_score_2_pairs():
    card1 = Card(2, 11)
    card2 = Card(3, 11)
    card7 = Card(4, 9)
    card6 = Card(1, 9)
    card5 = Card(2, 5)
    card3 = Card(4, 3)
    card4 = Card(2, 4)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (1190.05, 3)


def test_score_2_pairs_aces_on_two():
    card1 = Card(2, 2)
    card2 = Card(3, 2)
    card7 = Card(4, 14)
    card6 = Card(1, 14)
    card5 = Card(2, 5)
    card3 = Card(4, 3)
    card4 = Card(2, 4)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (1421.05, 4)


def test_score_three_of_kind():
    card1 = Card(2, 11)
    card2 = Card(4, 11)
    card3 = Card(4, 3)
    card4 = Card(2, 4)
    card5 = Card(2, 5)
    card6 = Card(1, 9)
    card7 = Card(3, 11)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (11009.05, 4)


def test_score_strit_on_2():
    card1 = Card(2, 2)
    card2 = Card(4, 3)
    card3 = Card(4, 10)
    card4 = Card(2, 5)
    card5 = Card(2, 4)
    card6 = Card(1, 2)
    card7 = Card(3, 6)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (20000, 3)


def test_score_strit_on_10():
    card1 = Card(2, 12)
    card2 = Card(4, 12)
    card3 = Card(4, 13)
    card4 = Card(2, 5)
    card5 = Card(2, 11)
    card6 = Card(1, 10)
    card7 = Card(3, 14)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (100000, 3)


def test_score_color_max_card_6():
    card1 = Card(2, 2)
    card2 = Card(2, 3)
    card3 = Card(4, 6)
    card4 = Card(2, 5)
    card5 = Card(2, 4)
    card6 = Card(1, 2)
    card7 = Card(2, 7)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (700000, 2)


def test_score_color_max_card_ace():
    card1 = Card(4, 2)
    card2 = Card(3, 10)
    card3 = Card(4, 10)
    card4 = Card(4, 5)
    card5 = Card(4, 4)
    card6 = Card(4, 3)
    card7 = Card(4, 14)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (1400000, 4)


def test_score_full_2_on_3():
    card1 = Card(1, 2)
    card2 = Card(3, 3)
    card3 = Card(3, 2)
    card4 = Card(4, 5)
    card5 = Card(2, 2)
    card6 = Card(4, 3)
    card7 = Card(4, 14)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (2000030, 3)


def test_score_full_9_on_aces_with_pair_of_10():
    card1 = Card(1, 9)
    card2 = Card(3, 10)
    card3 = Card(3, 9)
    card4 = Card(3, 14)
    card5 = Card(2, 9)
    card6 = Card(4, 10)
    card7 = Card(4, 14)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (9000140, 3)


def test_score_full_aces_on_kings_with_pair_of_10():
    card1 = Card(1, 14)
    card2 = Card(3, 10)
    card3 = Card(3, 14)
    card4 = Card(3, 13)
    card5 = Card(2, 14)
    card6 = Card(4, 10)
    card7 = Card(4, 13)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (14000130, 3)


def test_score_four_of_kind_ace():
    card1 = Card(1, 14)
    card2 = Card(4, 10)
    card3 = Card(3, 14)
    card4 = Card(2, 10)
    card5 = Card(2, 14)
    card6 = Card(3, 10)
    card7 = Card(4, 14)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (140000000.1, 4)


def test_score_four_of_kind_2():
    card1 = Card(1, 2)
    card2 = Card(4, 9)
    card3 = Card(3, 2)
    card4 = Card(4, 13)
    card5 = Card(2, 2)
    card6 = Card(4, 10)
    card7 = Card(4, 2)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (20000000.13, 4)


def test_score_poker_on_2_hearts():
    card1 = Card(3, 2)
    card2 = Card(2, 6)
    card3 = Card(3, 3)
    card4 = Card(3, 5)
    card5 = Card(3, 4)
    card6 = Card(4, 5)
    card7 = Card(3, 6)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (150000002, 3)


def test_score_poker_on_10_spades():
    card1 = Card(4, 14)
    card2 = Card(4, 6)
    card3 = Card(4, 10)
    card4 = Card(4, 13)
    card5 = Card(4, 12)
    card6 = Card(4, 5)
    card7 = Card(4, 11)
    cards = [card1, card2, card3, card4, card5, card6, card7]
    assert score(cards) == (150000010, 4)
