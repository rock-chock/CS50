# Decrypt passwords that were hashed by crypt() function

from crypt import crypt
import sys

# ASSUME: passwords are no longer than five (5) characters
# ASSUME: each password is composed entirely of alphabetical characters

def main():

    # List of tuples(login, hashed_pwds) provided by cs50 docs
    # https://docs.cs50.net/2019/x/psets/6/sentimental/crack/crack.html
    pwds_and_hashes = [
        ("brian", "51.xJagtPnb6s"),
        #("bjbrown", "50GApilQSG3E2"),
        ("emc", "502sDZxA/ybHs"),
        ("greg", "50C6B0oz0HWzo"),
        ("jana", "50WUNAFdX/yjA"),
        ("lloyd", "50n0AAUD.pL8g"),
        ("malan", "50CcfIk1QrPr6"),
        ("natmelo", "50JIIyhDORqMU"),
        ("rob", "51v3Nh6ZWGHOQ"),
        ("veronica", "61v1CDwwP95bY"),
        ("walker", "508ny6Rw0aRio"),
        ("zamyla", "50cI2vYkF0YU2")
        ]

    out_file = open("cracked", "w")

    # Crack each element in the list
    for i in range(len(pwds_and_hashes)):
        # Get hashed_pwd and salt for c
        hashed_pwd = pwds_and_hashes[i][1]
        salt = hashed_pwd[:2]
        out_file.write(f"{pwds_and_hashes[i][0]}: {hashed_pwd}: ")

        # Use dictionary to find cracking password
        res_from_dict = search_dict(hashed_pwd, salt)
        if res_from_dict == None:
            # Use brute force loop
            res_from_loops = brute_force(hashed_pwd, salt)
            if res_from_loops == None:
                print("Password is something other than 1-5 letters")
            else:
                out_file.write(f"{res_from_loops}\n")
        else:
            out_file.write(f"{res_from_dict}\n")

        out_file.write("\n")

    out_file.close()


# Use dictionary of pwd: hash to find
def search_dict(hashed_pwd, salt):
    # Load dictionary to memory
    in_file = open("dictionary", "r")
    dict_for_cracking = {}
    for line in in_file:
        key = line.rstrip("\n")
        dict_for_cracking[key] = crypt(key, salt)
    in_file.close()

    # Try to find a hash in dictionary
    for key_pwd, value_hash in dict_for_cracking.items():
        if value_hash ==  hashed_pwd:
            return key_pwd

    return None


# Check hashes of letter combinations from "a" to "ZZZZZ" for equality with given hash
def brute_force(hashed_pwd, salt):
    # Starting values
    # Use English Letter Frequency sequence of letters
    # http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    # Empty element is for the starting values
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
                        if is_cracked(hashed_pwd, test_list, salt) == True:
                            return "".join(test_list)

                        # If not found, advance item to the next letter
    return None


# Check if test password equals to hash from command line
def is_cracked(hashed_pwd, test_list, salt):
    test_pwd = "".join(test_list)
    test_hash = crypt(test_pwd, salt)
    if test_hash != hashed_pwd:
        return False
    return True


if __name__ == "__main__":
    main()