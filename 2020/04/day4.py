import re
from typing import List


def get_passports(filename: str) -> List[dict]:
    with open(filename, 'r') as file:
        content = file.read()
        pass_dicts = []
        passports = content.split('\n\n')
        for passport in passports:
            pairs = passport.split()
            pass_dict = {}
            for pair in pairs:
                sides = pair.split(':')
                pass_dict[sides[0]] = sides[1]
            pass_dicts.append(pass_dict)
        return pass_dicts


def validate_birth_year(val: str) -> bool:
    return len(val) == 4 and 1920 <= int(val) <= 2002


def validate_issue_year(val: str) -> bool:
    return len(val) == 4 and 2010 <= int(val) <= 2020


def validate_expiration_year(val: str) -> bool:
    return len(val) == 4 and 2020 <= int(val) <= 2030


def validate_height(val: str) -> bool:
    unit = val[-2:]
    if unit == 'cm':
        return 150 <= int(val[:-2]) <= 193
    else:
        return 59 <= int(val[:-2]) <= 76


def validate_hair_color(val: str) -> bool:
    pattern = re.compile(r'^#[0-9a-f]{6}$')
    return bool(pattern.match(val))


def validate_eye_color(val: str) -> bool:
    return val in (
        'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth',
    )


def validate_passport_id(val: str) -> bool:
    pattern = re.compile(r'^[0-9]{9}$')
    return bool(pattern.match(val))


VALIDATORS = {
    'byr': validate_birth_year,
    'iyr': validate_issue_year,
    'eyr': validate_expiration_year,
    'hgt': validate_height,
    'hcl': validate_hair_color,
    'ecl': validate_eye_color,
    'pid': validate_passport_id,
}


if __name__ == '__main__':
    passports = get_passports('input.txt')
    required_keys = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
    }
    count = 0
    for passport in passports:
        if required_keys <= passport.keys():
            if all(validator(passport[key]) for (key, validator) in VALIDATORS.items()):
                count += 1
    print(count)