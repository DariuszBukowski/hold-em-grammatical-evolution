import sys
import evol
import grammar
import pickle

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

def test_pop(filename):
    pop = []
    with open(filename, 'rb') as f:
        pop = pickle.load(f)
    #pick the best representative
    while len(pop) > 1:
        pop = evol.tourney(pop)
        
    c1 = make_caller()
    c2 = pop[0]
    
    G = twoPlayersGame.game()
    G.text_output = True
    G.addPlayer(c1)
    G.addPlayer(c2)
    print(G.run())
        
    
    

if __name__ == "__main__":
    test_pop("end_result_final_final_gen1604")
    