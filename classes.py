import random


class Table:

    def __init__(self, amount, stack, blind):

        self.amount = amount
        self.players = [Player('P' + str(i), stack) for i in range(1, amount + 1)]
        self.desk = Desk()
        self.cards = []
        self.bank = 0
        self.blind = blind
        self.botton = -1

    def __str__(self):

        view = ''

        for p in self.players:
            view += p.name + ': ' + \
                ' '.join([self.desk.get_card_name(c) for c in p.hand]) + '\n'

        if self.cards:
            view += 'cards: ' + ' '.join([self.desk.get_card_name(c) for c in self.cards])

        return view

    def pre_flop(self):

        self.botton = (self.botton + 1) % self.amount

        self.desk.hang_desk()

        for i in range(self.amount * 2):
            self.players[i % self.amount].take_card(self.desk.deal_card())

    def flop(self):

        self.cards = [self.desk.deal_card() for _ in range(3)]

    def turn_river(self):

        self.cards.append(self.desk.deal_card())

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


class Player:

    def __init__(self, name, stack):

        self.name = name
        self.stack = stack
        self.hand = []
        self.rate = 0

    def take_card(self, card):

        self.hand.append(card)