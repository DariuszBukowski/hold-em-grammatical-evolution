import numpy as np
import random
import copy
import math
import grammar
import operator
import twoPlayersGame
import pickle

def cross_over_all(c1, c2):
    c1n = copy.deepcopy(c1)
    c2n = copy.deepcopy(c2)
    
    
    for i in range(4):
        crs = random.randint(1, min(len(c1n.chr[i].string), len(c2n.chr[i].string)-1))
        c1n.chr[i].string = c1.chr[i].string[:crs] + c2.chr[i].string[crs:]
        c2n.chr[i].string = c2.chr[i].string[:crs] + c1.chr[i].string[crs:]
    
    c1n.construct()
    c2n.construct()
    
    return (c1n,c2n)

def cross_over_one(c1, c2, i):
    c1n = copy.deepcopy(c1)
    c2n = copy.deepcopy(c2)
    
    crs = random.randint(1, min(len(c1n.chr[i].string), len(c2n.chr[i].string)-1))
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
                char = str(1 - int(c.chr[i].string[j]))
                cn.chr[i].string = cn.chr[i].string[:j] + char + cn.chr[i].string[(j+1):]
    
    return cn
                
def tourney(population):
    random.shuffle(population)
    winners = []
    i = 0
    while i < len(population) - 1:
        c1 = population[i]
        c2 = population[i+1]
        G = twoPlayersGame.game()
        G.addPlayer(c1)
        G.addPlayer(c2)
        if G.run():
            winners.append(c2)
        else:
            winners.append(c1)
        i += 2
    return winners
    

def apply_operators(population, mutation_p):
    mut_population = []
    for c in population:
        mut_population.append(mutate(c, mutation_p))
    
    child_population = []
    i = 0
    while i < len(population) - 1:
        c1 = population[i]
        c2 = population[i+1]
        
        c3, c4 = cross_over_all(c1, c2)
        child_population.append(c3)
        child_population.append(c4)
        
        c3, c4 = cross_over_one(c1, c2, 0)
        child_population.append(c3)
        child_population.append(c4)
        
        c3, c4 = cross_over_one(c1, c2, 1)
        child_population.append(c3)
        child_population.append(c4)
        
        c3, c4 = cross_over_one(c1, c2, 2)
        child_population.append(c3)
        child_population.append(c4)
        
        c3, c4 = cross_over_one(c1, c2, 3)
        child_population.append(c3)
        child_population.append(c4)
        
        i += 2
    
    #mut_child_population = []
    #for c in child_population:
        #mut_child_population.append(mutate(c, mutation_p))
    
    population.extend(mut_population)
    population.extend(child_population)
    population.extend(mut_child_population)
    return population


def algorithm_file(starting_filename, iters, mutation_p):
    
    population = []
    with open(starting_filename, 'rb') as f:
        population = pickle.load(f)
    
    pop_size = len(population)
    
    for it in range(iters):
        
        print("Starting iteration",it)
        
        #perform crossovers and mutations
        population = apply_operators(population, mutation_p)
        
        print("Generation complete, starting tourney.")
        
        while len(population) > pop_size:
            population = tourney(population)
        
        print("Iteration",it,"done.")
        
        #with open(starting_filename+"_gen"+str(it), 'wb') as f:
            #pickle.dump(population, f, pickle.HIGHEST_PROTOCOL)
    
    with open(starting_filename+"_final", 'wb') as f:
        pickle.dump(population, f, pickle.HIGHEST_PROTOCOL)
    
    return population

def algorithm(population, iters, mutation_p, output_filename=None):
    
    pop_size = len(population)
    
    for it in range(iters):
        
        print("Starting iteration",it)
        
        #perform crossovers and mutations
        population = apply_operators(population, mutation_p)
        
        print("Generation complete, starting tourney.")
        
        while len(population) > pop_size:
            population = tourney(population)
        
        print("Iteration",it,"done.")
    
    if output_filename:
        with open(output_filename, 'wb') as f:
            pickle.dump(population, f, pickle.HIGHEST_PROTOCOL)
    
    return population

def algorithm_fresh(pop_size, iters, mutation_p, output_filename=None):
    population = []
    for i in range(pop_size):
        c = grammar.population_member()
        c.construct()
        population.append(c)
    
    for it in range(iters):
        
        print("Starting iteration",it)
        
        #perform crossovers and mutations
        population = apply_operators(population, mutation_p)
        
        print("Generation complete, starting tourney.")
        
        while len(population) > pop_size:
            population = tourney(population)
        
        print("Iteration",it,"done.")
        
    if output_filename:
        with open(output_filename, 'wb') as f:
            pickle.dump(population, f, pickle.HIGHEST_PROTOCOL)
    
    return population
        