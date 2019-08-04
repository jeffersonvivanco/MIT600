import unittest
import ps4

class TestCase(unittest.TestCase):

    def test_build_coder(self):
        # testing with positive values
        c = ps4.build_coder(28)
        self.assertEqual('B', c['u']['A'])
        self.assertEqual('C', c['u']['B'])
        self.assertEqual('b', c['l']['a'])
        self.assertEqual('a', c['l'][' '])

    def test_build_encoder(self):
        e = ps4.build_encoder(35)
        print(e)
        # self.assertEqual('D', e['u']['A'])
        # self.assertEqual('C', e['u']['Z'])
        # self.assertEqual('a', e['l']['y'])
        # self.assertEqual('d', e['l']['a'])
        self.assertEqual('g', e['l']['z'])

    def test_build_decoder(self):
        d = ps4.build_decoder(35)
        # self.assertEqual(d['u']['E'], 'E')
        self.assertEqual('z', d['l']['g'])

    def test_apply_coder(self):
        e = ps4.build_encoder(3)
        a = ps4.apply_coder('Hello, world!', e)
        print('\n' + a)
        self.assertEqual('Khoor,czruog!', a)

    def test_apply_shift(self):
        # t = ps4.apply_shift('z', 35)
        # self.assertEqual('g', t)
        # t1 = ps4.apply_shift(t, -35)
        # self.assertEqual('z', t1)
        t = ps4.apply_shift('This is a test.', 8)
        t2 = ps4.apply_shift(t, -8)
        self.assertEqual('Apq hq hiham a.', t)
        self.assertEqual('This is a test.', t2)
        s = 'Do Androids Dream of Electric Sheep?'
        t3 = ps4.apply_shift(s, 8)
        t4 = ps4.apply_shift(t3, -8)
        self.assertEqual(s, t4)

    def test_find_best_shift(self):
        encrypted_text = ps4.apply_coder('Hello, world!', ps4.build_encoder(8))
        print('encrypted {e}'.format(e=encrypted_text))
        b = ps4.find_best_shift(encrypted_text)
        self.assertEqual(8, b)
        text = ps4.apply_coder(encrypted_text, ps4.build_decoder(b))
        self.assertEqual('Hello, world!', text)

    def test_find_best_shift_2(self):
        for i in range(10):
            encrypted_text = ps4.random_scrambled(1)
            b = ps4.find_best_shift(encrypted_text)
            decrypted_text = ps4.apply_coder(encrypted_text, ps4.build_decoder(b))
            print('\nencrypted text: {e}, decrypted text: {d}'.format(e=encrypted_text, d=decrypted_text))
            self.assertTrue(ps4.is_word(decrypted_text))

    def test_apply_shifts(self):
        s = 'Do Androids Dream of Electric Sheep?'
        shifted_string = ps4.apply_shifts(s, [(0, 6), (3, 18), (12, 16)])
        self.assertEqual(len(s), len(shifted_string))
        b = ps4.find_best_shift(shifted_string)
        d = ps4.apply_coder(shifted_string, ps4.build_decoder(b))
        print('\n {b}, {d}'.format(b=b, d=d))
        # self.assertEqual('JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?', shifted_string)

    def test_apply_shifts_2(self):
        s = 'Do Androids Dream of Electric Sheep?'
        shifted_string = ps4.apply_shifts(s, [(0, 6), (3, 18), (12, 16)])
        reshifted_string = ps4.apply_shifts(shifted_string, [(0, -6), (3, -18), (12, -16)])
        self.assertEqual(s, reshifted_string)

    def test_random_string(self):
        s = ps4.random_string(20)
        self.assertIsNotNone(s)

    def test_random_scrambled(self):
        s = ps4.random_scrambled(1)
        print('\nWord is \n'+s)
        self.assertIsNotNone(s)

    def test_find_best_shifts(self):
        e = ps4.random_scrambled(2)
        bs = ps4.find_best_shifts(e)
        print(bs)
        ss = ps4.apply_shifts(e, bs)
        print(ss)

    def test_is_word(self):
        w = ps4.is_word('N')
        self.assertTrue(w)

    def test_find_best_shifts_2(self):
        s = 'Do Androids Dream of Electric Sheep?'
        print('\nlen of s {s}\n'.format(s=len(s)))
        shifted_string = ps4.apply_shifts(s, [(0, 6), (3, 18), (12, 16)])
        bs = ps4.find_best_shifts(shifted_string)
        print(bs)
        d = ps4.apply_shifts(shifted_string, bs)
        print(d)