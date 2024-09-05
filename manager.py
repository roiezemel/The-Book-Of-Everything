import random
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .!?'\"-,()אבגדהוזחטיכלמנסעפצקרשתךףםץן0123456789"

LINE_LENGTH = 50
PAGE_LINES = 40
PAGE_SIZE = LINE_LENGTH * PAGE_LINES


FIRST_PAGE_TEXT = "The Book of Everything By This computer"


def to_int(s):
    return sum([(CHARS.find(s[-i]) + 1) * ((len(CHARS) + 1) ** (i - 1)) for i in range(1, len(s) + 1)])


def to_str(n):
    result = ""
    ns = str(n)
    if len(ns) % 2:
        ns = '0' + ns
    for i in range(0, len(ns), 2):
        index = int(ns[i] + ns[i + 1]) - 1
        if index == -1:
            return ""
        result += CHARS[index]
    return result


def get_page_by_search(s):
    return make_page(s, to_int(s))


def get_page_by_number(n):
    if n == 0:
        return FIRST_PAGE_TEXT
    return make_page(to_str(n), n)


def make_page(val, seed):
    random.seed(seed)
    page_pos = random.randint(0, PAGE_SIZE - len(val))
    before = ''.join([CHARS[random.randint(0, len(CHARS) - 1)] for _ in range(page_pos)])
    after = ''.join([CHARS[random.randint(0, len(CHARS) - 1)] for _ in range(PAGE_SIZE - len(val) - page_pos)])
    return before + val + after


def page_lines(page_content):
    return [page_content[i:i + LINE_LENGTH] for i in range(0, len(page_content), LINE_LENGTH)]


def format_page(page_content):
    return '\n'.join(page_lines(page_content))
