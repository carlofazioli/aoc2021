import itertools
import collections

from utilities import load_data, submit

input_data = load_data(day=13)

points, folds = input_data.split('\n\n')
points = points.splitlines()
folds = folds.splitlines()

locs = set()
for point in points:
    x, y = list(map(int, point.split(',')))
    locs.add((x, y))

for f in folds:
    fold_loc = f.split(' ')[-1]
    d, val = fold_loc.split('=')
    val = int(val)
    new = set()
    if d == 'x':
        for p in locs:
            if p[0] < val:
                new.add(p)
            else:
                x = 2*val - p[0]
                new.add((x, p[1]))
    if d == 'y':
        for p in locs:
            if p[1] < val:
                new.add(p)
            else:
                y = 2*val - p[1]
                new.add((p[0], y))
    locs = new

X = max(x for x, y in locs)
Y = max(y for x, y in locs)
for y in range(Y+1):
    for x in range(X + 1):
        if (x, y) in locs:
            print('#', end='')
        else:
            print(' ', end='')
    print()
