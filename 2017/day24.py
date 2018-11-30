from copy import deepcopy
from collections import defaultdict


def extend_links(bridges, link):
    # print(link)
    head = link[-1][0]
    tail = link[-1][1]
    if not bridges[tail]:
        return [link]
    bridges[head].remove(tail)
    if head != tail:
        bridges[tail].remove(head)

    links = [link]
    bridge_cpy = deepcopy(bridges)
    for new_tail in bridges[tail]:
        new_link = list(link)
        new_link.append([tail, new_tail])
        links += extend_links(deepcopy(bridge_cpy), new_link)

    return links

def score(link):
    return sum([sum(bridge) for bridge in link])




with open('day24_input.txt') as file:
    bridges = defaultdict(list)
    for line in file:
        bridge = [int(part) for part in line.rstrip('\n').split('/')]
        bridges[bridge[0]].append(bridge[1])
        if bridge[0] != bridge[1]:
            bridges[bridge[1]].append(bridge[0])

    print(bridges)

    links = []
    for zero_tail in bridges[0]:
        links += extend_links(deepcopy(bridges), [[0, zero_tail]])

    max_len = max([len(link) for link in links])

    print(max([score(link) for link in links if len(link) == max_len]))
