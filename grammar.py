import numpy as np
import random
import matplotlib.pyplot as plt
import math

class population_member:
    def __init__(self):
        self.chr = [None, None, None, None]
        self.rule = [None, None, None, None]
        for i in range(4):
            self.chr[i] = chromosome()
        
    def construct(self):
        for i in range(4):
            self.chr[i].pos = 0
            self.rule[i] = g_expr()
            self.rule[i].construct(self.chr[i])
    
    def evaluate(self, game, i): #i - round of betting
        return self.rule[i].eval(game)

class chromosome:
    def __init__(self):
        self.string = "0000" #placeholder value
        self.pos = 0
    
    def read_next_codon(self):
        c = 0
        p = self.pos
        while p < self.pos + 4:
            c *= 2
            c += int(self.string[p])
            p += 1
        self.pos = (self.pos + 4) % len(self.string)
    
    def add(num):
        num = num % 16
        s = num.__format__("b")
        while len(s) < 4:
            s = "0"+s
        self.string = self.string+s
        

#grammar: 

#<expr> :: <cond>|<action>
class g_expr:
    def __init__(self):
        self.t = None
    def eval(self, game):
        return self.t.eval(game)
    def construct(self, chr):
        x = chr.read_next_codon()
        if x%2 == 0:
            self.t = g_cond()
        else:
            self.t = g_action()
        chr = self.t.construct(chr)
        return chr
        
#<cond> :: if <bool> then <expr> else <expr>
class g_cond:
    def __init__(self):
        self.b = None
        self.e1 = None
        self.e2 = None
    def eval(self, game):
        b = self.b.eval()
        if b:
            return self.e1.eval(game)
        else:
            return self.e2.eval(game)
    def construct(self, chr):
        self.b = g_bool()
        chr = self.b.construct(chr)
        self.e1 = g_expr()
        chr = self.e1.construct(chr)
        self.e2 = g_expr()
        chr = self.e2.construct(chr)
        return chr
        
#<action> :: call|raise|fold
class g_action:
    def __init__(self):
        self.action_type = None
    def eval(self, game):
        return self.action_type
    def construct(self, chr):
        x = chr.read_next_codon()
        self.val = x%3
        return chr

#<bool> :: <bool> and <bool>|<bool> or <bool>|<hand>|<pot>
class g_bool:
    def __init__(self):
        self.type = None
        self.b1 = None
        self.b2 = None
    def eval(self, game):
        if self.type == 0:
            return self.b1.eval(game) and self.b2.eval(game)
        elif self.type == 1:
            return self.b1.eval(game) or self.b2.eval(game)
        else:
            return self.b1.eval(game)
    def construct(self, chr):
        x = chr.read_next_codon()
        self.type = x%4
        
        self.val = g_intval()
        chr = self.intval.construct(chr)
        return chr
        
#<hand> :: hand better than <hand_value>|hand worse than <hand value>
class g_hand:
    def __init__(self):
        self.better_worse = None
        self.val = None
    def eval(self, game):
        v = self.val.eval(game)
        h = game.get_hand()#placeholder, gotta get data from the game state somehow
        
        if self.better_worse == 0:
            result = h[0] > v[0]
            if (h[0] == v[0]) and h[1]!=None:
                result = h[1] > v[1]
                if (h[1] == v[1]) and h[2]!=None:
                    result = h[2] > v[2]
            return result
        else:
            result = h[0] < v[0]
            if (h[0] == v[0]) and h[1]!=None:
                result = h[1] < v[1]
                if (h[1] == v[1]) and h[2]!=None:
                    result = h[2] < v[2]
            return result
            
    def construct(self, chr):
        x = chr.read_next_codon()
        self.better_worse = x%2
        
        self.val = g_hand_value()
        chr = self.intval.construct(chr)
        return chr
            

#<hand_value> :: high <card>|pair <card>|two pairs <card> <card>|three <card>|straight <card>|flush|full house <card> <card>|four <card>|straight flush <card>
class g_hand_value:
    def __init__(self):
        self.val = None
        self.c1 = None
        self.c2 = None
        
    def eval(self, game):
        c1 = None
        c2 = None
        if (self.c1):
            c1 = self.c1.eval(game)
        if (self.c2):
            c2 = self.c2.eval(game)
        return (self.val.eval(game), c1, c2)
        
    def construct(self, chr):
        x = chr.read_next_codon()
        self.val = x%9
        if self.val != 5: #not a flush
            self.c1 = g_card()
            chr = self.c1.construct(chr)
            if self.val == 2 or self.val == 6: #two pairs or full house
                self.c2 = g_card()
                chr = self.c2.construct(chr)
        return chr
        
#<card> :: 2|3|4|...|10|J|Q|K|A - 13 card values
class g_card:
    def __init__(self):
        self.val = None
        
    def eval(self, game):
        return self.val
        
    def construct(self, chr):
        x = chr.read_next_codon()
        self.val = x%13
        return chr
        
#<pot> :: pot less than <intval>|pot more than <intval>
class g_pot:
    def __init__(self):
        self.better_worse = None
        self.val = None
        
    def eval(self, game):
        v = self.val.eval(game)
        p = game.get_pot()#placeholder, gotta get data from the game state somehow
        
        if self.better_worse == 0:
            return p < v
        else:
            return p > v
            
    def construct(self, chr):
        x = chr.read_next_codon()
        self.better_worse = x%2
        
        self.val = g_intval()
        chr = self.intval.construct(chr)
        return chr
    
    
#<intval> :: <int><intval>|<int>
class g_intval:
    def __init__(self):
        self.int = None
        self.intval = None
    def eval(self):
        v = self.val
        if self.intval:
            v = v*10 + self.intval.eval()
        return v
    def construct(self, chr):
        x = chr.read_next_codon()
        self.int = g_digit()
        chr = self.int.construct(chr)
        
        if x%2 == 0:
            self.intval = g_intval()
            chr = self.intval.construct(chr)
        
        return chr
        
#<digit> :: 0|1|...|9
class g_digit:
    def __init__(self):
        self.val = None
    def eval(self):
        return self.val
    def construct(self, chr):
        x = chr.read_next_codon()
        self.val = x % 10
        return chr