from random import shuffle


class HumanPlayer(Player):
    def calls(self):
        pass

    def raises(self, amount):
        pass

    def fold(self):
        pass


class Player:
    def __init__(self, name):
        self._name = name
        self._chips = 10000

    @property
    def name(self):
        return self._name

    @property
    def chips(self):
        return self._chips

    def set_cards(self, cards):
        self._cards = cards

    @property
    def cards(self):
        return self._cards


class ComputerPlayer(Player):
    def make_smart_decision():
        pass


class Card:
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank


class Table:
    def __init__(self, dealer, players=None):
        if not players:
            self._players = []
        else:
            self._players = players
        self._deck = create_deck()
        self._deck = shuffle(self._deck)
        self._dealer = players[dealer]
        self.big_blind = players[(dealer+2) % len(players)]
        self.big_blind = players[(dealer+1) % len(players)]

    def first_phase(self):
        for player in self._players:
            player.set_cards([self._deck.pop(), self._deck.pop()])

    def flop(self):
        self._cards_on_table = [
            self._deck.pop(),
            self._deck.pop(),
            self._deck.pop()
        ]

    def river(self):
        self._cards_on_table.append(self._deck.pop())

    def turn(self):
        self._cards_on_table.append(self._deck.pop())


class Game:
    def __init__(self, players=None):
        if not players:
            self._players = []
        else:
            self._players = players

    def play():
        pass


def create_deck():
    deck = []
    suits = ['c', 'd', 'h', 's']
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'j', 'g', 'k', 'a']
    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit, rank))
    return deck
