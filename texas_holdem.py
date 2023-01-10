from classes import Game
from database import Database


def main():
    """
    Expecting User to input name and numbers of players.
    Prints needed interface.
    Creates instance of Game.
    Calls out game.play method.
    """
    print("Welcome to Poker Texas Hold'em")
    print(45*'-')
    name = input('Enter your name: ')
    while True:
        num_of_players = input('Enter number of oponents(from 1 to 10): ')
        try:
            num_of_players = int(num_of_players)
        except ValueError:
            print('Number of oponents has to be a number!!')
            print()
            continue
        print()
        if num_of_players >= 1 and num_of_players <= 10:
            game = Game(num_of_players, name)
            player = game.play()
            if player.chips > 0:
                database = Database()
                place = database.add_to_ranking((player.name, player.chips))
                print(f'You are {place} in the ranking.')
                print()
                print(45*'-')
                print("Top 5 scores")
                database.print_ranking(5)
            break
        else:
            print('Number of oponents has to to be in range <1, 10>!!')
            print()
            continue


if '__main__':
    main()
