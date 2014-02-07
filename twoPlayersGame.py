# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import grammar
import functools
import operator

class game:
	def __init__(self):
		self.blindBet = 10
		self.startingCapital = 1000
		self.iterations = 100
		self.pot = 0
		self.currentRound = 0
		self.players = []
		self.playersCapital = []

	def addPlayer(self, player):
		self.players.append(player)
		self.playersCapital.append(self.startingCapital)

	def run(self):
		self.cards = list(range(52)) # numbers from 0 to 51 - cards from 2 to A, clubs, diamonds, hearts, spades
		startingPlayer = 0
		iteration = 0
		while self.playersCapital[0] >= self.blindBet and self.playersCapital[1] >= self.blindBet and iteration < self.iterations:
			random.shuffle(self.cards)
			print('after', iteration, 'iterations', self.playersCapital[0], 'to', self.playersCapital[1])
			self.pot = self.blindBet
			bidDifference = self.blindBet
			alreadyCalled = False
			self.playersCapital[startingPlayer] -= self.blindBet
			startingPlayer ^= 1
			self.currentPlayer = startingPlayer
			self.currentRound = 0
			while True:
				fold = False
				while True:
					action = self.players[self.currentPlayer].evaluate(self, self.currentRound)
					#Current player folds
					if action == 2: 
						print(self.currentPlayer, 'folds')
						self.playersCapital[self.currentPlayer ^ 1] += self.pot
						self.pot = 0
						fold = True
						break
					#Current player can raise
					elif action == 1 and not (self.playersCapital[self.currentPlayer] < 2 * self.blindBet or self.playersCapital[self.currentPlayer ^ 1] < self.blindBet):
						print(self.currentPlayer, 'raises')
						self.playersCapital[self.currentPlayer] -= (self.blindBet + bidDifference)
						self.pot += self.blindBet + bidDifference
						bidDifference = self.blindBet
						self.currentPlayer ^= 1
					#Current player calls
					else: 
						print(self.currentPlayer, 'calls')
						if bidDifference == 0 and not alreadyCalled:
							alreadyCalled = True
							self.currentPlayer ^= 1
							continue
						if bidDifference == 0:
							self.currentPlayer ^= 1
							break
						self.playersCapital[self.currentPlayer] -= self.blindBet
						self.pot += self.blindBet
						self.currentPlayer ^= 1
						break
				alreadyCalled = False
				bidDifference = 0
				if fold:
					break
				elif self.currentRound == 3:
					h1 = self.get_players_hand(0)
					print('which is', h1)
					h2 = self.get_players_hand(1)
					print('which is', h2)
					print('pot was', self.pot)
					if h1 == h2: #split the pot
						self.playersCapital[0] += self.pot / 2
						self.playersCapital[1] += self.pot / 2
					elif h1 < h2:
						self.playersCapital[1] += self.pot
					else:
						self.playersCapital[0] += self.pot
					self.pot = 0
					break
				self.currentRound += 1
			iteration += 1
		if iteration == self.iterations:
			return self.playersCapital[1] > self.playersCapital[0]
		return self.playersCapital[0] < self.blindBet

	def get_players_hand(self, player):
		playersCards = [self.cards[player * 2], self.cards[player * 2 + 1]]
		if self.currentRound > 0:
			playersCards += self.cards[4 : 6 + self.currentRound]
		print(player, 'has', playersCards)
		for i in range(8, -1, -1):
			for j in range(0, 4):
				if functools.reduce(operator.and_, map(lambda x: x in playersCards, range(i + j * 13, i + j * 13 + 5))):
					return (8, i, None) # Straight flush
		suits = list(map(lambda x: x % 13, playersCards))
		for i in range(12, -1, -1):
			if suits.count(i) == 4:
				return (7, i, None) # Four
		for i in range(12, -1, -1):
			for j in range(12, -1, -1):
				if i != j and suits.count(i) >= 3 and suits.count(j) >= 2:
					return (6, i, j) # Full House
		colors = list(map(lambda x: x / 13, playersCards))
		for i in range(0, 4):
			if colors.count(i) >= 5:
				return (5, None, None) # Flush
		for i in range(8, -1, -1):
			if functools.reduce(operator.and_, map(lambda x: x in suits, range(i, i + 5))):
				return (4, i, None) # Straight
		for i in range(12, -1, -1):
			if suits.count(i) == 3:
				return (3, i, None) # Three
		for i in range(12, -1, -1):
			for j in range(i - 1, -1, -1):
				if i != j and suits.count(i) >= 2 and suits.count(j) >= 2:
					return (2, i, j) # Two pairs
		for i in range(12, -1, -1):
			if suits.count(i) == 2:
				return (1, i, None) # Pair
		return (0, max(suits), None) # High card

	def get_hand(self):
		return self.get_players_hand(self.currentPlayer)

	def get_pot(self):
		return self.pot
		
	def get_cash(self):
		return self.playersCapital(self.currentPlayer)
	

	
