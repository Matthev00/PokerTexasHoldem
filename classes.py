from random import shuffle


class Player:
    def __init__(self, name):
        self._name = name
        self._chips = 10000
        self._cards = []

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
    def make_smart_decision(self, phase):
        pass


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
    """
    suits:
        4: spades
        3: hearts
        2: diamonds
        1: Clubs
    """
    for suit in range(1, 5):
        for rank in range(2, 15):
            deck.append(Card(suit, rank))
    return deck


def score(players_cards):
    cards = []
    for card in players_cards:
        cards.append((card.suit, card.rank))
    cards
    ranks = [0 for i in range(2, 15)]
    suits = [0 for i in range(1, 5)]
    cards_sorted_by_rank = sorted(cards, key=lambda x: x[1], reverse=True)
    counter1 = 0
    for i in range(1, len(cards_sorted_by_rank)):
        if cards_sorted_by_rank[i] + 1 == cards_sorted_by_rank[i-1]:
            counter1 += 1
            first1 = cards_sorted_by_rank[i-1]
        else:
            counter1 = 0
    pairs = 0
    threes = 0
    fours = 0
    for rank in cards:
        ranks[rank[1]] += 1
    for suit in cards:
        suits[suit[0]] += 1
    for i in range(1, 5):
        if suits[i] >= 5:
            color = i
    for rank in ranks:
        if rank == 2:
            pairs += 1
        elif rank == 3:
            threes += 1
        elif rank == 4:
            fours += 1
    score_color = 0
    if pairs == 0 and threes == 0 and fours == 0:
        for i in range(14, 1, -1):
            if ranks[i] == 1:
                score = i
                for card in cards_sorted_by_rank:
                    if card[1] == i:
                        score_color = max(score_color, card[0])
                break
    elif pairs == 1 and threes == 0 and fours == 0:
        for i in range(14, 1, -1):
            if ranks[i] == 2:
                score = 10 * i
                for card in cards_sorted_by_rank:
                    if card[1] == i:
                        score_color = max(score_color, card[0])
                break
    elif pairs >= 2 and threes == 0 and fours == 0:
        h = False
        low = False
        for i in range(14, 1, -1):
            if ranks[i] == 2:
                if not h:
                    if i == 14:
                        score += 1
                    score += 100 * i
                    for card in cards_sorted_by_rank:
                        if card[1] == i:
                            score_color = max(score_color, card[0])
                elif not low:
                    score += 10 * i
                    low = True
                    for card in cards_sorted_by_rank:
                        if card[1] == i:
                            score_color = max(score_color, card[0])
                h = True
    elif pairs == 0 and threes >= 1 and fours == 0:
        for i in range(14, 1, -1):
            if ranks[i] == 3:
                score = 1000 * i
                for card in cards_sorted_by_rank:
                    if card[1] == i:
                        score_color = max(score_color, card[0])
                break
    elif pairs >= 1 and threes >= 1 and fours == 0:
        three = False
        two = False
        for i in range(14, 1, -1):
            if ranks[i] == 3 and not three:
                score += 1000000 * i
                three = True
            elif ranks[i] == 2 and not two:
                two = True
                score += 10 * i
    elif fours:
        for i in range(14, 1, -1):
            if ranks[i] == 4:
                score = i * 10000000
    elif color:
        score_color = color
        chance_for_poker = []
        for card in cards_sorted_by_rank:
            if card[0] == color:
                chance_for_poker.append(card[1])
        counter = 0
        for i in range(1, len(chance_for_poker)):
            if chance_for_poker[i] + 1 == chance_for_poker[i-1]:
                counter += 1
                first = chance_for_poker[i-1]
            else:
                counter = 0
        if counter >= 5:
            score = 150000000 + first
        else:
            score = chance_for_poker[0] * 100000
    elif counter1 >= 5:
        score = first1 * 10000
    return (score, score_color)
