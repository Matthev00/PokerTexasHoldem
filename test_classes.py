from classes import Player


def player_test():
    player = Player
    assert player.chips == 0
    assert player.cards == []
