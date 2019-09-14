from sys import argv, exit

# ASSUME: in_file has 1 lowercase word per line, \n is in the end of the string
# ASSUME: input phrase doesn't contain punctuation marks


def main():
    # Exit if there are not 2 command-line arguments
    if len(argv) != 2:
        print(f"Usage: python bleep.py  dictionary")
        exit(1)

    # Load  from dict to a struct (set)
    in_dict = open(argv[1], "r")
    censored_dict = set()
    for line in in_dict:
        censored_dict.add(line.strip("\n"))
    in_dict.close()

    # Ask for user's input and tokenize it
    phrase_to_censor = input("What line would you like to censor?\n").split()

    # If any word from input phrase is in a dictionary, convert it to stars
    censored_res = ""
    for word in phrase_to_censor:
        if word.lower() in censored_dict:
            censored_res += f"{'*'*len(word)} "
        else:
            censored_res += f"{word} "
    print(censored_res)


if __name__ == "__main__":
    main()
