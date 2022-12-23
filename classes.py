from random import shuffle


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

    def add_cards(self, cards):
        self._cards += cards

    @property
    def cards(self):
        return self._cards


class ComputerPlayer(Player):
    # def make_smart_decision(self, phase):
    #     cards = []
    #     for card in self.card:
    #         cards.append((card.suit, card.rank))
    #     cards_sorted_by_rank = sorted(cards, key=cards[1])
    #     cards_sorted_by_suit = sorted(card)




class HumanPlayer(Player):
    def calls(self):
        pass

    def raises(self, amount):
        pass

    def fold(self):
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
            player.add_cards([self._deck.pop(), self._deck.pop()])

    def flop(self):
        self._cards_on_table = [
            self._deck.pop(),
            self._deck.pop(),
            self._deck.pop()
        ]
        for player in self._players:
            player.add_card(self._cards_on_table)

    def river(self):
        river_card = self._deck.pop()
        self._cards_on_table.append(river_card)
        for player in self._players:
            player.add_card([river_card])

    def turn(self):
        turn_card = self._deck.pop()
        self._cards_on_table.append(turn_card)
        for player in self._players:
            player.add_card([turn_card])


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
    for suit in suits:
        for rank in range(1, 14):
            deck.append(Card(suit, rank))
    return deck
