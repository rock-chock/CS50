# Output 2 pyramids from Mario

# Get a number
while True:
    n_str = input("Input a number in range 1-8\n")

    # Check if n is a number and is in the valid range
    if n_str.isdigit() and 1 <= int(n_str) <= 8:
        n = int(n_str)
        break
    else:
        print("Input a valid number\n")

# Iterate over rows
for i in range(n):
    hashes = i + 1
    spaces = n - hashes

    # Iterate over columns
    print(f"{spaces * ' '}", end="")
    print(f"{hashes * '#'}", end="")
    print("  ", end="")
    print(f"{hashes * '#'}")