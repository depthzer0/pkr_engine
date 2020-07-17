import classes as cl

rules = cl.Rules()

print(rules.get_sets([(1, 4), (1, 8)], [(2, 4), (1, 6), (1, 5), (1, 7), (1, 3)]))