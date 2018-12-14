def make_recipes(initial_recipes, n):
    recipes = initial_recipes
    elf_1_idx = 0
    elf_2_idx = 1

    end_length = len(recipes) + n + 10

    #print(recipes)

    while True:
        recipes += str(int(recipes[elf_1_idx]) + int(recipes[elf_2_idx]))
        elf_1_idx = (int(elf_1_idx) + int(recipes[elf_1_idx]) + 1) % len(recipes)
        elf_2_idx = (int(elf_2_idx) + int(recipes[elf_2_idx]) + 1) % len(recipes)
        #print(recipes)

        if len(recipes) >= end_length:
            return recipes[n:n + 10]


def find_pattern_in_recipes(pattern):
    recipes = '37'
    elf_1_idx = 0
    elf_2_idx = 1

    #print(recipes)
    last_six = ''

    while True:
        to_add = str(int(recipes[elf_1_idx]) + int(recipes[elf_2_idx]))
        for c in to_add:
            recipes += c
            last_six += c
            if len(last_six) > len(pattern):
                last_six = last_six[1:]
            #print(last_six)
            if last_six == pattern:
                return len(recipes) - len(pattern)
            
        
        elf_1_idx = (int(elf_1_idx) + int(recipes[elf_1_idx]) + 1) % len(recipes)
        elf_2_idx = (int(elf_2_idx) + int(recipes[elf_2_idx]) + 1) % len(recipes)
        #print(recipes)


#print(make_recipes('37', 77201))
print(find_pattern_in_recipes(pattern='077201'))
