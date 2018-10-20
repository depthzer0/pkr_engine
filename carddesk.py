import random

d = []
suits = ('C', 'D', 'H', 'P')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'Q', 'K', 'A')
combinations = ('One', 'Pair', 'TwoPair', 'Set', 'Straight', 'Flush', 'FullHouse', 'Quads', 'StraightFlush', 'Royal')

def GetCardName(card):
    return suits[card[0]] + ranks[card[1]] + ' '

def GetDesk():

    desk = [(s, r) for s in range(len(suits)) for r in range(len(ranks))]

    return desk

def HangDesk(desk):
    newDesk = desk[:]
    random.shuffle(newDesk)
    return newDesk

def CreatePlayers(playersCount):
    return {'P' + str(i + 1): {'hand': []} for i in range(playersCount)}

def Deal(desk, players, cardCount):
    for _ in range(cardCount):
        for plr in players:
            players[plr]['hand'].append(desk.pop())

def IdentSet(hand):
    prev = None; prevS = None; mtr = []; z = 0; o = 0; r = False; s = True
    cards = ''
    for i in range(len(hand)):
        if prev != None:
            diff = hand[i][1] - prev
            mtr.append(diff)
            z += [0, 1][diff == 0]
            o += [0, 1][diff == 1]
            r = r or diff == 0 and z > 0 and len(mtr) > z
            s = s and prevS == hand[i][0]
        prev = hand[i][1]
        prevS = hand[i][0]
        cards += GetCardName(hand[i])
    
    rules = {
        o == 4 and s and hand[len(hand)-1][1] == len(ranks): 'Royal',
        o == 4 and s and hand[len(hand)-1][1] != len(ranks): 'StraightFlush',
        z == 3 and not r: 'Quads',
        z == 3 and r: 'FullHouse',
        o < 4 and s: 'Flush',
        o == 4 and not s: 'Straight',
        z == 2 and not r: 'Set',
        z == 2 and r: 'TwoPair',
        z == 1: 'Pair',
        z == 0 and o < 4 and not s: 'One'
    }

    comby = rules[True]

    if comby in ('Royal', 'StraightFlush', 'FullHouse', 'Flush', 'Straight', 'One'):
        highCard = hand[-1]
    else:
        highCard = hand[index(mtr, 0, mtr.count(0))]

    #return (comby, highCard, z, o, r, s, mtr, cards)
    return (combinations.index(comby), highCard[1], highCard[0])

def index(l, x, n):
    pos = -1
    for _ in range(n):
        pos = l.index(x, pos+1)
    return pos

def getKey(d, value):
    res = None
    for k, v in d.items():
        if v == value:
            res = k; break
    return res

def SortedCards(hand):
    hand.sort()
    hand.sort(key=lambda i: i[1])

"""def CompareCards(players):
    for plr in players:
        cards = players[plr]
        for curCard in cards:
            value = suits.index(curCard[0]) + ranks.index(curCard[1])"""

def SetSet(players):
    for plr in players:
        SortedCards(players[plr]['hand'])
        players[plr]['set'] = IdentSet(players[plr]['hand'])

def abra():
    dH = HangDesk(d)
    p = CreatePlayers(4)
    Deal(dH, p, 2)
    t = {'T': {'hand': []}}
    Deal(dH, t, 5)

    print(p)
    print(t)

def abra3():
    dH = HangDesk(d)
    p = CreatePlayers(4)
    Deal(dH, p, 5)
    print(dH)

    mS = (); pS = {}
    for plr in p:
        SortedCards(p[plr]['hand'])
        p[plr]['set'] = IdentSet(p[plr]['hand'])
        pS[plr] = p[plr]['set']
        mS = max(p[plr]['set'], mS)

    return p, getKey(pS, mS)

def abra2():
    dd = {}; nilList = [0] * 52; x = 10000

    dd = {crd: nilList[:] for crd in d}    
    for _ in range(x):
        dH = HangDesk(d)
        for crd in d:
            dd[crd][dH.index(crd)] += 1

    print(dd)

    
if __name__ == "__main__":
    d = GetDesk()
    abra()
    strParam = None
    while strParam != 'exit':
        strParam = input()
        if strParam == 'abra3': abra3()