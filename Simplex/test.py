from LPP import LPP

lpp = LPP()

lpp.add_W(["6.5", "0", "-7.5", "23.5", "-5", 0])

lpp.add_limit(["1", "3", "1", "4", "-1", "12"])
lpp.add_limit(["2", "0", "-1", "12", "-1", "14"])
lpp.add_limit(["1", "2", "0", "3", "-1", "6"])

lpp.simplex_method(max=True)
lpp.simplex_method(max=True)
lpp.simplex_method(max=True)

print(lpp.get_optimal_value())

