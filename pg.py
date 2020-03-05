import classes as cl

table = cl.Table(4, 500, 20)
table.pre_flop()
print(table)

table.flop()
print(table)

table.turn_river()
print(table)

table.turn_river()
print(table)

'''desk = cl.Desk()

desk.hang_desk()

print(desk)

card = desk.deal_card()

print(desk.get_card_name(card))
print(desk)'''
