class NumberGenerator:
    def __init__(self, start, multiplicand, multiple):
        self.last = start
        self.multiplicand = multiplicand
        self.multiple = multiple

    def get(self):
        while True:
            next_val = (self.multiplicand * self.last) % 2147483647
            self.last = next_val
            if next_val % self.multiple == 0:
                return next_val


def gen_a(prev):
    return (16807 * prev) % 2147483647


def gen_b(prev):
    return (48271 * prev) % 2147483647


def judge():
    a_prev = 883
    b_prev = 879

    a_gen = NumberGenerator(a_prev, 16807, 4)
    b_gen = NumberGenerator(b_prev, 48271, 8)

    matches = 0
    for i in range(5000000):
        a_val = a_gen.get()
        b_val = b_gen.get()
        # print(a_val, b_val)
        # print(bin(a_prev & 0xffff), bin(b_prev & 0xffff))
        if ((a_val & 0xffff) == (b_val & 0xffff)):
            matches += 1
    print(matches)


judge()
