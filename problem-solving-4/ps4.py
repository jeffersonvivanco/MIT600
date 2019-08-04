import string, unicodedata, math, random

words = []

# creating a map of chars we want to remove such as '!', ',', '?'
remap = {
    ord('!'): None,
    ord(','): None,
    ord('?'): None,
    ord('"'): None,
    ord('.'): None
}
prev_word = ''

def build_coder(shift):
    """
    Returns a dict that can apply a Ceasar cipher to a letter. Ignores non-letter characters like punctuation and numbers.
    :param shift: -27 < int < 27
    :return: dict
    """
    coder = {'l': {}, 'u': {}}
    l_letters = {}
    u_letters = {}

    index = 1
    # Making letter reference for uppercase letters
    for l in string.ascii_uppercase:
        u_letters[index] = l
        index += 1

    # Adding space after 'z'
    u_letters[index] = ' '

    index = 1
    # Making letter reference for lowercase letters
    for l in string.ascii_lowercase:
        l_letters[index] = l
        index += 1

    # Adding space after 'z'
    l_letters[index] = ' '

    start = 1
    end = index

    # shifting letters
    for l in u_letters.keys():
        s = l + shift
        if s > end:
            s = (abs(s) % end)
        if s < start:
            s = end - (abs(s) % end)
        coder['u'][u_letters[l]] = u_letters[s]

    for l in l_letters.keys():
        s = l + shift
        if s > end:
            s = (abs(s) % end)
        if s < start:
            s = end - (abs(s) % end)
        coder['l'][l_letters[l]] = l_letters[s]

    return coder

def build_encoder(shift):
    """
    Returns a dict that can used to encode a plain text.
    :param shift: 0 <= int < 27
    :return: dict
    """
    return build_coder(shift)

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text.
    :param shift: 0 <= int < 27
    :return: dict
    """
    return build_coder(-shift)

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.
    :param text: string
    :param coder: dict with mappings of characters to shifted characters
    :return: text after mapping coder chars to original text
    """
    encoded_s = ''
    for s in text:
        o = ord(s)
        if ord('a') <= o <= ord('z') or o == ord(' '):
            encoded_s += coder['l'][s]
        elif ord('A') <= o <= ord('Z'):
            encoded_s += coder['u'][s]
        else:
            encoded_s += s

    return encoded_s

def apply_shift(text, shift):
    """
    Given a text, returns a new text Ceasar shifted by the given shift offset.
    :param text: string to apply the shift to
    :param shift: amount to shift the text
    :return: text after being shifted by specific amount
    """
    encoder = None
    if shift > 0:
        encoder = build_encoder(shift)
    elif shift < 0:
        encoder = build_decoder(abs(shift))
    else:
        print("Error: shift cannot be zero")

    return apply_coder(text, encoder)

def load_words():
    global words
    print('Loading word list from file ...')
    try:
        with open('words.txt') as f:
            lines = (line.strip() for line in f)
            for line in lines:
                words += line.split(' ')
        print('{a} words loaded'.format(a=len(words)))
    except FileNotFoundError:
        print('File words.txt not found!')

def is_word(word):
    '''
    checks if word is in words
    :param word: string
    :return: boolean
    '''
    global words
    if word.lower().strip() in words:
        return  True
    else:
        return False

def find_best_shift(text, start_shift=1):
    '''
    Decrypts the encoded text and returns the plaintext.
    :param text: string
    :return: 0 <= int < 27
    '''
    global words
    global remap

    max_shift = 1
    shift = start_shift
    max_word_len = 0

    while shift < 100:
        sentence_shifted = apply_shift(text, -shift)
        s_words = sentence_shifted.split(' ')
        words_len = 0
        w = s_words[0]
        w = w.translate(remap)

        if is_word(w):
            words_len = len(w)

        if words_len > max_word_len:
            max_shift = shift
            max_word_len = words_len

        shift += 1
    return max_shift

def apply_shifts(text, shifts):
    '''
    Applies a sequence of shifts to an input text
    :param text: string
    :param shifts: a list of tuples containing the location each shift should begin and the shift offset. Each tuple is of
    the form (location, shift). The shifts are layered: each one is applied from its starting position all the way through
    the end of the string.
    :return: text after applying shifts
    '''
    shifted_final_string = ''
    prev_shift = 0
    for s in shifts:
        shifted_string = apply_shift(text, s[1] + prev_shift)
        prev_shift += s[1]
        shifted_final_string = shifted_final_string[0:s[0]] + shifted_string[s[0]:]
    return shifted_final_string

def find_best_shifts(text):
    '''
    Given a scrambled string, returns a shift key that will decode the text to words in wordlist, or None if there is
    no such key.
    :param text: scrambled text to try to find the words for
    :return: lists of tuples, each tuple is (position in text, amount of shift)
    '''
    best_shifts =  _find_best_shifts_rec(text, 0)
    best_shifts_altered = []
    prev_shift = 0
    for s in best_shifts:
        shift = s[1] - prev_shift
        best_shifts_altered.append((s[0], -shift))
        prev_shift += shift

    return best_shifts_altered

def _find_best_shifts_rec(text, start, start_shift=1):
    '''
    Given a scrambled string and a given position from which to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.
    :param text: scrambled text to try to find the words for
    :param start: where to start looking at shifts
    :return: list of tuples, each tuple is (position in text, amount of shift)
    '''
    global remap
    global prev_word

    if len(text[start:]) == 0:
        return []
    # best shift, should find first word in sentence
    b = find_best_shift(text[start:], start_shift)
    d = apply_coder(text, build_decoder(b))
    s = start
    prev_start = start
    next_start = start
    while s < len(d) - 1:
        s += 1
        if d[s] in [' ', '!', ',', '?', '"', '.'] or s == len(d) - 1:
            c_w = d[prev_start:s + 1]
            if not is_word(c_w):
                if prev_word == c_w:
                    next_start = s+1
                else:
                    prev_word = c_w
                    s += 1
                break
            else:
                prev_start = s
                next_start = s + 1

    return [(start, b)] + _find_best_shifts_rec(text, next_start, abs(b))

def random_string(n):
    '''
    Generates n random words from wordlist and returns them in a string
    :param n: number of random words
    :return: n random words in a string
    '''
    global words
    random_words = random.choices(words, k=n)
    return ' '.join(random_words)

def random_scrambled(n):
    '''
    Generates n random words from wordlist and returns them in a string after encrypting them with a random multi-level
    Ceasar shift.
    :param n: number of encrypted words
    :return: n encrypted words in a string
    '''
    random_words = random_string(n)
    start = 0
    end = 0
    shifts = []
    for i in range(0, len(random_words)):
        if i == 0:
            start = i
        if random_words[i] == ' ' or i == len(random_words) - 1:
            end = i
            shifted_word = apply_shift(random_words[start:end + 1], random.randint(1, 26))
            start = end + 1
            shifts.append(shifted_word)
    return ''.join(shifts)

def decrypt_fable():
    fable_string = get_fable_string()
    fable_string = fable_string.translate(remap)
    print('Decrypting fable text please wait ...')
    bs = find_best_shifts(fable_string)
    d = apply_shifts(fable_string, bs)
    print('Fable text below:')
    print(d)
    # I don't understand the fable, but I think it has something to do with just moving forward
    # which is how I think my education is
    return d

def get_fable_string():
    try:
        with open('fable.txt') as f:
            return f.read()
    except FileNotFoundError:
        print('File not found!')

# load on start
load_words()
decrypt_fable()