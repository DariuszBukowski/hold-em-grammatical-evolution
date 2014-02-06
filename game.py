# -*- coding: utf-8 -*-
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import grammar

class game:
    def __init__(self):
	self.blindBet = 10
	self.startingCapital = 1000
	self.pot = 0
	self.currentRound = 0
	self.players = []
	self.playersCapital = []

    def addPlayer(self, player):
	self.players.append(player)
	self.playersCapital.append(self.startingCapital)

    def run(self):
	self.numberOfPlayers = len(self.players)
	playersLeft = deque(range(0, self.numberOfPlayers))
	cards = range(52)
	while len(playersLeft) > 1:
	    random.shuffle(cards)
	    self.pot = 0
	    self.currentRound = 0
	    playersLeftInRound = deque(playersLeft)
	    self.currentPlayer = playersLeftInRound[0]
	    self.playersCapital[self.currentPlayer] -= self.blindBet
	    while True:
		# TO DO
	    	for _ in range(0, len(playersLeftInRound) - 1):
		    playersLeftInRound.rotate()
		    self.currentPlayer = playersLeftInRound[0]
		    action = self.players[self.currentPlayer].evaluate(self, self.currentRound)
	    
	    
	return playersLeft[0]

    def get_players_hand(self, player):
	playersCards = (cards[player * 2], cards[player * 2 + 1])
	if self.currentRound > 0:
	    playersCards += cards[self.numberOfPlayers * 2 : self.numberOfPlayers * 2 + 2 + self.currentRound]
	#TO DO

    def get_hand(self):
	return self.get_players_hand(self.currentPlayer)

    def get_pot(self):
	return self.pot
	

    
