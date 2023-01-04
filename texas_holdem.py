from classes import Game


def main():
    """
    Expecting User to input name and numbers of players.
    Prints needed interface.
    Creates instance of Game.
    Calls out game.play method.
    """
    print("Wlcome to Poker Texas Hold'em")
    print(45*'-')
    name = input('Enter your name: ')
    while True:
        num_of_players = input('Enter number of oponents(from 1 to 10): ')
        try:
            num_of_players = int(num_of_players)
        except Exception:
            print('Number of oponents has to be a number!!')
            print()
            continue
        print()
        if num_of_players >= 1 and num_of_players <= 10:
            game = Game(num_of_players, name)
            game.play()
            break
        else:
            print('Number of oponents has to to be in range <1, 10>!!')
            print()
            continue


if '__main__':
    main()
