import classes as cl

desk = cl.Desk()

desk.hang_desk()

print(desk)

card = desk.deal_card()

print(desk.get_card_name(card))
print(desk)