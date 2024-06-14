import bcrypt
import os
import readline
import glob
import time
import curses

# Enable tab completion
def complete_path(text, state):
    line = readline.get_line_buffer()
    return [x for x in glob.glob(os.path.expanduser(text) + '*')][state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)

# Function to crack bcrypt hash with curses for dynamic UI
def crack_bcrypt(stdscr, hashed_text, wordlist_path):
    curses.curs_set(0)
    stdscr.nodelay(1)
    
    # Read the wordlist file
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as file:
            wordlist = file.readlines()
    except FileNotFoundError:
        stdscr.addstr(1, 0, f"Wordlist file not found at path: {wordlist_path}")
        stdscr.refresh()
        time.sleep(2)
        return
    
    # Get the total number of words in the wordlist
    total_words = len(wordlist)
    
    # Convert the hashed text to bytes once
    hashed_bytes = hashed_text.encode()
    
    # Track start time
    start_time = time.time()
    
    # Iterate through each word in the wordlist and try to match the hash
    for index, word in enumerate(wordlist, start=1):
        word = word.strip()  # Remove newline characters
        if bcrypt.checkpw(word.encode(), hashed_bytes):
            stdscr.addstr(1, 0, f"Password cracked: {word}")
            stdscr.refresh()
            break
        
        # Calculate elapsed time and estimate remaining time
        elapsed_time = time.time() - start_time
        avg_time_per_attempt = elapsed_time / index
        remaining_attempts = total_words - index
        estimated_time_remaining = remaining_attempts * avg_time_per_attempt
        hours, rem = divmod(estimated_time_remaining, 3600)
        minutes, seconds = divmod(rem, 60)
        
        # Print verbose output for every attempt
        stdscr.addstr(0, 0, f"Attempt {index}/{total_words}: {word}")
        stdscr.addstr(2, 0, f"Estimated time remaining: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        stdscr.refresh()
        
        # Throttle output to avoid excessive CPU usage
        time.sleep(0.01)
    else:
        stdscr.addstr(1, 0, "Password not found in wordlist.")
        stdscr.refresh()
        time.sleep(2)

# Get the bcrypt hash from the user
hashed_text = input("Enter the bcrypt hash to crack: ")

# Get the path to the wordlist from the user
wordlist_path = input("Enter the path to the wordlist: ")

# Run the curses application
curses.wrapper(crack_bcrypt, hashed_text, wordlist_path)
