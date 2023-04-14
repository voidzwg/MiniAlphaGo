#!/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-
# main.py

if __name__ == '__main__':
    from game import Game
    from players import HumanPlayer, AIPlayer, RandomPlayer
    
    black_player =  HumanPlayer("X")
    # black_player = RandomPlayer("X")
    white_player = AIPlayer("O")
    game = Game(black_player, white_player)
    game.run()
