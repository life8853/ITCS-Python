# import the time library
import time
start = time.time()

PESEL_LENGTH = 11
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)
NUMBER_OF_DAYS_IN_A_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
YEAR_BY_YEAR_MODIFIER = (1900, 2000, 2100, 2200, 1800)


def date_check(pesel):
    # Check if the day is correct
    day = int(pesel[4:6])

    if day == 0:
        return False

    # check if the month if correct
    month = int(pesel[2:4])
    year_modifier = month // 20
    month %= 20

    if not (1 <= month <= 12):
        return False

    # calculate the whole year
    year = int(pesel[0:2]) + YEAR_BY_YEAR_MODIFIER[year_modifier]

    # check if the year is a leap year
    is_leap_year = 0

    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        is_leap_year = 1

    # check if the day digit is correct
    max_day = NUMBER_OF_DAYS_IN_A_MONTH[month - 1]
    if month == 2:
        max_day += is_leap_year

    if day > max_day:
        return False

    return True


def checksum(pesel):
    checksum = 0

    for i in range(PESEL_LENGTH - 1):
        checksum += PESEL_WEIGHT[i] * int(pesel[i])

    checksum = (10 - (checksum % 10)) % 10

    return checksum


# counters
total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = 0

file = open("1e6.dat", 'r')

# main processing loop
for pesel in file:
    pesel = pesel.strip()
    total += 1

    # 1) Check the length of the string
    if len(pesel) != PESEL_LENGTH:
        invalid_length += 1
        continue

    # 2) Check if the string is a digit
    if not pesel.isdigit():
        invalid_digit += 1
        continue

    # 3) Check if the date is correct
    if not date_check(pesel):
        invalid_date += 1
        continue

    # 4) Check if the checksum is correct
    checksum_pesel = int(pesel[10])

    if checksum(pesel) != checksum_pesel:
        invalid_checksum += 1
        continue

    # 5) Increment the correct counters
    correct += 1
    if int(pesel[9]) % 2 == 0:
        female += 1
    else:
        male += 1

file.close()

# show results
print(total, correct, female, male)
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)
print("Runtime =", time.time()-start, "s")
