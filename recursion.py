# params
# n = how big the stack is, f = from stack, t = to stack, s = spare stack
def hanoi(n, f, t, s):
    if n == 1:
        print('move from f to t')
    else:
        Hanoi(n-1, f, s, t)
        Hanoi(1, f, t, s)
        Hanoi(n-1, s, t, f)

# hanoi(1, 'f', 't', 's')

def is_palindrome(s):
    if len(s) <= 1:
        return True
    else:
        return s[0] == s[-1] and is_palindrome(s[1:-1])


def check_palindrome(s):
    res = is_palindrome(s.lower())
    print(str(res))

check_palindrome('racecar')