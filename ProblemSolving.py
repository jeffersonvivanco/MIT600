# using bisection search

x = 0.5
epsilon = 0.01
numGuesses = 0
low = 0.0
high = max(x, 1.0)
ans = (high + low)/2.0
while abs(ans**2 - x) >= epsilon and ans <= x:
    numGuesses += 1
    if ans**2 < x:
        low = ans
    else:
        high = ans
    ans = (high + low)/2.0

print('num of guesses: {num}'.format(num=numGuesses))
# if abs(ans**2 - x) >= epsilon:
#     print('Failed on the square root of {x}'.format(x=x))
# else:
print('{ans} is close to the square root of {x}'.format(ans=ans, x=x))

def withinEpsilon(x, y, epsilon):
    # x, y, epsilon - floats
    # epsilon > 0
    return abs(x - y) <= epsilon