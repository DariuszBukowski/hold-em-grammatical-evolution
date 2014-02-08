import sys
import evol

def main():
    pop = evol.algorithm_fresh(50, 3, 0.1, "end_result")
    while len(pop) > 1:
        pop = evol.tourney(pop)
    print(pop[0].rule[0].text())
    print(pop[0].rule[1].text())
    print(pop[0].rule[2].text())
    print(pop[0].rule[3].text())

if __name__ == "__main__":
    main()
    