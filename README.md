# Advent of Code 2021

Code + writeups for AoC 2021!

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
