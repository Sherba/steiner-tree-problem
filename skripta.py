from random import randint

n = 15;
print([(a, b, randint(4, 10)) for a in range(n) for b in range(n) if a < b])
