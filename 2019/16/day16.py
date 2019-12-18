from itertools import cycle

base_pattern = [0, 1, 0, -1]

def get_new_pattern(times_to_repeat, num_len) -> int:
    i = 0
    while True:
        for p in base_pattern:
            for _ in range(times_to_repeat):
                if i == 0:
                    i += 1
                    continue
                yield int(p)
                if i == num_len:
                    return
                i += 1


def fft(input: str, phases: int) -> str:
    num_len = len(input)

    for _ in range(phases):
        output = ""
        for i in range(num_len):
            times_to_repeat = i + 1
            pattern = get_new_pattern(times_to_repeat, num_len)
            total = 0
            for ch in input:
                product = next(pattern) * int(ch)
                total += product
            output += str(total)[-1]
        input = output
    return output


# print(list(get_new_pattern(1, 8)))
# print(list(get_new_pattern(2, 8)))
# print(list(get_new_pattern(3, 8)))
# print(list(get_new_pattern(4, 8)))
assert fft('12345678', 4) == '01029498'
assert fft('80871224585914546619083218645595', 100)[:8] == '24176176'
assert fft('19617804207202209144916044189917', 100)[:8] == '73745418'
assert fft('69317163492948606335995924319873', 100)[:8] == '52432133'

# print(fft('59773419794631560412886746550049210714854107066028081032096591759575145680294995770741204955183395640103527371801225795364363411455113236683168088750631442993123053909358252440339859092431844641600092736006758954422097244486920945182483159023820538645717611051770509314159895220529097322723261391627686997403783043710213655074108451646685558064317469095295303320622883691266307865809481566214524686422834824930414730886697237161697731339757655485312568793531202988525963494119232351266908405705634244498096660057021101738706453735025060225814133166491989584616948876879383198021336484629381888934600383957019607807995278899293254143523702000576897358', 100))