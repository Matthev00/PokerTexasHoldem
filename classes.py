from random import shuffle, randint


class Player:
    def __init__(self):
        self._chips = 10000
        self._cards = []

    @property
    def id(self):
        return self._id

    @property
    def chips(self):
        return self._chips

    def add_cards(self, cards):
        self._cards += cards

    @property
    def cards(self):
        return self._cards

    def call(self, min_bet):
        self.chips -= min_bet
        return (2, min_bet)

    def raisee(self, min_bet):
        self.chips -= min_bet
        to_rand = self.chips // 50
        bet = randint(1, to_rand) * 50
        return (3, bet+min_bet)

    def fold(self):
        return (1, 0)

    def points(self):
        return score(self.cards)


class ComputerPlayer(Player):
    def __init__(self, id=0):
        super().__init__()
        self._name = f'Computer{id}'
        self._id = id

    @property
    def name(self):
        return self._name

    def make_decision(self, phase, min_bet):
        points, color = self.points()
        if phase == 1:
            if min_bet > self.chips / 10 and points > 11:
                ans = self.call(min_bet)
            elif min_bet < self.chips / 10 and points > 11:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        elif phase == 2:
            if min_bet > self.chips / 7 and points > 100:
                ans = self.call(min_bet)
            elif min_bet < self.chips / 7 and points > 100:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        elif phase == 3:
            if min_bet > self.chips / 5 and points > 130:
                ans = self.call(min_bet)
            elif min_bet < self.chips / 5 and points > 130:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        elif phase == 4:
            if min_bet < self.chips and points > 130:
                ans = self.call(min_bet)
            elif min_bet <= self.chips and points > 1000:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        return ans


class HumanPlayer(Player):
    def __init__(self, name='Player'):
        super().__init__()
        self._id = 0
        self._name = name

    @property
    def name(self):
        return self._name

    def print_cards(self):
        print(self.cards[0])
        print(self._cards[1])


class Card:
    def __init__(self, suit, rank):
        self.ranks = {
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
            10: "Ten",
            11: "Jack",
            12: "Queen",
            13: "King",
            14: "Ace"
        }
        self.suits = {
            4: "spades",
            3: "hearts",
            2: "diamonds",
            1: "clubs"
        }
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def __str__(self) -> str:
        return f'{self.ranks[self.rank]} of {self.suits[self.suit]}'


class Table:
    def __init__(self, dealer, players=None):
        if not players:
            self._players = []
        else:
            self._players = players
        self._pot = 0
        self._calls = []
        self._bets = []
        self._deck = []
        self._deck = create_deck()
        self._dealer = players[dealer]
        self._big_blind = players[(dealer+2) % len(players)]
        self._small_blind = players[(dealer+1) % len(players)]

    def bidding(self, phase):
        while False in self._calls:
            if len(self._players) > 1:
                print(f'{self._players[0].name} won {self._pot}!!')
                self._players[0].chips += self._pot
                return 'END'
            start = self._small_blind
            for player in self._players:
                self._calls[player.id] = False
            for i in range(start, start, 0):
                to_bet = self._max_bet - self._bets[i]
                if self._players[i].id != 0:
                    data = self._players[i].make_decision(phase, to_bet)
                else:
                    data = self._players[i].play(to_bet)
                if data[0] == 1:
                    print(f'{self._players[i].name} folded')
                    self._calls[i] = True
                    self._players.pop(self._players[i])
                elif data[0] == 2:
                    print(f'{self._players[i].name} called')
                    self._calls[i] = True
                    self._bets[i] += data[1]
                    self._pot += data[1]
                else:
                    print(f'{self._players[i].name} raised {data[1]}')
                    self._bets[i] += data[1]
                    self._pot += data[1]
                self._max_bet = max(self._max_bet, self._bets[i])
                i = (i + 1) % len(self._players)

    def first_phase(self):
        print('Cards dealt.')
        print('Your Cards')
        print('Lets get the bidding started')
        for player in self._players:
            player.add_cards([self._deck.pop(), self._deck.pop()])
        print('Your cards')
        self._players[0].print_cards()
        for player in self._players:
            self._calls.append(False)
            self._bets.append(0)
        self._bets[self._small_blind] = 50
        self._players[self._small_blind].call(50)
        self._bets[self._big_blind] = 100
        self._players[self._big_blind].call(100)
        self._max_bet = 100
        self._pot = 150
        if self.bidding(1) == 'END':
            return 'END'
        print('End of bidding phase')

    def flop(self):
        print('Flop')
        print('Your cards')
        self._players[0].print_cards()
        self._cards_on_table = [
            self._deck.pop(),
            self._deck.pop(),
            self._deck.pop()
        ]
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        for player in self._players:
            player.add_card(self._cards_on_table)
        if self.bidding(2) == 'END':
            return 'END'
        print('End of flop phase')

    def river(self):
        print('River')
        print('Your cards')
        self._players[0].print_cards()
        river_card = self._deck.pop()
        self._cards_on_table.append(river_card)
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        for player in self._players:
            player.add_card([river_card])
        if self.bidding(3) == 'END':
            return 'END'
        print('End of river phase')

    def turn(self):
        print('Turn')
        print('Your cards')
        self._players[0].print_cards()
        turn_card = self._deck.pop()
        self._cards_on_table.append(turn_card)
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        for player in self._players:
            player.add_card([turn_card])
        if self.bidding(4) == 'END':
            return 'END'
        print('End of turn phase')

    def who_wins(self):
        self._scores = []
        for player in self._players:
            points, color = player.points()
            self._scores.append((points, color, player))
        self._scores = sorted(self._scores, reverse=True)
        if self._scores[0][0] > self._scores[1][0]:
            self._scores[0][2].chips += self._pot
            print(f'{self._scores[0][2].name} won {self._pot}!!')
        else:
            win_score = self._scores[0][1]
            winner = self._scores[0][2]
            for i in range(1, len(self._scores)):
                if self._scores[i][0] == self._scores[i-1][0]:
                    if self._scores[i][1] > win_score:
                        winner = self._scores[i][2]
                else:
                    break
            winner.chps += self._pot
            print(f'{winner.name} won {self._pot}!!')

    def play_table(self):
        if self.first_phase() != 'END':
            if self.flop() != 'END':
                if self.river() != 'END':
                    if self.turn() != 'END':
                        self.who_wins()


class Game:
    def __init__(self, num_of_players, player_name):
        self._num_of_players = int(num_of_players)
        self._players = []
        self._player = HumanPlayer(player_name)
        self._players.append(self._player)
        for i in range(1, self._num_of_players+1):
            computer = ComputerPlayer(i)
            self._players.append(computer)

    def play(self):
        dealer = randint(1, self._num_of_players) - 1
        rund = 1
        while True:
            table = Table(dealer, self._players)
            table.play_table()
            if self._player.chips == 0:
                print("Unfortunately You've lost")
            else:
                print("Options:")
                print(f"1: Go away with {self._player.chips}")
                print('2: Play at new table')
                if input("Choose option") == '1':
                    print(f'Your winnings is {self._player.chips}')
                    return self._player.chips
            rund += 1


def create_deck():
    deck = []
    """
    suits:
        4: spades
        3: hearts
        2: diamonds
        1: clubs
    ranks:
        1: 1
        2: 2
        ...
        11: jack
        12: queen
        13: king:
        14: ace
    """
    for suit in range(1, 5):
        for rank in range(2, 15):
            deck.append(Card(suit, rank))
    deck = shuffle(deck)
    return deck


def score(players_cards):
    """
    returns score of given cards
    """
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
