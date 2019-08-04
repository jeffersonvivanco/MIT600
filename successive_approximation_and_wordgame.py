# successive approximation is a problem-solving method where you try to guess the right answer to a problem
# and then check your guess. If the guess is good enough, you're done. Otherwise, you keep improving your guess
# in small increments and checking it, getting closer and closer to the right answer, until you determine that the
# guess is good enough

# this function valuates a polynomial represented as a tuple for x. the index of a number in the tuple represents the power
# and the value at the index represents the coefficient for that term
# params: poly = tuple of numbers, x = what the function evaluates to
# params are floats
# returns float
def evaluate_poly(poly, x):
    res = 0
    for i in range(0, len(poly)):
        res += poly[i] * (x ** i)
    return res

# Derivatives
# Recall that the derivative of a polynomial f(x) = a*x^b is f'(x) = ab * x ^ (b-1), unless b=0,
# in which case f'(x) = 0. To compute the derivative of a polynomial function with many terms, you just do
# the same thing to every term individually. For example, if f(x) = x^4 + 3x^3 + 17.5x^2 - 13.39, then
# f'(x) = 4 * x^3 + 9 * x^2 + 35 * x
# this function computes the derivative of a polynomial function. It takes in a tuple of numbers poly and returns
# the derivative, which is also a polynomial represented by a tuple
def compute_deriv(poly):
    if len(poly) <= 1:
        0
    d = []
    for i in range(0, len(poly)):
        if i > 0:
            d.append(i * poly[i])
    return tuple(d)

# Newton's Method - a successive approximation method for finding the roots of a function. Recall that the roots of a function
# f(x) are the values of x such that f(x) = 0.
# Here is how Newton's method works:
# 1. We guess some x0
# 2. We check to see if it's a root or close enough to a root by calculating f(x0). If f(x0) is within some small value
# epsilon of 0, we say thats good enough and call x0 a root.
# 3. If f(x0) is not good enough, we need to come up with a better guess, x1. x1 is calculated by the equation:
# x1 = x0 - ( f(x0) / f'(x0) )
# 4. We check to see if x1 is close enough to a root. If it is not, we make a better guess x2 and check that. And so on
# and so on. For every xn that is not close enough to a root, we replace it with xn+1 = xn - ( f(xn)/f'(xn) ) and check if
# thats close enough to the root. We repeat until we finally find a value close to a root.
# this function applies Newton's method of successive approximation as described above to find a root of the polynomial function.
# It takes in a tuple of numbers poly, an initial guess x_0, and an error bound epsilon.
# It returns a tuple. The first element is the root of the polynomial represented by poly; the second element is the number of iterations
# it took to get to that root.
def compute_root(poly, x_0, ep, t):
    v = evaluate_poly(poly, x_0)
    if abs(v) <= ep:
        t += 1
        return (x_0, t)
    else:
        deriv = compute_deriv(poly)
        x_0 = x_0 - ( evaluate_poly(poly, x_0) / evaluate_poly(deriv, x_0))
        t += 1
        return compute_root(poly, x_0, ep, t)

# uncomment below to test above functions

# e = evaluate_poly((0.0, 0.0, 5.0, 9.3, 7.0), -13)
# print(e)
#
# d = compute_deriv((-13.9, 0.0, 17.5, 3.0, 1.0))
# print(d)
#
# r = compute_root((-13.39, 0.0, 17.5, 3.0, 1.0), 0.1, .0001, 0)
# print(r)

import random
import string
def hangman():
    r_word = select_random_word()
    user_word = '_' * len(r_word)
    num_guesses = len(r_word) * 2
    print(r_word)
    print('Welcome to the game, Hangman')
    print('I am thinking of a word that is {l} letters long'.format(l=len(r_word)), end='\n' + '-' * 50 + '\n')
    print('Available letters => ' + string.ascii_lowercase)

    while user_word != r_word and num_guesses > 0:
        print('You have {n} guesses left'.format(n=num_guesses))
        user_guess = input('Please guess a letter: ').lower()
        if len(user_guess) != 1 or user_guess not in string.ascii_lowercase:
            print('please enter a letter!!')
            continue
        num_guesses -= 1
        user_word_arr = list(l for l in user_word)
        if user_guess in r_word:
            for i in range(0, len(r_word)):
                if r_word[i] == user_guess:
                    user_word_arr[i] = user_guess
            user_word = ''.join(user_word_arr)
            print('Good guess: {w}'.format(w=user_word))
        else:
            print('Oops, that letter is not in my word: {w}'.format(w=user_word))

    if user_word == r_word:
        print('Congratulations, you won, word = {w}'.format(w=r_word))
    else:
        print('Sorry, the word was {w}'.format(w=r_word))


def select_random_word():

    try:
        print('Loading file')
        with open('words.txt') as f:
            words = f.read().strip().split()
            print('{l} words loaded'.format(l=len(words)))
            r_word = words[random.randint(0, len(words) - 1)]
            return r_word

    except FileNotFoundError:
        print('File words.txt not found')

hangman()