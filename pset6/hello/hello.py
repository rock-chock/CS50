# Program that prints a greeting to a user

while True:
    name = input("What is your name?\n")
    if name.isalpha():
        print(f"hello, {name}")
        break
    else:
        print("Name should include only letters")