import re

LINE_PATTERN = re.compile(r'(?P<team>[a-z]+) (?P<num_units>\d+) units each with (?P<unit_hp>\d+) hit points (\((?P<weaknesses>.+)\) )?with an attack that does (?P<attack_damage>\d+) (?P<attack_type>[a-z]+) damage at initiative (?P<initiative>\d+)')

class Group:
    def __init__(
        self,
        id,
        team,
        num_units, 
        unit_hp, 
        attack_type, 
        attack_damage, 
        initiative, 
        weaknesses,
        immunities,
    ):
        self.id = id
        self.team = team
        self.num_units = int(num_units)
        self.unit_hp = int(unit_hp)
        self.attack_type = attack_type
        self.attack_damage = int(attack_damage)
        self.initiative = int(initiative)
        self.weaknesses = weaknesses
        self.immunities = immunities

    def __str__(self):
        return str(self.__dict__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Group) and self.id == other.id

    def effective_power(self):
        return self.num_units * self.attack_damage

    def calculate_attack_damage(self, target):
        if self.attack_type in target.immunities:
            return 0
        damage = self.effective_power()
        if self.attack_type in target.weaknesses:
            damage *= 2
        return damage

    def target_sort_key(self, target):
        return (
            -self.calculate_attack_damage(target),
            -target.effective_power(),
            -target.initiative,
        )

    def take_damage(self, damage):
        num_lost = (damage // self.unit_hp)
        self.num_units -= num_lost
        #print('{} lost {} units'.format(self.id, num_lost))

    def is_alive(self):
        return self.num_units > 0

def parse_weaknesses_and_immunities(weaknesses_str):
    weaknesses = []
    immunities = []
    clauses = weaknesses_str.split('; ')
    for clause in clauses:
        if clause.startswith('weak to '):
            weaknesses.extend(clause.split('weak to ')[1].split(', '))
        elif clause.startswith('immune to '):
            immunities.extend(clause.split('immune to ')[1].split(', '))
    return weaknesses, immunities

def parse_groups(filename):
    team_ids = {
        'immune': 1,
        'infection': 1,
    }
    with open(filename) as file:
        for i, line in enumerate(file):
            match = LINE_PATTERN.match(line.rstrip('\n'))
            group_dict = match.groupdict()
            weaknesses = []
            immunities = []
            if group_dict.get('weaknesses'):
                weaknesses, immunities = parse_weaknesses_and_immunities(group_dict['weaknesses'])
            yield Group(
                group_dict['team'] + str(team_ids[group_dict['team']]),
                group_dict['team'],
                group_dict['num_units'],
                group_dict['unit_hp'],
                group_dict['attack_type'],
                group_dict['attack_damage'],
                group_dict['initiative'],
                weaknesses,
                immunities,
            )
            team_ids[group_dict['team']] += 1

def run_battle(filename, immunity_boost=0):
    groups = list(parse_groups(filename))
    for group in groups:
        if group.team == 'immune':
            group.attack_damage += immunity_boost
    i = 1
    while True:
        #print('fight {}'.format(i))
        choosable_groups = list(groups)
        targets = {}
        target_selection_groups = sorted(groups, key=lambda group: (-group.effective_power(), -group.initiative))
        for targeting_group in target_selection_groups:
            # check if dead?
            choosable_enemies = (target for target in choosable_groups if targeting_group.team != target.team)
            target = min(choosable_enemies, key=lambda target: targeting_group.target_sort_key(target), default=None)
            if target and targeting_group.calculate_attack_damage(target) > 0:
                targets[targeting_group] = target
                choosable_groups.remove(target)

        # attack
        for attacker in sorted(targets.keys(), key=lambda group: -group.initiative):
            if not attacker.is_alive():
                continue
            target = targets[attacker]
            damage = attacker.calculate_attack_damage(target)
            #print('{} attacking {}'.format(attacker.id, target.id))
            target.take_damage(damage)
            if not target.is_alive():
                groups.remove(target)

        teams = {group.team for group in groups}
        num_teams_alive = len(teams)
        if num_teams_alive == 1:
            return teams.pop(), sum((group.num_units for group in groups))
        i += 1

def find_smallest_boost_to_immunity(filename):
    boost = 188
    while True:
        print(boost)
        winner, num_left = run_battle(filename, boost)
        if winner == 'immune':
            return num_left
        boost += 1

print(find_smallest_boost_to_immunity('day24_input.txt'))