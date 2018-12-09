from collections import defaultdict


class Node:
    def __init__(self, value):
        self.value = value
        self.previous = self
        self.next = self

    def delete(self):
        self.previous.next = self.next
        self.next.previous = self.previous
        return self.next

    def clockwise(self, n):
        current = self
        for i in range(n):
            current = current.next
        return current

    def counter_clockwise(self, n):
        current = self
        for i in range(n):
            current = current.previous
        return current

    def insert_before(self, value):
        new_node = Node(value)
        new_node.previous = self.previous
        new_node.next = self
        self.previous.next = new_node
        self.previous = new_node
        return new_node

    def insert_after(self, value):
        new_node = Node(value)
        new_node.previous = self
        new_node.next = self.next
        self.next.previous = new_node
        self.next = new_node
        return new_node

def get_high_score_linked(num_players, last_marble_score):
    current = Node(0)
    scores = defaultdict(int)
    marble_id = 1
    while True:
        for player_id in range(num_players):
            if marble_id % 23 == 0:
                score = 0
                score += marble_id
                to_take = current.counter_clockwise(7)
                score += to_take.value
                scores[player_id] += score
                current = to_take.delete()
                # print('Player {} marble {} scores {}, total score {}'.format(player_id, marble_id, score, scores[player_id]))
            else:
                to_place = current.clockwise(1)
                current = to_place.insert_after(marble_id)
            # print_circle(circle, current_index)
            if marble_id == last_marble_score:
                return max(scores.values())
            
            marble_id += 1


print(get_high_score_linked(458, 7201900))
