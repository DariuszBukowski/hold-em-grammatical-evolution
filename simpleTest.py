# -*- coding: utf-8 -*-
import sys
import grammar
import twoPlayersGame

def main():
    c1 = grammar.population_member()
    c2 = grammar.population_member()
    c1.construct()
    c2.construct()
    G = twoPlayersGame.game()
    G.addPlayer(c1)
    G.addPlayer(c2)
    G.run()

if __name__ == "__main__":
    main()