import math
import re
from collections import defaultdict
import os
from collections import Counter
import math
import chardet


def find_key_length(text):
    words = text.split()
    word_positions = defaultdict(list)

    # Track the positions of each word
    for index, word in enumerate(words):
        word_positions[word].append(index)

    # Take only repeating words, where length is greater than 1
    repeating_words = {word: positions for word, positions in word_positions.items() if len(positions) >= 1}
    # Filter those where length is greater than 3, so that the word with the most occurances is lenght of 3 (word "the")
    repeating_words = {word: positions for word, positions in repeating_words.items() if len(word) >= 3} # Might exclude

    starts = {}
    # Remove all non-alphabetic characters
    text_with_alphabetic = re.sub(r'[^a-zA-Z]', '', text)
    for word in repeating_words.keys():
        # Use regular expression to find all occurrences of the word
        pattern = re.compile(re.escape(word))
        for match in pattern.finditer(text_with_alphabetic):
            start = match.start()
            # for each word append start indices into dictonary
            if word in starts:
                starts[word].append(start)
            else:
                starts[word] = [start]

    # Find the word with the most occurrences
    max_key = None
    max_values_length = 0
    for key, values in starts.items():
        # Check if the current key has more values than the current max
        if len(values) > max_values_length:
            max_key = key
            max_values_length = len(values)

    # For the word with the most occurrences, find the distances between each pair of occurrences
    final_lengths = []
    for i in range(1, len(starts[max_key])):
        final_lengths.append(starts[max_key][i] - starts[max_key][i - 1])

    # Divide the final_lengths list into triplets and calculate the GCD of each triplet
    # List to store the results
    gcd_results = []
    # Iterate over the list in steps of 3
    for i in range(0, len(final_lengths) - len(final_lengths) % 3, 3):
        # Calculate GCD of the current triplet
        triplet_gcd = math.gcd(math.gcd(final_lengths[i], final_lengths[i+1]), final_lengths[i+2])
        # Append the result to the gcd_results list
        gcd_results.append(triplet_gcd)

    # Now find the most common number in the gcd_results list
    # Use Counter to count the occurrences of each number
    counter = Counter(gcd_results)
    # Find the number with the highest frequency
    most_common_number = counter.most_common(1)[0]
    # If the most common number is 1, take the second most common number => you cannot insert key of length 1
    if most_common_number[0] == 1:
        most_common_number = counter.most_common(2)[1]

    return most_common_number[0]

def frequency_analysis(text, gcd):
    # Remove non-alphabetic characters from the text
    text_with_alphabetic = re.sub(r'[^a-zA-Z]', '', text)

    # Initialize a list of 14 empty strings (blocks)
    blocks = [''] * gcd
    # Distribute characters into the correct blocks
    for i, char in enumerate(text_with_alphabetic):
        block_index = i % gcd
        blocks[block_index] += char

    # In each block find the most occured character
    most_common_chars = []
    for block in blocks:
        # Initialize a dictionary to store the number of occurrences of each character
        char_occurrences = {}
        for char in block:
            if char in char_occurrences:
                char_occurrences[char] += 1
            else:
                char_occurrences[char] = 1
        # Find the character with the most occurrences
        most_common_char = max(char_occurrences, key=char_occurrences.get)
        most_common_chars.append(most_common_char)
        
    # Each of the character of the alphabet has a number A = 0, B = 1, ..., Z = 25. Subtract 4 from all characters in the list
    adjusted_values = []
    for char in most_common_chars:
        # Convert character to numerical value (A=0, B=1, ..., Z=25)
        char_value = ord(char) - ord('A')
        # Subtract 4 and handle wrap-around using modulo 26
        adjusted_value = (char_value - 4) % 26
        # Convert numerical value back to character
        adjusted_char = chr(adjusted_value + ord('A'))
        adjusted_values.append(adjusted_char)

    # Join the adjusted characters into a single string
    result = ''.join(adjusted_values)
    return result

# Function to encrypt or decrypt text using the Vigenere cipher
def vigenere_cipher(text, key="", mode='encrypt'):
    final_text = []
    text_chars = list(text)
    non_alpha_count = 0
    # Iterate over each character in the text
    for i, char in enumerate(text_chars):
        # If the character is a letter, encrypt or decrypt it
        if char.isalpha():
            # Get the current key character
            current_key_char = key[(i - non_alpha_count) % len(key)]
            # Encrypt or decrypt the character
            if mode == 'encrypt':
                # Add the numerical values of the character and the key character, subtract 2 times the value of 'A' and take modulo 26
                new_char = (ord(char) + ord(current_key_char) - 2 * ord('A')) % 26
            else:
                # Subtract the numerical value of the key character from the numerical value of the character, add 26 and take modulo 26
                new_char = (ord(char) - ord(current_key_char)) % 26
            # Convert the numerical value back to a character and append it to the final text
            final_text.append(chr(new_char + ord('A')))
        # If the character is not a letter, append it to the final text without encrypting or decrypting it
        else:
            final_text.append(char)
            non_alpha_count += 1

    return ''.join(final_text)

# Function to read text from a file
def get_text_from_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    
    result = chardet.detect(raw_data)
    encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as file:
        return file.read().upper()

# Determine whether the user wants to encrypt or decrypt the text
mode = input('Encrypt or decrypt: ').lower()

# Ask the user if they want to take the text from a file
if mode == 'encrypt':
    use_file = input('Do you want to take the text from file "vigenere.txt"? (yes/no): ').lower()
else:
    use_file = input('Do you want to take the text from file "vigenere_encrypted.txt"? (yes/no): ').lower()

if use_file == 'yes':
    # Change the directory to the one where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if mode == 'encrypt':
        file_path = "vigenere.txt"
    else:
        file_path = "vigenere_encrypted.txt"
    text = get_text_from_file(file_path)
else:
    text = input('Enter the text: ').upper()

if mode == 'encrypt':
    key = input('Enter the key: ').upper()

if mode == "encrypt":
    result = vigenere_cipher(text, key, mode)
    if use_file == 'no':
        print(result)
    # Save the result to a file
    else:
        with open('vigenere_encrypted.txt', 'w') as file:
            file.write(result)
            print(f"Result saved to {os.path.abspath('vigenere_encrypted.txt')}")
elif mode == "decrypt":
    key_length = find_key_length(text)
    print(f"Key length: {key_length}")
    key = frequency_analysis(text, key_length)
    print(f"Key: {key}")
    result = vigenere_cipher(text, key, mode)
    if use_file == 'no':
        print(result)
    else:
        # Save the result to a file
        with open('vigenere_decrypted.txt', 'w') as file:
            file.write(result)
            print(f"Result saved to {os.path.abspath('vigenere_decrypted.txt')}")
else:
    print('Invalid mode. Please enter "encrypt" or "decrypt".')
