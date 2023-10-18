''' Experiments with Hailstone sequences '''


def next_hsn(c):
    ''' Return next hsn-number'''
    if c % 2 == 0:
        return c//2
    else:
        return 3*c+1


def hsn(c):
    ''' Return full hsn-sequence for seed c'''
    sequence = [c]
    while c > 1:
        c = next_hsn(c)
        sequence.append(c)
    return sequence


LIMIT = 1000

# Problem 1
length_of_longest_sequence = 1

for i in range(LIMIT+1):
    current_length = len(hsn(i))
    if current_length > length_of_longest_sequence:
        length_of_longest_sequence = current_length
        seed = i

print("Problem 1 (for range 1-1000): \n")
print(f"- longest sequence contains {length_of_longest_sequence} elements\n")
print(f"- starts from seed: {seed} \n")


# Problem 2

max_value = 1
times_found = 0
seeds = []
for i in range(LIMIT+1):
    current_max = max(hsn(i))
    if current_max > max_value:
        max_value = current_max
        times_found = 0
        seeds = []
    if current_max == max_value:
        times_found += 1
        seeds.append(i)

print("Problem 2 (for range 1-1000): \n")
print(f"- highest element value is {max_value}\n")
print(f"- found {times_found} times\n")
print(f"- in sequences starting from seeds: {seeds} times\n")

# Problem 3

all_lengths = []
unique_lengths = []
max_number_of_appearances = 0
common_length = 0
seeds = []

for i in range(LIMIT+1):
    all_lengths.append(len(hsn(i)))
    if unique_lengths.count(len(hsn(i))) == 0:
        unique_lengths.append(len(hsn(i)))

for unique_length in unique_lengths:
    number_of_appearances = all_lengths.count(unique_length)
    if max_number_of_appearances < number_of_appearances:
        max_number_of_appearances = number_of_appearances
        common_length = unique_length

for i, length in enumerate(all_lengths):
    if (length == common_length):
        seeds.append(i)

print("Problem 3 (for range 1-1000):\n")
print(f"- most common sequence length is {common_length}\n")
print(f"- found {max_number_of_appearances} times\n")
print(f"- in sequences starting from seeds: {seeds}")
