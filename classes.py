import random


class Table:

    def __init__(self, amount):
        self.amount = amount


class Desk:

    def __init__(self):

        self.suits = ('C', 'D', 'P', 'H')
        self.ranks = ('2', '3', '4', '5', '6', '7', '8',
                      '9', '10', 'V', 'Q', 'K', 'A')

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
