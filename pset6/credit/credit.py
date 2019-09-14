import sys

# Validate credit card number and output name of company


def main():

    # Possible names to label a card
    AMEX = "AMEX"
    MAST_C = "MASTERCARD"
    VISA = "VISA"
    MAST_C_OR_VISA = "MASTERCARD_OR_VISA"
    INVLD = "INVALID"

    # Ask for input at least once.
    while True:
        str_number = input("Input a credit card number\n")
        # Check for valid input
        if str_number.isdigit() == False:
            print("Only digits can be accepted")
        else:
            break


    # Standart first 2 digits of card number
    FIRST_2_AMEX = [34, 37]
    FIRST_2_MAST_C = list(range(51, 55+1))
    FIRST_2_VISA = list(range(40, 50))

    crd_first_2 = int(str_number[:2])

    # Check first 2 digits, define name if first two digits equal to standart case
    if crd_first_2 in FIRST_2_AMEX:
        name_first_2 = AMEX
    elif crd_first_2 in FIRST_2_MAST_C:
        name_first_2 = MAST_C
    elif crd_first_2 in FIRST_2_VISA:
        name_first_2 = VISA
    else:
        # Invalid case
        print(INVLD)
        sys.exit(0)


    # Standart length of credit card number
    LENGTH_AMEX = 15
    LENGTH_MAST_C_OR_VISA = 16
    LENGTH_VISA = 13

    crd_length = len(str_number)

    # Check length, exit if Define name if number fits in standarts
    if crd_length == LENGTH_AMEX:
        name_length = AMEX
    elif crd_length == LENGTH_MAST_C_OR_VISA:
        name_length = MAST_C_OR_VISA
    elif crd_length == LENGTH_VISA:
        name_length = VISA
    else:
        # Invalid case
        name_length = INVLD
        print(INVLD)
        sys.exit(0)


    # Check card number by Luhn's algorithm
    res_luhn = 0

    # Iterate over every other digit, starting with the number's second-to-last digit
    sum_mult_second = 0
    sum_first = 0
    for i in range(crd_length-2, -1, -2):
        mult_second = int(str_number[i]) * 2
        for digit in str(mult_second):
            sum_mult_second += int(digit)
        # Add not multiplied digits:
        sum_first += int(str_number[i-1])

    res_luhn = sum_mult_second + sum_first

    # Check if res_luhn's last digit is 0 and define company's name
    if (res_luhn % 10) == 0:
        if (name_length == MAST_C_OR_VISA and name_first_2 == MAST_C):
            print(MAST_C)
        elif ((name_length == MAST_C_OR_VISA or name_length == VISA) and name_first_2 == VISA):
            print(VISA)
        elif (name_length == AMEX and name_first_2 == AMEX):
            print(AMEX)
        else:
            print(INVLD)
    else:
        print(INVLD)


if __name__ == "__main__":
    main()