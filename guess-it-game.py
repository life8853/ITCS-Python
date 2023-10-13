import random

goal = random.randint(1, 100)

while True:
    guess = input("Guess the number: ")
    if not guess.isdigit():
        continue
    guess = int(guess)  # convert guess to

    if guess > goal:
        print("Too big")
    elif guess < goal:
        print("Too small")
    else:
        print("You guessed the number. Congratulations!")
        break
