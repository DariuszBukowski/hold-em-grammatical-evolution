import sys
import evol

def main():
    pop = evol.algorithm(50, 10, 0.1)
    pop = evol.tourney(pop)
    pop = evol.tourney(pop)
    pop = evol.tourney(pop)
    print(pop[0].rule[0].text())
    print(pop[0].rule[1].text())
    print(pop[0].rule[2].text())
    print(pop[0].rule[3].text())

if __name__ == "__main__":
    main()
    