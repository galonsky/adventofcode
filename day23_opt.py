# h = 0

# while c != b: # b: 108400 -> 125400 in chunks of 17
# 	f = 1
# 	d = 2
# 	e = 2
# 	while d != b:
# 		e = 2
# 		while e != b:
# 			if d * e == b:
# 				f = 0
# 			e += 1
# 		d += 1
# 	if f == 0:
# 		h += 1
# 	b += 17

# # optimized to

# e = b
# d = b
# if b % 2 == 0:
# 	f = 0

import math

h = 0
for b in range(108400, 125400 + 1, 17):
	sqrt = math.ceil(math.sqrt(b))
	if any((b % k == 0 for k in range(2,sqrt))):
		h = h + 1
print(h)
