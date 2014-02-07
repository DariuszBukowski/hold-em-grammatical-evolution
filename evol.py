import numpy as np
import random
import copy
import math
import grammar
import operator
import twoPlayersGame

def cross_over_all(c1, c2):
    c1n = copy.deepcopy(c1)
    c2n = copy.deepcopy(c2)
    
    
    for i in range(4):
        crs = random.randint(1, min(len(c1n.chr[i].string), len(c2n.chr[i].string)-1)
        c1n.chr[i].string = c1.chr[i].string[:crs] + c2.chr[i].string[crs:]
        c2n.chr[i].string = c2.chr[i].string[:crs] + c1.chr[i].string[crs:]
    
    c1n.construct()
    c2n.construct()
    
    return (c1n,c2n)

def cross_over_one(c1, c2, i):
    c1n = copy.deepcopy(c1)
    c2n = copy.deepcopy(c2)
    
    crs = random.randint(1, min(len(c1n.chr[i].string), len(c2n.chr[i].string)-1)
    c1n.chr[i].string = c1.chr[i].string[:crs] + c2.chr[i].string[crs:]
    c2n.chr[i].string = c2.chr[i].string[:crs] + c1.chr[i].string[crs:]
    
    c1n.construct()
    c2n.construct()
    
    return (c1n,c2n)
    
def mutate(c, p):
    cn = copy.deepcopy(c)
    
    for i in range(4):
        for j in range(len(c.chr[i].string)):
            if random.random() < p:
                char = str(1 - int(c.chr[i][j]))
                cn.chr[i] = cn.chr[i][:j] + char + cn.chr[i][(j+1):]
    
    return cn
                

def algorithm(pop_size, iters):
    population = []
    for i in range(pop_size):
        population.append(grammar.population_member())
    
    for i in range(iters):
        #evaluate the population
        #select the best-performing members
        #perform crossovers and mutations
        pass
    