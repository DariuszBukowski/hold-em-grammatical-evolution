import sys
import evol
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
    
    return caller

def test_pop(filename):
    pop = []
    with open(filename, 'rb') as f:
        pop = pickle.load(f)
    #pick the best representative
    while len(pop) > 1:
        pop = evol.tourney(pop)
        
    c = make_caller()
        
    
    

if __name__ == "__main__":
    test_pop("insert filename here")
    