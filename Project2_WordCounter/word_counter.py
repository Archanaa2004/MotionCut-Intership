# Word Counter Program

def count_words(text):
    """
    Function to count the number of words in a given text.
    :param text: str, 
    :return: int, 
    """
    words = text.split()  
    return len(words)

def main():
    print("Welcome to the Word Counter Program!")
    while True:
        user_input = input("Enter a sentence or paragraph (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Thank you for using the Word Counter Program. Goodbye!")
            break
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        
        word_count = count_words(user_input)
        print(f"The total word count is: {word_count}")

if __name__ == "__main__":
    main()
