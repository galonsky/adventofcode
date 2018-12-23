# import ipdb
# ipdb.set_trace()
reg3 = 0
reg0 = 0

guesses = []

while True:
    reg2 = reg3 | 0x10000
    reg3 = 0xD6B39A


    while True:
        reg1 = reg2 & 0xFF
        # if reg1 == 0:
        #     print('reg1 set to 0 when reg2 = {}'.format(hex(reg2)))
        reg3 += reg1
        reg3 &= 0xFFFFFF
        reg3 *= 0x1016b
        reg3 &= 0xFFFFFF
        # if reg1 == 0:
        #     print('reg 3 = {}'.format(hex(reg3)))

        if 0x100 > reg2:
            break

        # simplified inner loop
        reg2 = reg2 >> 8

    #print('checking reg3 {}'.format(hex(reg3)))
    if reg3 in guesses:
        print('already guessed {} at index {}'.format(hex(reg3), guesses.index(reg3)))
        print(len(guesses), guesses[-1])
        break
    else:
        guesses.append(reg3)
    if reg3 == reg0:
        break