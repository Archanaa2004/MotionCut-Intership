import random

adjectives = ["Adventurous","Creative","Bright","Fast","Smart","Beautiful","Active","Talent","Brave","Strong"]
nouns = ["Tiger","Parrot","Eagle","Queen","Princess","Dog","Lion","Peacock","Child","Monkey"]

def generate_username(include_numbers=False, include_special=False):
    username = random.choice(adjectives) + random.choice(nouns)
    if include_numbers:
        username += str(random.randint(10, 99))
    if include_special:
        username += random.choice("!@#$%&*")
    return username

def save_to_file(usernames):
    with open("usernames.txt", "a") as file:
        file.write("\n".join(usernames) + "\n")
    print("Usernames saved to 'usernames.txt'.")

def main():
    print("Welcome to the Random Username Generator!")
    while True:
        try:
            include_numbers = input("Include numbers in usernames? (yes/no): ").lower() in ["yes","y","Yes","Y","YES"]
            include_special = input("Include special characters in usernames? (yes/no): ").lower() in ["yes","y","Yes","Y","YES"]
            count = int(input("How many usernames would you like to generate? "))
            if count <= 0:
                raise ValueError("Count must be greater than 0.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue
        
        usernames = [generate_username(include_numbers, include_special) for _ in range(count)]
        print("\nGenerated Usernames:")
        print("\n".join(usernames))
        
        save_option = input("Do you want to save these usernames to a file? (yes/no): ").lower()
        if save_option in ["yes","y","Yes","Y","YES"]:
            save_to_file(usernames)
        
        again = input("Do you want to generate more usernames? (yes/no): ").lower()
        if again not in ["yes","y","Yes","Y","YES"]:
            print("Thank you for using the Random Username Generator!")
            break

if __name__ == "__main__":
    main()
