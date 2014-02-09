import sys
import evol
import twoPlayersGame
import grammar

def make_caller():
    caller = grammar.population_member()
    caller.chr[0].string = "0000"
    caller.chr[0].add(4) #pot
    caller.chr[0].add(0) #less than _?
        
    caller.chr[0].add(0) # _ _?
    caller.chr[0].add(5) # 5 _?
    caller.chr[0].add(1) # 5 _
    caller.chr[0].add(0) # 5 0
    
    caller.chr[0].add(1) #if true then action
    caller.chr[0].add(1) #raise
    
    caller.chr[0].add(1) #else action
    caller.chr[0].add(0) #call
    
    caller.chr[1].string = "00010000"
    caller.chr[2].string = "00010000"
    caller.chr[3].string = "00010000"
    
    caller.construct()
    
    return caller

def main():
    pop = evol.algorithm_fresh(50, 1, 0.1, "call_results")
    while True:
        while len(pop) > 1:
            pop = evol.tourney(pop)
        res = 0.0
        for _ in range(500):
            c1 = make_caller()
            c2 = pop[0]
            G = twoPlayersGame.game()
            G.addPlayer(c1)
            G.addPlayer(c2)
            if G.run():
                res += 0.002
        print(res)
        pop = evol.algorithm_file("call_results", 1, 0.1)

if __name__ == "__main__":
    main()
    
