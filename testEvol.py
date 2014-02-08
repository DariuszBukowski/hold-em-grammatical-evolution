import sys
import evol
import twoPlayersGame
import grammar

def main():
    pop = evol.algorithm_fresh(50, 1, 0.1, "end_results")
    while True:
        while len(pop) > 1:
            pop = evol.tourney(pop)
        res = 0.0
        for _ in range(500):
            c1 = grammar.population_member()
            c1.construct()
            c2 = pop[0]
            G = twoPlayersGame.game()
            G.addPlayer(c1)
            G.addPlayer(c2)
            if G.run():
                res += 0.002
        print(res)
        pop = evol.algorithm_file("end_results", 1, 0.1)

if __name__ == "__main__":
    main()
    
