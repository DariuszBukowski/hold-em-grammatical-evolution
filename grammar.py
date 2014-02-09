# -*- coding: utf-8 -*-
import numpy as np
import random
import math

class population_member:
    def __init__(self):
        self.chr = [None, None, None, None]
        self.rule = [None, None, None, None]
        for i in range(4):
            self.chr[i] = chromosome()
        self.init_chr0()
        self.init_chr_random(1)
        self.init_chr_random(2)
        self.init_chr_random(3)
        
        
    def construct(self):
        for i in range(4):
            self.chr[i].reset()
            self.rule[i] = g_expr()
            self.rule[i].construct(self.chr[i])
    
    def evaluate(self, game, i): #i - round of betting
        return self.rule[i].eval(game)
    
    def init_chr0(self):
        self.chr[0].string = "0000" #cond
        
        
        self.chr[0].add(3) #hand
        self.chr[0].add(0) #better than
        self.chr[0].add(random.randint(0,1)) #high card or pair
        self.chr[0].add(random.randint(0,12)) #random card value
        
        
        self.chr[0].add(0) #if true then cond
        self.chr[0].add(4) #pot
        self.chr[0].add(0) #less than _?
        
        self.chr[0].add(0) # _ _?
        self.chr[0].add(5) # 5 _?
        self.chr[0].add(1) # 5 _
        self.chr[0].add(0) # 5 0
        
        self.chr[0].add(1) #if true then action
        self.chr[0].add(1) #raise
        
        self.chr[0].add(1) #else action
        self.chr[0].add(0) #call
        
        
        self.chr[0].add(1) #else action
        self.chr[0].add(2) #fold
    
    def init_chr_random(self, i):
        self.chr[i].string = "0000" #cond
        for j in range(50):
            self.chr[i].add(random.randint(0,15))
            
class chromosome:
    def __init__(self):
        self.string = "00010000" #placeholder value
        self.pos = 0
        self.loops = 0
        self.loop_cap = 10
    
    def read_next_codon(self):
        c = 0
        p = self.pos
        while p < self.pos + 4:
            c *= 2
            c += int(self.string[p])
            p += 1
        self.pos = (self.pos + 4) % len(self.string)
        if self.pos == 0:
            self.loops += 1
        return c
    
    def reset(self):
        self.pos = 0
        self.loops = 0
    
    def add(self, num):
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
        if x%2 == 0 and chr.loops < chr.loop_cap:
            self.t = g_cond()
        else:
            self.t = g_action()
        chr = self.t.construct(chr)
        return chr
    
    def text(self):
        return self.t.text()
        
#<cond> :: if <bool> then <expr> else <expr>
class g_cond:
    def __init__(self):
        self.b = None
        self.e1 = None
        self.e2 = None
    def eval(self, game):
        b = self.b.eval(game)
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
        
    def text(self):
        return "if ( " + self.b.text() + " ) then ( " + self.e1.text() + " ) else ( " + self.e2.text() + " )"
        
#<action> :: call|raise|fold
class g_action:
    def __init__(self):
        self.action_type = None
    def eval(self, game):
        return self.action_type
    def construct(self, chr):
        x = chr.read_next_codon()
        self.action_type = x%3
        return chr
    def text(self):
        if self.action_type == 0:
            return "call"
        elif self.action_type == 1:
            return "raise"
        else:
            return "fold"

#<bool> :: <bool> and <bool>|<bool> or <bool>|<hand>|<pot>|<cash>
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
        self.type = x%5
        
        if self.type < 2 and chr.loops < chr.loop_cap:
            self.b1 = g_bool()
            chr = self.b1.construct(chr)
            self.b2 = g_bool()
            chr = self.b2.construct(chr)
        elif self.type <= 3:
            self.type = 3 #if loop cap is reached, default to type 3 condition
            self.b1 = g_hand()
            chr = self.b1.construct(chr)
        elif self.type == 4:
            self.b1 = g_pot()
            chr = self.b1.construct(chr)
        else:
            self.b1 = g_cash()
            chr = self.b1.construct(chr)

        return chr
    
    def text(self):
        if self.type == 0:
            return "( " + self.b1.text() + " ) and ( " + self.b2.text() + " )"
        elif self.type == 1:
            return "( " + self.b1.text() + " ) or ( " + self.b2.text() + " )"
        else:
            return self.b1.text()
        
#<hand> :: hand better than <hand_value>|hand worse than <hand value>
class g_hand:
    def __init__(self):
        self.better_worse = None
        self.val = None
    def eval(self, game):
        v = self.val.eval(game)
        h = game.get_hand()
        
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
        chr = self.val.construct(chr)
        return chr
    
    def text(self):
        t = ""
        if self.better_worse == 0:
            t = "better"
        else:
            t = "worse"
        return "hand " + t + " than " + self.val.text()
            

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
        return (self.val, c1, c2)
        
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
    
    def text(self):
        hands = ["high","pair","two pairs","three","straight","flush","full house","four","straight flush"]
        text = hands[self.val]
        if (self.c1):
            text = text + " " + self.c1.text()
        if (self.c2):
            text = text + " " + self.c2.text()
        return text
        
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
    
    def text(self):
        if self.val < 9:
            return str(self.val+2)
        elif self.val == 9:
            return "J"
        elif self.val == 10:
            return "Q"
        elif self.val == 11:
            return "K"
        else:
            return "A"
        
#<pot> :: pot less than <intval>|pot more than <intval>
class g_pot:
    def __init__(self):
        self.better_worse = None
        self.val = None
        
    def eval(self, game):
        v = self.val.eval(game)
        p = game.get_pot()
        
        if self.better_worse == 0:
            return p < v
        else:
            return p > v
            
    def construct(self, chr):
        x = chr.read_next_codon()
        self.better_worse = x%2
        
        self.val = g_intval()
        chr = self.val.construct(chr)
        return chr
    
    def text(self):
        t = ""
        if self.better_worse == 0:
            t = "less"
        else:
            t = "more"
        return "pot " + t + " than " + self.val.text()
        

#<cash> :: have less than <intval>|have more than <intval>
class g_cash:
    def __init__(self):
        self.better_worse = None
        self.val = None
        
    def eval(self, game):
        v = self.val.eval(game)
        p = game.get_cash()
        
        if self.better_worse == 0:
            return p < v
        else:
            return p > v
            
    def construct(self, chr):
        x = chr.read_next_codon()
        self.better_worse = x%2
        
        self.val = g_intval()
        chr = self.val.construct(chr)
        return chr
    
    def text(self):
        t = ""
        if self.better_worse == 0:
            t = "less"
        else:
            t = "more"
        return "have " + t + " than " + self.val.text()
    
#<intval> :: <int><intval>|<int>
class g_intval:
    def __init__(self):
        self.int = None
        self.intval = None
    def eval(self, game):
        v = self.int.eval(game)
        if self.intval:
            v = v*10 + self.intval.eval(game)
        return v
    def construct(self, chr):
        x = chr.read_next_codon()
        self.int = g_digit()
        chr = self.int.construct(chr)
        
        if x%2 == 0 and chr.loops < chr.loop_cap:
            self.intval = g_intval()
            chr = self.intval.construct(chr)
        
        return chr
    
    def text(self):
        text = self.int.text()
        if self.intval:
            text = text + self.intval.text()
        return text
        
#<digit> :: 0|1|...|9
class g_digit:
    def __init__(self):
        self.val = None
    def eval(self, game):
        return self.val
    def construct(self, chr):
        x = chr.read_next_codon()
        self.val = x % 10
        return chr
    
    def text(self):
        return str(self.val)