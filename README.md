# Advent of Code 2021

Code + writeups for AoC 2021!  Use the bullet-list icon to 
navigate to each day/part.  

## Day 1

### Part 1

This puzzle provides a list of integers, representing depths 
identified by a sonar sweep in a submarine.  We are asked to
inspect consecutive pairs of measurements, and count the 
number of times the 2nd is larger than the 1st.  

With the integers stored in the list `input_data`, we can use
a list comprehension together with a `zip` operation to build
the deltas between subsequent elements:

```python
diffs = [b-a for a, b in zip(input_data[:-1], input_data[1:])]
```

Here, the `zip` operation collates its two operands into an
iterable of ordered pairs.  The operands use python list
slicing to extract subsets of the input list array.  

```python
input_data[:-1] = [d0, d1, ..., dn-1]
input_data[1:]  = [d1, d2, ..., dn]
zip(...)        = [(d0, d1), (d1, d2), ..., (dn-1, dn)]
```

The comprehension extracts the values of each ordered 
pair into the local vars `a, b` and populates the list
with their difference.  

Next, we want to count the number of times these [forward
differences](https://en.wikipedia.org/wiki/Finite_difference#Basic_types)
are strictly greater than zero.  

We can identify these by creating a lambda function to
test for positivity, and map this onto the diffs:
The result is an iterable of booleans, with `True` when the
forward difference is positive, and `False` otherwise.  
We can use the builtin `sum` on this iterable to count
the number of increases:

```python
f = lambda x: x > 0
increases = map(f, diffs)
answer = sum(increases)
```

### Part 2

For part 2, we need to repeat the above, but instead of 
operating on the original list of integers we need to
create a list of sliding window sums.  We can create
this list with another comprehension:

```python
windows = [sum(input_data[i:i+3]) for i in range(len(input_data)-2)]
```

Here, we iterate over the first `n-2` indices of `input_data`.  
For each index, we sum the window of 3 values starting there.  
Then, we simply repeat the forward difference calculation,
lambda function mapping, and summation as before.  

```python
diffs = [b-a for a, b in zip(windows[:-1], windows[1:])]
increases = map(f, diffs)
answer = sum(increases)
```

## Day 2

### Part 1

For this puzzle, our input consists of a list of instructions.  Each
instruction is a keyword from the set `forward, down, up`, followed
by an integer value that the puzzle calls `X`.  

The puzzle tells us that the instructions indicate how we pilot a
submarine whose initial coordinates are `horizontal = 0` and 
`depth = 0`.  There are descriptions of how each instruction keyword
modifies the `horizontal` and `depth` coordinates.  We simply 
translate those descriptions into cases, and loop over the list of 
instructions:

```python
horizontal = 0
depth = 0
for instruction in input_data:
    a, x = instruction.split(' ')
    x = int(x)
    if a == 'forward':
        horizontal += x
    if a == 'down':
        depth += x
    if a == 'up':
        depth -= x
```

The descriptions are slightly tricky, since depth is a positive quantity
that increases when instructed by the `down` keyword.  Once we've 
completed this iteration, the product of `horizontal` and `depth` is our
answer.

### Part 2

For the next part, the descriptions of the instruction keywords changes,
but the overall solution method remains the same.  So, we just make a 
small alternation to the code:

```python
horizontal = 0
depth = 0
aim = 0
for instruction in input_data:
    a, x = instruction.split(' ')
    x = int(x)
    if a == 'forward':
        horizontal += x
        depth += aim*x
    if a == 'down':
        aim += x
    if a == 'up':
        aim -= x
```

## Day 3

### Part 1

The puzzles from Day 3 require us to analyze a list of numbers represented
as a strings of zeroes and ones.  The list of numbers represents a 
diagnostic report, and analyzing the report implies two values `gamma` and
`epsilon`.  

To define these values, we need to parse the entire diagnostic report, and
find the most frequent bit in each binary digit place.  The value `gamma` 
is the binary number whose digits are comprised of these most-frequent bits.
The value `epsilon` is the bitwise NOT of `gamma`.  

It would have been more efficient to parse the diagnostic list a single time,
but the first idea that popped in my head at midnight was to parse the list
once for each digit.  Additionally, I wasn't sure about exactly how to 
bitwise NOT one of the values to get the other, so I constructed both at the
same time.  So, here's my initial solution:

```python
gamma = ''
epsilon = ''
for i in range(len(input_data[0])):
    count_0 = 0
    count_1 = 0
    for b in input_data:
        if b[i] == '0':
            count_0 += 1
        if b[i] == '1':
            count_1 += 1
    if count_0 > count_1:
        gamma += '0'
        epsilon += '1'
    else:
        gamma += '1'
        epsilon += '0'
answer = int(gamma, 2) * int(epsilon, 2)
```

Here's a slightly slicker implementation I wrote after thinking about it a bit more:

```python
n = len(input_data[0])
N = len(input_data)
count_ones = [0]*n
for b in input_data:
    count_ones = [a+(b == '1') for a, b in zip(count_ones, b)]
gamma = ''.join([str(1*(d > N/2)) for d in count_ones])
epsilon = ''.join([str(1*(d < N/2)) for d in count_ones])
answer = int(gamma, 2) * int(epsilon, 2)
```

### Part 2

The second part of the puzzle requires us to parse the diagnostic
report for 2 specific values.  These values are determined again by
parsing the frequency of digits in certain places.  Differing from
part 1, however, is that the values used to determine digit frequency
in one place must match the frequent digits from earlier places.  

Again, the solution that popped in my head at midnight was a little
clumsy.  I decided to use a
temporary list of the values to keep, and then overwrite it as we 
iterate through the digit places.  

```python
input_data = load_data()
input_data = input_data.splitlines()

ox = ''
for i in range(12):
    count_0 = 0
    count_1 = 0
    for b in input_data:
        if b[i] == '0':
            count_0 += 1
        if b[i] == '1':
            count_1 += 1
    if count_1 >= count_0:
        keep_digit = '1'
    else:
        keep_digit = '0'
    keep_list = []
    for b in input_data:
        if b[i] == keep_digit:
            keep_list.append(b)
    input_data = keep_list
    if len(input_data) == 1:
        ox = input_data[0]
        
input_data = load_data()
input_data = input_data.splitlines()

co2 = ''
for i in range(12):
    count_0 = 0
    count_1 = 0
    for b in input_data:
        if b[i] == '0':
            count_0 += 1
        if b[i] == '1':
            count_1 += 1
    if count_1 >= count_0:
        keep_digit = '0'
    else:
        keep_digit = '1'
    keep_list = []
    for b in input_data:
        if b[i] == keep_digit:
            keep_list.append(b)
    input_data = keep_list
    if len(input_data) == 1:
        co2 = input_data[0]

answer = int(ox, 2) * int(co2, 2)
```

Because I'm overwriting the `input_data` list, I have to load it a 
second time to find the second value!  *blech*  This could definitely 
be improved.  A first pass through the `input_data` could segregate
it into two lists of values that start with `0` and values that start
with `1`.  Then, those lists could be individually pared down to 
determine the `ox` and `co2` values.  Maybe I'll go back and update
this code someday...

## Day 4

### Part 1

BINGO!  The puzzle input is 2-part: a list of random integers (the
numbers called during Bingo), and a list of Bingo cards represented
by 5x5 arrays of `int`.  Each Bingo card is a 5-list of 5-list rows.  
When numbers are called out, matches on each card are replaced with 
`'X'`.  

To do that, I broke the functionality out into a `mark_bingo_card` 
function.  The function ingests the called number `n` and the card
`b` and returns the updated card.

```python
def mark_bingo_card(n, b):
    for i, row in enumerate(b):
        for j, item in enumerate(row):
            if item == n:
                row[j] = 'X'
    return b
```

Then, I need to check if a card is a winner.  This version of Bingo
only counts rows and columns as winners, so I'm looking for an
entire 5-list of `'X'`s.  Inside this same function, I can compute
the score of a winning card, which is specified to just be the sum
of all unmarked entries.

```python
def check_bingo_card(b):
    winning = False
    score = 0
    for row in b:
        if row == ['X', 'X', 'X', 'X', 'X']:
            winning = True
            break
    for col in range(5):
        if [row[col] for row in b] == ['X', 'X', 'X', 'X', 'X']:
            winning = True
            break
    if winning:
        for row in b:
            for item in row:
                if isinstance(item, int):
                    score += item
    return winning, score
```

For part 1, it's a simple matter of iterating over each drawn value,
and then iterating over each Bingo card.  I mark the cards, then 
check if they're winners.  I stopped when the first winner is hit
and use the score and drawn value to compute the answer.  

### Part 2

For part 2, we need to know the score and value for the _last_ card
that wins.  To do this, I iterate over each drawn value and each card.
I mark the cards, check for winners, and pop them out of the list of
cards.  Each time I find a winner, I write its score into the `answer`
variable.  Thus, that variable will hold the score of the whichever 
card is the last winner.

```python
for v in vals:
    winning_indices = []
    for i, b in enumerate(boards):
        b = mark_bingo_card(v, b)
        w, s = check_bingo_card(b)
        if w:
            answer = v * s
            winning_indices.append(i)
    if winning_indices:
        winning_indices.sort(reverse=True)
        for idx in winning_indices:
            boards.pop(idx)
```

## Day 5

### Parts 1 and 2

For this puzzle, we are presented with the locations of hydrothermal
vents on the ocean floor, in the format `'x0,y0 -> x1,y1'`.  We need
to find the `x,y` locations where 2 or more vents overlap.  

To do this, I'm going to create a `floor_map` dict whose keys are the
x,y grid locations and whose values are the number of vents at those
locations.  

For each vent, I'll extract the start/end locations and then march over
each grid location between them, incrementing the `floor_map`.  

```python
for line in input_data:
    start, end = line.split(' -> ')
    x0, y0 = list(map(int, start.split(',')))
    x1, y1 = list(map(int, end.split(',')))
    dx = 1 if x1 > x0 else 0 if x1 == x0 else -1
    dy = 1 if y1 > y0 else 0 if y1 == y0 else -1
    loc = (x0, y0)
    while True:
        if loc in floor_map:
            floor_map[loc] += 1
        else:
            floor_map[loc] = 1
        loc = (loc[0] + dx, loc[1] + dy)
        if loc == (x1, y1):
            if loc in floor_map:
                floor_map[loc] += 1
            else:
                floor_map[loc] = 1
            break
```

For Part 1, we only want to consider the horizontal and
vertical vents.  After computing `dx,dy` we can add a 
conditional like `if dx and dy: continue`, which will
advance to the next line of input if both `dx != 0` and `dy != 0`.

## Day 6

### Parts 1

In this puzzle, we need to study a population of fish that
periodically reproduce and produce more fish.  Each fish has an
int time-to-reproduce, which is specified in the puzzle input
for each of a list of fishies.  When a particular fish's timer
hits zero, its reproductive cycle restarts with `t=6` remaining,
as well as producing a juvenile fish that has `t=8`.  

For part 1, the quick-n-dirty process was to store the school of
fish as a list of their timers.  For each day that elapses, we
march the list and decrement all the timers.  When a timer would go
negative, it means that fish's timer should reset and a new juvenile
should be spawned/appended to the list.  

### Part 2

For part 2, we need to run the simulation for 256 days - doing it
manually would consume unreasonable amounts of time and RAM.  So,
we realize that we don't need to keep track of individual fish - 
simply tracking the populations of fish that share a certain timer
value is sufficient.  A list whose indices represent the timer values
and whose entries represent the populations is a great way of doing
this.  However, I decided to use a dict.  

```python
fish_timers = list(map(int, input_data[0].split(',')))

fish_populations = {i: 0 for i in range(9)}
for t in fish_timers:
    fish_populations[t] += 1

for g in range(256):
    aged_fish = {i-1: fish_populations[i] for i in range(1, 9)}
    repro_fish = fish_populations[0]
    aged_fish[6] += repro_fish
    aged_fish[8] = repro_fish
    fish_populations = aged_fish


answer = sum(fish_populations.values())
print(answer)
```
