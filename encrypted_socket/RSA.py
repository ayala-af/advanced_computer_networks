#add an expla


P = 137
Q = 151
T = (P-1)*(Q-1)
print(T)
print(("t"))
E = 83
print(T%E)
print("T%E")
i = 2
while True:
 res = (i*E)%T
 if res == 1:
    print(i)
    break
 i += 1