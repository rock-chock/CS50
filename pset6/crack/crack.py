# Decrypt passwords that were hashed with Python hash() function

import string
from crypt import crypt
import sys

# ASSUME: passwords are no longer than five (5) characters
# ASSUME: each password is composed of alphabetical characters only


def main():

    # Check if there are only 2 command line arguments: name of file and hash
    if len(sys.argv) != 2:
        print("Usage: python3 crack.py hashed_password")
        sys.exit(1)

    # Get hash and salt[]
    hashed_pwd = sys.argv[1]
    salt = hashed_pwd[:2]

    # Use dictionary to find crack
    if search_dict(hashed_pwd, salt) == None:
        # Use brute force loops to find crack
        print("Couldn't find in dictionary. Starting brute force looping")
        crack = brute_force(hashed_pwd, salt)
        if crack == None:
            print("Password is something other than sequence of 1-5 letters")


# Use dictionary of pwd: hash to find
def search_dict(hashed_pwd, salt):
    # Load dictionary to memory
    in_file = open("dictionary", "r")
    dictionary = {}
    for line in in_file:
        key = line.rstrip("\n")
        dictionary[key] = crypt(key, salt)
    in_file.close()

    # Try to find a hash in dictionary
    for key_pwd, value_hash in dictionary.items():
        if value_hash == hashed_pwd:
            print(key_pwd)
            sys.exit(0)

    return None


# Check hashes of letter combinations from "a" to "ZZZZZ" for equality with given hash
def brute_force(hashed_pwd, salt):
    # Use English Letter Frequency sequence of letters
    # http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    ascii = [""] + list("eEtTaAoOiInNsSrRhHdDlLuUcCmMfFyYwWgGpPbBvVkKxXqQjJzZ")
    steps = len(ascii)
    test_list = ["", "", "", "", ""]

    for i in range(steps):
        # If index is 0 and next letter is "Z" - advance current index to skip element "".
        if i == 0 and test_list[1] == "Z":
            i += 1
        test_list[0] = ascii[i]

        for j in range(steps):
            if j == 0 and test_list[2] == "Z":
                j += 1
            test_list[1] = ascii[j]

            for k in range(steps):
                if k == 0 and test_list[3] == "Z":
                    k += 1
                test_list[2] = ascii[k]

                for l in range(steps):
                    if l == 0 and test_list[4] == "Z":
                        l += 1
                    test_list[3] = ascii[l]

                    for m in range(steps):
                        test_list[4] = ascii[m]

                        # Check if found crack
                        if is_crack(hashed_pwd, test_list, salt) == True:
                            print("".join(test_list))
                            sys.exit(0)
    return None


# Check if test password equals to hash from command line
def is_crack(hashed_pwd, test_list, salt):

    test_pwd = "".join(test_list)
    test_hash = crypt(test_pwd, salt)
    if test_hash != hashed_pwd:
        return False
    return True


if __name__ == "__main__":
    main()