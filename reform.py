from collections import OrderedDict
from math import log


class Manager:
    def __init__(self):
        self.ENGLISH = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,'
        self.HEBREW = 'אבגדהוזחטיכלמנסעפצקרשתףךןםץ .,'
        self.NUMBERS = '0123456789 .-'
        self.SPECIAL_CHARS = ' .!?\'"-,();*/\\=+_#@<>%&$^~|[]{}:₪€'
        self.CHARS = ""
        self.PAGE_SIZE = 1500
        self.search_result = {'start_page': None, 'start_index': None, 'end_page': None, 'end_index': None}

    @classmethod
    def total_characters_n_digits(cls, b, n):
        """
        Calculates the total number of characters needed to write all the numbers
        between 0 and the biggest n-digit number in base b.
        Example:
        for base 10 (b = 10) and n = 2, the total number of characters
        needed to write all the numbers with up to 2 digits (0 - 99),
        is given by the following formula.
        Note: this formula only applies for bases such that b >= 2.
        :param b: base
        :param n: max digits
        :return: total number of characters
        needed to write all the numbers with up to n digits in base b
        """
        if n == 0:
            return 0
        return (n - 1) * (b ** n) + (b - 2) * ((b ** n - 1) // (b - 1)) + 2

    def define_chars(self, english, hebrew, numbers, specials):
        chars = ""
        if english:
            chars += self.ENGLISH
        if hebrew:
            chars += self.HEBREW
        if numbers:
            chars += self.NUMBERS
        if specials:
            chars += self.SPECIAL_CHARS
        self.CHARS = "".join(OrderedDict.fromkeys(chars))

    def to_b(self, val):
        if val == 0:
            return self.CHARS[0]
        result = ""
        b = len(self.CHARS)
        while val > 0:
            result += self.CHARS[val - b * (val // b)]
            val = val // b
        return result[::-1]

    def get_sequence_at_position(self, pos, in_decimal=False):
        if pos == 0:
            return (0 if in_decimal else self.to_b(0)), 0
        b = len(self.CHARS)
        n = len(self.to_b(pos))
        a = 0 if n == 1 else int(log(n - 1, b))
        d = n - 1 - a
        D = d if pos <= self.total_characters_n_digits(b, d) else d + 1
        r = pos - self.total_characters_n_digits(b, D - 1)
        N = r // D
        c = r - N * D
        T = (b ** (D - 1) if D > 1 else 0) + N
        # T - the sequence at position. c - the index of specific character inside the sequence
        return (T if in_decimal else self.to_b(T)), c

    def get_char_by_position(self, pos):
        T, c = self.get_sequence_at_position(pos)
        return T[c]

    def to_decimal(self, val):
        result = 0
        for i in range(len(val)):
            result += self.CHARS.find(val[i]) * (len(self.CHARS) ** (len(val) - i - 1))
        return result

    def total_characters_to_sequence(self, val):
        if len(val) == 1:
            return self.CHARS.find(val)
        a = self.total_characters_n_digits(len(self.CHARS), len(val) - 1)
        val_decimal = self.to_decimal(val)
        b = (val_decimal - len(self.CHARS) ** (len(val) - 1) + 1) * len(val) - 1
        return a + b

    def get_page_number(self, val):
        if val == self.CHARS[0]:
            self.search_result = {'start_page': 1,
                                  'start_index': 0,
                                  'end_page': 1,
                                  'end_index': 1}
            return 1
        leading_zero = False
        if val[0] == self.CHARS[0]:
            val = self.CHARS[1] + val
            leading_zero = True

        pos = self.total_characters_to_sequence(val) - len(val) + 1
        if leading_zero:
            pos += 1
            val = val[1:]

        pages = pos // self.PAGE_SIZE
        start_page = pages + 1
        start_page_index = pos - pages * self.PAGE_SIZE

        end_page = (pos + len(val) - 1) // self.PAGE_SIZE
        end_page_index = (pos + len(val)) - end_page * self.PAGE_SIZE
        end_page += 1 if end_page * self.PAGE_SIZE != pos + len(val) else 0

        self.search_result = {'start_page': start_page,
                              'start_index': start_page_index,
                              'end_page': end_page,
                              'end_index': end_page_index}

        return pages + 1

    def get_page_by_number_old(self, number):
        """
        Deprecated. This function is slower than "get_page_by_number(number)"
        :param number:
        :return:
        """
        page_pos = (number - 1) * self.PAGE_SIZE
        page = ""
        for i in range(page_pos, page_pos + self.PAGE_SIZE):
            page += self.get_char_by_position(i)
        return page

    def get_page_by_number(self, number):
        page_pos = (number - 1) * self.PAGE_SIZE
        T, c = self.get_sequence_at_position(page_pos, in_decimal=True)
        page = self.to_b(T)[c:]
        while len(page) < self.PAGE_SIZE:
            T += 1
            page += self.to_b(T)
        return page[:self.PAGE_SIZE]

    def get_page_by_search(self, val):
        return self.get_page_number(self.get_page_number(val))

    def clear_search_result(self):
        self.search_result = {'start_page': None, 'start_index': None, 'end_page': None, 'end_index': None}
