from random import shuffle, randint


class NegativeValueError(Exception):
    def __init__(self, value):
        super().__init__("Value can not be nagative")
        self.value = value


class OutOfRangeError(Exception):
    def __init__(self,):
        super().__init__('Value is out of range')


class Player:
    """
    Class Player. Contains attributes:
    :param chips: player's chips, set to 10000
    :type chips: int

    :param cards: player's cards, set to empty list
    :type lives: list

    """
    def __init__(self):
        self._chips = 10000
        self._cards = []

    @property
    def id(self):
        """
        Player's id getter.
        """
        return self._id

    @property
    def name(self):
        """
        Player's name getter.
        """
        return self._name

    @property
    def chips(self):
        """
        Player's chips getter.
        """
        return self._chips

    def add_chips(self, achips):
        """
        Adds new chips to player's chips.
        """
        if achips < 0:
            raise NegativeValueError(achips)
        else:
            self._chips += achips

    def add_cards(self, cards):
        """
        Adds new list of cards to player's cards.
        """
        self._cards += cards

    @property
    def cards(self):
        """
        Player's cards getter.
        """
        return self._cards

    def call(self, min_bet):
        """
        Enable Player to call by:
        - reducing player's chips by given amount
        - returning information that player called
        """
        self._chips -= min_bet
        return (2, min_bet)

    def fold(self):
        """
        Enable Player to fold
        Returns information that player folded
        """
        return (1, 0)

    def points(self):
        """
        Counts score of player's cards.
        """
        return score(self.cards)

    def print_cards(self):
        """
        Prints player's cards.
        """
        print(self.cards[0])
        print(self.cards[1])


class ComputerPlayer(Player):
    """
    class ComputerPlayer. Inheritance class Player. Contains attributes:
    :param name: player's name, set 'Computer{id}'
    :type name: str

    :param id: player's id
    :type id: int
    """
    def __init__(self, id):
        super().__init__()
        if id < 0:
            raise NegativeValueError(id)
        else:
            self._name = f'Computer{id}'
        self._id = id

    def raisee(self, min_bet, phase):
        """
        Enables Player to raise by:
        - reducing player's chips by given amount
        - deciding how much player bet based on phase of the game
        - returning information that player raised anf how much
        """
        if phase not in [1, 2, 3, 4]:
            raise OutOfRangeError
        else:
            self._chips -= min_bet
            if phase == 1:
                to_rand = (self.chips / 10) // 50
            elif phase == 2:
                to_rand = (self.chips / 7) // 50
            elif phase == 3:
                to_rand = (self.chips / 5) // 50
            elif phase == 4:
                to_rand = self.chips // 50
            bet = randint(1, to_rand) * 50
            self._chips -= bet
            return (3, bet+min_bet)

    def make_decision(self, phase, min_bet, bet, called):
        """
        Makes dacision whether Computer player should:
        - raise
        - call
        - fold
        based on phase of the game and player's bet in current game
        """
        points, color = self.points()
        if phase == 1:
            if (
                (
                    min_bet > self.chips / 10 and
                    points >= 8 and
                    min_bet < self.chips
                ) or (
                    points >= 8 and
                    min_bet < self.chips and
                    bet > 2000
                ) or (
                    points < 8 and
                    min_bet < self.chips and
                    called
                )
            ):
                ans = self.call(min_bet)
            elif (
                min_bet < self.chips / 10 and
                points >= 8 and
                min_bet < 2 * self.chips
            ):
                ans = self.raisee(min_bet, phase)
            else:
                ans = self.fold()
        elif phase == 2:
            if (
                (
                    min_bet > self.chips / 7 and
                    points >= 20 and
                    min_bet < self.chips
                ) or (
                    points >= 20 and
                    min_bet < self.chips and
                    bet > 4000
                ) or (
                    points < 20 and
                    min_bet < self.chips and
                    called
                )
            ):
                ans = self.call(min_bet)
            elif min_bet < self.chips / 7 and points >= 20:
                ans = self.raisee(min_bet, phase)
            else:
                ans = self.fold()
        elif phase == 3:
            if (
                (
                    min_bet > self.chips / 5 and
                    points >= 70 and
                    min_bet < self.chips
                ) or (
                    points >= 70 and
                    min_bet < self.chips and
                    bet > 5000
                ) or (
                    points < 70 and
                    min_bet < self.chips and
                    called
                )
            ):
                ans = self.call(min_bet)
            elif min_bet < self.chips / 5 and points >= 70:
                ans = self.raisee(min_bet, phase)
            else:
                ans = self.fold()
        elif phase == 4:
            if min_bet <= self.chips and points > 1000:
                ans = self.raisee(min_bet, phase)
            elif min_bet <= self.chips and points > 130:
                ans = self.call(min_bet)
            else:
                ans = self.fold()
        return ans


class HumanPlayer(Player):
    """
    class HumanPlayer. Inheritance class Player. Contains attributes:
    :param name: player's name
    :type name: str

    :param id: player's id, set to 0
    :type id: int
    """
    def __init__(self, name='Player'):
        super().__init__()
        self._id = 0
        self._name = name

    def p_raise(self, bet):
        """
        Enables Player to raise by:
        - reducing player's chips by given amount
        - returning information that player raised anf how much
        """
        if bet < 0:
            raise NegativeValueError(bet)
        elif bet > self.chips:
            raise OutOfRangeError
        else:
            self._chips -= bet
        return (3, bet)

    def play(self, to_bet):
        """
        Enables Player to decide whether she/he want to:
        - raise
        - call
        - fold
        """
        print(f'Your money: {self.chips}')
        print()
        print('Options:')
        print(f'1: raise(over {to_bet}, multiple of 50)')
        print(f'2: call({to_bet})')
        print('3: fold')
        while True:
            while True:
                inp = input('Choose option: ')
                try:
                    inp = int(inp)
                except ValueError:
                    print('Selected option must be a number')
                    print()
                    continue
                break
            if inp == 1:
                while True:
                    amount = input('Your bet: ')
                    try:
                        amount = int(amount)
                    except ValueError:
                        print('Bet has to a number!!')
                        print()
                        continue
                    if amount <= to_bet:
                        first_part = 'Your bet is too low!!'
                        second_part = f'Bet needs to be at least {to_bet+50}.'
                        print(f'{first_part} {second_part}')
                        print()
                        continue
                    elif amount % 50 != 0:
                        print('Your bet is not a multiple of 50')
                        print()
                        continue
                    else:
                        break
                ans = self.p_raise(amount)
                print()
            elif inp == 2:
                ans = self.call(to_bet)
            elif inp == 3:
                ans = self.fold()
            else:
                print("Selected option does not exist!!")
                print()
                continue
            break
        return ans


class Card:
    """
    class Card. Contains attributes:
    :param suit: player's suit
    :type suit: int

    :param rank: player's rank
    :type rank: int
    """
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
        """
        Card's suit getter.
        """
        return self._suit

    @property
    def rank(self):
        """
        Card's rank getter.
        """
        return self._rank

    def __str__(self) -> str:
        """
        Returns basic description of Card.
        """
        return f'{self.ranks[self.rank]} of {self.suits[self.suit]}'


class Table:
    """
    Class Player. Contains attributes:
    :param players: list of players at the table
    :type players: list of Players

    :param dealer: indicator of dealer at the player
    :type dealer: int

    :param pot: table's pot
    :type pot: int

    :param calls: list of players who called
    :type calls: list

    :param bets: list of players bets
    :type bets: list

    :param deck: table's deck. Set by functions crate deck()
    :type deck: list of cards

    :param folded: list of players who folded
    :type folded: list

    :param big blind: indicator of big blind at the table
    :type big blind: int

    :param small blind: indicator of small blind at the table
    :type small blind: int
    """
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
        self._big_blind = (dealer+2) % len(self._players)
        self._small_blind = (dealer+1) % len(self._players)
        """
        Sets cards to empty list for each player at the table.
        """
        for player in self._players:
            player._cards = []

    @property
    def players(self):
        return self._players

    def potential_end(self):
        """
        Checks if n-1 of n players folded.
        Returns bool
        """
        counter = 0
        for element in self._folded:
            if element is False:
                counter += 1
        if counter <= 1:
            return True
        else:
            return False

    def everyone_called(self):
        """
        Checks if n-1 of n players folded.
        Returns bool
        """
        counter = 0
        for player in self._calls:
            if player is False:
                counter += 1
        if counter <= 1:
            return True
        else:
            return False

    def bidding(self, phase):
        """
        Bidding
        For each player sets calls on True if player folded, or False if not
        Untill method everyone_calles returns True betting continues
        If potential end returns True:
        - print Winner and gives him pot
        - breaks the game
        If it is first phase starts bidding from player next to Big Blind
        In another case starts from small blind
        Enable for each player to make decision:
        - if it is a computer calls out player.make_smart_decison mathod
        - if it is human calls out player.play method
        - this methods returns info what players did
            - 1 player folded
                - sets folds and calls on True for player
            - 2 player called
                - sets called od True for player
                - add his bet to bets and to pot
            - 3 player raised
                - add his bet to bets and to pot
        Checks if it is not end of the game in important moments
        - if it is print winner and gives him pot breaks loop and end game
        """
        for player in self._players:
            if self._folded[player.id]:
                self._calls[player.id] = True
            else:
                self._calls[player.id] = False
        while self.everyone_called() is False:
            if self.potential_end() is True:
                for index in range(0, len(self._players)):
                    if self._folded[index] is False:
                        print()
                        print(f'{self._players[index].name} won {self._pot}!!')
                        print('Winner cards:')
                        self._players[index].print_cards()
                        self._players[index].add_chips(self._pot)
                        print(45*'-')
                        print(45*'-')
                return 'END'
            if phase == 1:
                start = (self._big_blind + 1) % len(self._players)
            else:
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
                        called = self.everyone_called()
                        data = self._players[i].make_decision(
                            phase,
                            to_bet,
                            self._bets[i] + to_bet,
                            called
                            )
                    else:
                        print()
                        print(f'Current pot: {self._pot}')
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
            if self.potential_end() is True:
                for index in range(0, len(self._players)):
                    if self._folded[index] is False:
                        print()
                        print(f'{self._players[index].name} won {self._pot}!!')
                        print('Winner cards:')
                        self._players[index].print_cards()
                        print(45*'-')
                        print(45*'-')
                        self._players[index].add_chips(self._pot)
                return 'END'

    def first_phase(self):
        """
        First phase of play.
        For each players gives two cards.
        For each players sets:
        - calls to False
        - bets to 0
        - folded to false
        Makes big and small blids bet 100 and 50 chips.
        Update max bet and pot by blinds.
        Prints needed interface.
        """
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
        print(f'{self._players[self._small_blind].name} is small blind')
        self._bets[self._big_blind] = 100
        self._players[self._big_blind].call(100)
        print(f'{self._players[self._big_blind].name} is big blind')
        self._max_bet = 100
        self._pot = 150
        if self.bidding(1) == 'END':
            return 'END'
        print('End of bidding phase')
        print(45*'-')

    def flop(self):
        """
        Second phase of play(flop).
        Puts 3 cards on the table
        For each players adds cards from table which is needed to count score.
        Prints needed interface.
        """
        print('Flop')
        print('Your cards:')
        self._players[0].print_cards()
        self._cards_on_table = [
            self._deck.pop(),
            self._deck.pop(),
            self._deck.pop()
        ]
        print()
        print("Cards on the table:")
        for card in self._cards_on_table:
            print(card)
        for player in self._players:
            player.add_cards(self._cards_on_table)
        print()
        if self.bidding(2) == 'END':
            return 'END'
        print('End of flop phase')
        print(45*'-')

    def river(self):
        """
        Third phase of play(river).
        Puts 1 card on the table
        For each players adds card from table which is needed to count score.
        Prints needed interface.
        """
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
        print(45*'-')

    def turn(self):
        """
        Fourth phase of play(turn).
        Puts 1 card on the table
        For each players adds card from table which is needed to count score.
        Prints needed interface.
        """
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
        print(45*'-')

    def who_wins(self):
        """
        Counts score for ech one.
        Sorts scores.
        Decides which Player won the game.
        If there are more then one player with the highest score
        points the winner by dicinding wich color is higher
        Add pot to winners chips
        Prints needed interface
        """
        self._scores = []
        for player in self._players:
            if not self._folded[player.id]:
                points, color = player.points()
                self._scores.append((points, color, player))
        self._scores = sorted(self._scores, key=lambda x: x[0], reverse=True)
        if len(self._scores) == 1:
            winner = self._scores[0][2]
            winner.add_chips(self._pot)
            print()
            print(f'{winner.name} won {self._pot}!!')
            print('Winner cards:')
            winner.print_cards()
            print(45*'-')
            print(45*'-')
        elif self._scores[0][0] > self._scores[1][0]:
            winner = self._scores[0][2]
            winner.add_chips(self._pot)
            print()
            print(f'{winner.name} won {self._pot}!!')
            print('Winner cards:')
            winner.print_cards()
            print(45*'-')
            print(45*'-')
        else:
            win_score = self._scores[0][1]
            winner = self._scores[0][2]
            for i in range(1, len(self._scores)):
                if self._scores[i][0] == self._scores[i-1][0]:
                    if self._scores[i][1] > win_score:
                        winner = self._scores[i][2]
                        win_score = self._scores[i][1]
                else:
                    break
            winner.add_chips(self._pot)
            print()
            print(f'{winner.name} won {self._pot}!!')
            print('Winner cards:')
            winner.print_cards()
            print(45*'-')
            print(45*'-')
        return winner

    def play_table(self):
        """"
        Calls out following methods to play the game.
        """
        if self.first_phase() != 'END':
            if self.flop() != 'END':
                if self.river() != 'END':
                    if self.turn() != 'END':
                        self.who_wins()


class Game:
    """
    Class Game. Contains attributes:
    :param num_of_players: number of computer players
    :type num_of_players: int

    :param player_name: human player's name
    :type player_name: str

    :param players: list of players in the game
    :type players: list of Players

    :param player: human player
    :type player: HumanPlayer
    """
    def __init__(self, num_of_players, player_name):
        self._num_of_players = num_of_players
        self._players = []
        """
        Creates Human Player and num_of_players Computer Players.
        Adds them to list of players.
        """
        self._player = HumanPlayer(player_name)
        self._players.append(self._player)
        for i in range(1, self._num_of_players+1):
            computer = ComputerPlayer(i)
            self._players.append(computer)

    def play(self):
        """
        Draws dealer.
        Creates instance of class Table.
        Call out table.paly method.
        If any of Coputer Player is bankrupt raplaces him.
        Prints needed interface.
        After each rund swiches dealer to next player.
        """
        dealer = randint(0, self._num_of_players)
        rund = 1
        while True:
            table = Table(dealer, self._players)
            table.play_table()
            for player in self._players:
                if player.chips <= 100 and player != self._player:
                    print(f'{player.name} replaced')
                    player.add_chips(10000)
            if self._player.chips == 0:
                print("Unfortunately You've lost")
                print(25*'-')
                print()
            else:
                while True:
                    print("Options:")
                    print(f"1: Go away with {self._player.chips}")
                    print('2: Play new deal')
                    choice = input("Choose option: ")
                    if choice == '1':
                        print(f'Your winnings is {self._player.chips}')
                        if rund == 1:
                            string_end = 'rund'
                        else:
                            string_end = 'runds'
                        print(f"You've played {rund} {string_end}")
                        return self._player.chips
                    elif choice == '2':
                        rund += 1
                        print(25*'-')
                        print()
                        break
                    else:
                        print("Selected option does not exist!!")
                        print()
                        continue
            dealer = (dealer + 1) % len(self._players)


def create_deck():
    deck = []
    """
    Function creates deck of Cards
    Shuffle it
    Returns list of Cards

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
    Searchs for:
    - high card
    - pair
    - two pairs
    - three of kind
    - straight
    - flush
    - full house
    - four of kind
    - straight flush
    - royal flush
    Returns score according to score.excl and color of the best score.
    """
    score = 0
    cards = []
    for card in players_cards:
        cards.append((card.suit, card.rank))
    ranks = [0 for i in range(2, 17)]
    suits = [0 for i in range(1, 6)]
    cards_sorted_by_rank = sorted(cards, key=lambda x: x[1], reverse=True)
    counter1 = 0
    for i in range(1, len(cards_sorted_by_rank)):
        if cards_sorted_by_rank[i][1] + 1 == cards_sorted_by_rank[i-1][1]:
            counter1 += 1
            first1 = cards_sorted_by_rank[i]
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
                first = chance_for_poker[i]
            else:
                counter = 0
        if counter >= 5:
            score = 150000000 + first
        else:
            score = chance_for_poker[0] * 100000
    elif counter1 >= 5:
        score = first1 * 10000
    return (score, score_color)
