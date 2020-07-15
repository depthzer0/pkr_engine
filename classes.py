'''
classes
'''

import random
import numpy as np


class Table:

    def __init__(self, amount, stack, blind):

        self.amount = amount  # ammount players
        self.blind = blind  # size of bet
        self.players = [Player('P' + str(i), stack)
                        for i in range(1, amount + 1)]
        self.desk = Desk()
        self.cards = []
        self.bank = 0
        self.botton = -1
        self.point = -1
        self.rules = Rules()

    def __str__(self):

        view = ''

        for i, p in enumerate(self.players):
            view += p.name + [': ', ':*'][i == self.botton] + \
                ' '.join([self.desk.get_card_name(c) for c in p.hand]) + \
                '\t' + str(p.rate) + '\t' + self.desk.ranks[p.high_hand] + \
                '\t' + self.rules.combinations[p.set] + \
                '\t\t' + ' '.join([self.desk.get_card_name(c) for c in p.sets_content]) + '\n'

        if self.cards:
            view += 'cards: ' + \
                ' '.join([self.desk.get_card_name(c) for c in self.cards])

        return view

    def pre_flop(self):

        self.desk.hang_desk()

        for i in range(self.amount * 2):
            self.players[i % self.amount].take_card(self.desk.deal_card())

        for i in range(self.amount):
            self.players[i].hand.sort(key=lambda i: i[1])

            self.players[i].high_hand = self.desk.get_high_card(
                self.players[i].hand)
            self.players[i].set, self.players[i].sets_content = self.rules.get_sets(
                self.players[i].hand, self.cards)

        self.botton = (self.botton + 1) % self.amount

        for i in range(2):
            self.players[(self.botton + 1 + i) %
                         self.amount].do_rate(int(self.blind / 2 ** (1 - i)))

        self.point = (self.botton + 3) % self.amount

    def flop(self):

        self.cards = [self.desk.deal_card() for _ in range(3)]

        for i in range(self.amount):
            self.players[i].set, self.players[i].sets_content = self.rules.get_sets(
                self.players[i].hand, self.cards)

    def turn_river(self):

        self.cards.append(self.desk.deal_card())

        for i in range(self.amount):
            self.players[i].set, self.players[i].sets_content = self.rules.get_sets(
                self.players[i].hand, self.cards)


class Desk:

    def __init__(self):

        self.suits = ('C', 'D', 'P', 'H')
        self.ranks = ('2', '3', '4', '5', '6', '7', '8',
                      '9', 'T', 'J', 'Q', 'K', 'A')

        self.cards = [(s, r) for s in range(len(self.suits))
                      for r in range(len(self.ranks))]

    def __str__(self):

        return ' '.join([self.get_card_name(c) for c in self.cards])

    def get_card_name(self, card):

        return self.suits[card[0]] + self.ranks[card[1]]

    def hang_desk(self):

        self.cards = [(s, r) for s in range(len(self.suits))
                      for r in range(len(self.ranks))]

        random.shuffle(self.cards)

    def deal_card(self):

        return self.cards.pop()

    def get_high_card(self, cards):

        rank = -1
        for i in cards:
            rank = i[1] if i[1] > rank else rank

        return rank


class Player:

    def __init__(self, name, stack):

        self.name = name  # Players name
        self.stack = stack  # money
        self.hand = []  # cards
        self.rate = 0  # bet
        self.high_hand = -1
        self.set = -1
        self.sets_content = []

    def take_card(self, card):

        self.hand.append(card)

    def do_rate(self, rate):

        self.stack -= rate
        self.rate += rate


class Rules:

    def __init__(self):

        self.combinations = ('HighHand', 'OnePair', 'TwoPairs', 'ThreeKind', 'Straight',
                             'Flush', 'FullHouse', 'FourKind', 'StraightFlush', 'RoyalFlush')

    def get_sets(self, hand, board):

        cards = hand + board

        sets_kind = 0
        sets_content = []

        cards.sort()  # sort by suit
        cards.sort(key=lambda i: i[1])  # sort by rank

        flush = {i: [] for i in reversed(range(4))}
        kind = {i: [] for i in reversed(range(13))}
        straight = []

        for card in cards:

            flush[card[0]].append(card)
            kind[card[1]].append(card)

            diff = -1
            if straight:
                diff = card[1] - straight[-1][1]
            if diff > 1 and len(straight) < 5:
                straight.clear()
                straight.append(card)
            elif diff in (-1, 1):
                straight.append(card)
        
        flush_items = sorted(flush, key=lambda x: len(flush[x]), reverse=True)
        kind_items = sorted(kind, key=lambda x: len(kind[x]), reverse=True)

        max_flush = flush[flush_items[0]]
        kind_one = kind[kind_items[0]]
        kind_two = kind[kind_items[1]]

        straight_flush = sorted(list(set(straight)&set(max_flush)), key=lambda i: i[1])

        # 'RoyalFlush'
        if len(straight) >= 5 and len(max_flush) >= 5 and straight[-1][1] == 12:
            sets_kind = 9
            sets_content = straight
        # 'StraightFlush'
        elif len(straight) >= 5 and len(max_flush) >= 5:
            sets_kind = 8
            sets_content = straight
        # 'FourKind'
        elif len(kind_one) == 4:
            sets_kind = 7
            sets_content = kind_one
        # 'FullHouse'
        elif len(kind_one) == 3 and len(kind_two) == 2:
            sets_kind = 6
            sets_content = kind_one + kind_two
        # 'Flush'
        elif len(max_flush) >= 5:
            sets_kind = 5
            sets_content = max_flush[-5:]
        # 'Straight'
        elif len(straight) >= 5:
            sets_kind = 4
            sets_content = straight[-5:]
        # 'ThreeKind'
        elif len(kind_one) == 3:
            sets_kind = 3
            sets_content = kind_one
        # 'TwoPairs'
        elif len(kind_one) == 2 and len(kind_two) == 2:
            sets_kind = 2
            sets_content = kind_one + kind_two
        # 'OnePair'
        elif len(kind_one) == 2:
            sets_kind = 1
            sets_content = kind_one
        # 'HighHand'
        elif len(kind_one) == 1:
            sets_content = hand[-1:]

        sets_content.sort()  # sort by suit
        sets_content.sort(key=lambda i: i[1])  # sort by rank

        return sets_kind, sets_content
