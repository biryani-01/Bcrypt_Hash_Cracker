import bcrypt

# Get the bcrypt hash from the user
hashed_text = input("Enter the bcrypt hash to crack: ")

# Get the path to the wordlist from the user
wordlist_path = input("Enter the path to the wordlist: ")

# Read the wordlist file
with open(wordlist_path, 'r', encoding='latin-1') as file:
    wordlist = file.readlines()

# Get the total number of words in the wordlist
total_words = len(wordlist)

# Iterate through each word in the wordlist and try to match the hash
for index, word in enumerate(wordlist, start=1):
    word = word.strip()  # Remove newline characters
    if bcrypt.checkpw(word.encode(), hashed_text.encode()):
        print(f"Password cracked: {word}")
        break
    else:
        print(f"Attempt {index}/{total_words}: {word}")

else:
    print("Password not found in wordlist.")
