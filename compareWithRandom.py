import numpy as np
import random
import copy
import math
import grammar
import operator
import twoPlayersGame
import pickle
import evol

def main():
    with open("end_result", 'rb') as f:
        population = pickle.load(f)
    print("read from file")
    while len(population) > 1:
        population = evol.tourney(population)
    print("chosen the best one") 
    c1 = grammar.population_member()
    c1.construct()
    c2 = population[0]
    G = twoPlayersGame.game()
    G.text_output = True
    G.addPlayer(c1)
    G.addPlayer(c2)
    print(G.run())

if __name__ == "__main__":
    main()
