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

    def add_chips(self, achips):
        self._chips += achips

    def add_cards(self, cards):
        self._cards += cards

    @property
    def cards(self):
        return self._cards

    def call(self, min_bet):
        self._chips -= min_bet
        return (2, min_bet)

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

    def raisee(self, min_bet):
        self._chips -= min_bet
        to_rand = self.chips // 50
        bet = randint(1, to_rand) * 50
        self._chips -= bet
        return (3, bet+min_bet)

    def make_decision(self, phase, min_bet):
        points, color = self.points()
        if phase == 1:
            if (
                min_bet > self.chips / 10 and
                points > 8 and
                min_bet < self.chips
            ):
                ans = self.call(min_bet)
            elif min_bet < self.chips / 10 and points >= 8:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        elif phase == 2:
            if (
                min_bet > self.chips / 7 and
                points > 20 and
                min_bet < self.chips
            ):
                ans = self.call(min_bet)
            elif min_bet < self.chips / 7 and points > 20:
                ans = self.raisee(min_bet)
            else:
                ans = self.fold()
        elif phase == 3:
            if (
                min_bet > self.chips / 5 and
                points > 70 and
                min_bet < self.chips
            ):
                ans = self.call(min_bet)
            elif min_bet < self.chips / 5 and points > 70:
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

    def p_raise(self, bet):
        self._chips -= bet
        return (3, bet)

    def play(self, to_bet):
        print('Options:')
        print(f'1: raise(over {to_bet}, multiple of 50)')
        print(f'2: call({to_bet})')
        print('3: fold')
        inp = int(input('Choose option: '))
        if inp == 1:
            ans = self.p_raise(int(input('Your bet: ')))
        elif inp == 2:
            ans = self.call(to_bet)
        elif inp == 3:
            ans = self.fold()
        return ans


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
        self._folded = []
        self._deck = create_deck()
        self._dealer = players[dealer]
        self._big_blind = players[(dealer+2) % len(players)].id
        self._small_blind = players[(dealer+1) % len(players)].id

    def potential_end(self):
        counter = 0
        for element in self._folded:
            if element is False:
                counter += 1
        if counter == 1:
            return True
        else:
            return False

    def everyone_called(self):
        counter = 0
        for player in self._calls:
            if player is False:
                counter += 1
        if counter == 1:
            return True
        else:
            return False

    def bidding(self, phase):
        for player in self._players:
            if self._folded[player.id]:
                self._calls[player.id] = True
            else:
                self._calls[player.id] = False
        while self.everyone_called() is False:
            if self.potential_end() is True:
                for index in range(0, len(self._players)):
                    if self._folded[index] is False:
                        print(f'{self._players[index].name} won {self._pot}!!')
                        self._players[index].add_chips(self._pot)
                return 'END'
            start = self._small_blind
            for player in self._players:
                if self._folded[player.id]:
                    self._calls[player.id] = True
                else:
                    self._calls[player.id] = False
            i = start
            k = 0
            while k < len(self._players):
                if self.potential_end() or self.everyone_called():
                    i = (i + 1) % len(self._players)
                    k += 1
                    break
                if self._folded[i] is False:
                    to_bet = self._max_bet - self._bets[i]
                    if self._players[i].id != 0:
                        data = self._players[i].make_decision(phase, to_bet)
                    else:
                        data = self._players[i].play(to_bet)
                    if data[0] == 1:
                        print(f'{self._players[i].name} folded')
                        self._folded[i] = True
                        self._calls[i] = True
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
                    k += 1
                else:
                    i = (i + 1) % len(self._players)
                    k += 1
                    continue

    def first_phase(self):
        print('Cards dealt.')
        print('Lets get the bidding started')
        for player in self._players:
            player.add_cards([self._deck.pop(), self._deck.pop()])
        print('Your cards:')
        self._players[0].print_cards()
        print()
        for player in self._players:
            self._calls.append(False)
            self._bets.append(0)
            self._folded.append(False)
        self._bets[self._small_blind] = 50
        self._players[self._small_blind].call(50)
        self._bets[self._big_blind] = 100
        self._players[self._big_blind].call(100)
        self._max_bet = 100
        self._pot = 150
        if self.bidding(1) == 'END':
            return 'END'
        print('End of bidding phase')
        print(25*'-')

    def flop(self):
        print('Flop')
        print('Your cards:')
        self._players[0].print_cards()
        self._cards_on_table = [
            self._deck.pop(),
            self._deck.pop(),
            self._deck.pop()
        ]
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        print()
        for player in self._players:
            player.add_cards(self._cards_on_table)
        print()
        if self.bidding(2) == 'END':
            return 'END'
        print('End of flop phase')
        print(25*'-')

    def river(self):
        print('River')
        print('Your cards:')
        self._players[0].print_cards()
        print()
        river_card = self._deck.pop()
        self._cards_on_table.append(river_card)
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        print()
        for player in self._players:
            player.add_cards([river_card])
        if self.bidding(3) == 'END':
            return 'END'
        print('End of river phase')
        print(25*'-')

    def turn(self):
        print('Turn')
        print('Your cards:')
        self._players[0].print_cards()
        turn_card = self._deck.pop()
        self._cards_on_table.append(turn_card)
        print()
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        print()
        for player in self._players:
            player.add_cards([turn_card])
        if self.bidding(4) == 'END':
            return 'END'
        print('End of turn phase')
        print(25*'-')

    def who_wins(self):
        self._scores = []
        for player in self._players:
            points, color = player.points()
            self._scores.append((points, color, player))
        self._scores = sorted(self._scores, key=lambda x: x[0], reverse=True)
        if self._scores[0][0] > self._scores[1][0]:
            self._scores[0][2].add_chips(self._pot)
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
            winner.add_chips(self._pot)
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
                print('2: Play new deal')
                if input("Choose option: ") == '1':
                    print(f'Your winnings is {self._player.chips}')
                    return self._player.chips
            rund += 1
            dealer = (dealer + 1) % len(self._players)


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
    shuffle(deck)
    return deck


def score(players_cards):
    """
    returns score of given cards
    """
    score = 0
    cards = []
    for card in players_cards:
        cards.append((card.suit, card.rank))
    cards
    ranks = [0 for i in range(2, 17)]
    suits = [0 for i in range(1, 6)]
    cards_sorted_by_rank = sorted(cards, key=lambda x: x[1], reverse=True)
    counter1 = 0
    for i in range(1, len(cards_sorted_by_rank)):
        if cards_sorted_by_rank[i][1] + 1 == cards_sorted_by_rank[i-1][1]:
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
    for i in range(1, 4):
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


deck = create_deck()
game = Game(3, 'Stefan')
game.play()
