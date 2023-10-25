text_file = open("dorian.txt", 'r')

letter_occurence = {}
word_occurence = {}
word_length = {}
# A dictionary for storing the number of occurences of every letter

for line in text_file:
    # Delete unnecessary spaces and make text lowercase
    line = line.strip().lower()

    for letter in line:
        if letter not in letter_occurence:
            letter_occurence[letter] = 1
        else:
            letter_occurence[letter] += 1

    # Make a dictionary of words
    words = line.split()
    for word in words:
        word = word.strip(".,;:-'`\"?!()")
        if word not in word_occurence:
            word_occurence[word] = 1
        else:
            word_occurence[word] += 1

    # Make dictionary of words and their length
        if len(word) not in word_length:
            word_length[len(word)] = [word]
        else:
            word_length[len(word)].append(word)

text_file.close()

# Reversing the dictionary of letters

reverse_letter_occurence = {}

for letter, number in letter_occurence.items():
    if number not in reverse_letter_occurence:
        reverse_letter_occurence[number] = [letter]
    else:
        reverse_letter_occurence[number].append(letter)

# Reversing the dictionary of words

reverse_word_occurence = {}

for word, number in word_occurence.items():
    if number not in reverse_word_occurence:
        reverse_word_occurence[number] = [word]
    else:
        reverse_word_occurence[number].append(word)

# Print out the results

x = list(reverse_letter_occurence.items())
x.sort()
x.reverse()

y = list(reverse_word_occurence.items())
y.sort()
y.reverse()

z = list(word_length.items())
z.sort()
z.reverse()

limit = 5

# Results for letters
print("Letters statistics:\n")
print(f"- {limit} most common letters/chars\n")
for number, letter in x[:limit]:
    print(f"letter/char '{letter}' found {number} times,\n")

x.reverse()

print(f"- {limit} least common letters/chars\n")
for number, letter in x[:limit]:
    print(f"letter/char '{letter}' found {number} times,\n")

# Results for words
print("Words statistics\n")
print(f"- number of unique words: {len(word_occurence)}\n")

print(f"- {limit} most common words:\n")
for number, word in y[:limit]:
    print(f"word '{word}' found {number} times,\n")

print(f"- the longest words(with {limit} longest lengths) :\n")
for length, word in z[:limit]:
    print(f"words of length {length} are {word}\n")
