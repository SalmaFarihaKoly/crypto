def caesar_encrypt(plaintext, shift):
    """
    Encrypts the plaintext using the Caesar Cipher technique.
    """
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            start = ord('A') if char.isupper() else ord('a')
            
            # Apply the shift with modulo 26
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += shifted_char
        else:
            # Keep non-alphabetic characters (spaces, numbers, punctuation) unchanged
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    """
    Decrypts the ciphertext using a known shift key.
    """
    return caesar_encrypt(ciphertext, -shift)

def brute_force_attack(ciphertext):
    """
    Performs a brute-force analysis by attempting every possible shift (1-25).
    """
    print(f"\n--- Brute Force Analysis for Ciphertext: '{ciphertext}' ---")
    # Try every possible key from 1 to 25
    for key in range(1, 26):
        decrypted_attempt = caesar_decrypt(ciphertext, key)
        print(f"Key #{key:02}: {decrypted_attempt}")
    print("-------------------------------------------------------")

# --- Main Execution Block ---
if __name__ == "__main__":
    print("=== Caesar Cipher Tool ===")
    
    # 1. Take User Input
    user_message = input("Enter the message to encrypt: ")
    
    # Input validation for the key to ensure it's a number
    while True:
        try:
            user_key = int(input("Enter the shift key (1-25): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # 2. Perform Encryption
    encrypted_msg = caesar_encrypt(user_message, user_key)
    print(f"\n[+] Encrypted Result: {encrypted_msg}")

    # 3. Perform Decryption (Verification)
    # We decrypt the result just to prove the math works
    decrypted_verification = caesar_decrypt(encrypted_msg, user_key)
    print(f"[+] Decryption Check: {decrypted_verification}")

    # 4. Study: Brute-Force Attack
    # Now we simulate an attacker who intercepted 'encrypted_msg'
    print("\n[!] Simulating Brute-Force Attack on your message...")
    input("Press Enter to start the attack...")
    brute_force_attack(encrypted_msg)
    
    
    import numpy as np
import math

# Helper dictionaries mapping characters to indices and vice versa
chr_to_idx = {chr(i + 65): i for i in range(26)}
idx_to_chr = {i: chr(i + 65) for i in range(26)}

def text_to_matrix(text, m):
    text = text.upper().replace(" ", "") 
    remainder = len(text) % m
    if remainder != 0:
        padding_needed = m - remainder
        text += 'X' * padding_needed 
        print(f"[*] Padding added: {'X' * padding_needed}")
    numeric_text = [chr_to_idx[char] for char in text]
    return np.array(numeric_text).reshape(-1, m)

def matrix_mod_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix))) 
    try:
        det_inv = pow(det, -1, modulus)
    except ValueError:
        raise ValueError("The determinant has no modular inverse. This key is invalid!")

    matrix_inv = np.linalg.inv(matrix)
    adjugate = matrix_inv * det
    return (det_inv * np.round(adjugate)).astype(int) % modulus

def generate_random_key(m):
    while True:
        random_matrix = np.random.randint(0, 26, (m, m))
        det = int(np.round(np.linalg.det(random_matrix))) % 26
        if math.gcd(det, 26) == 1:
            return random_matrix

# ==========================================
# Step-by-Step Encryption
# ==========================================
def hill_encrypt_verbose(plaintext, key_matrix):
    m = key_matrix.shape[0] 
    plaintext_matrix = text_to_matrix(plaintext, m)
    
    encrypted_text = ""
    print("\n--- Encryption Steps (Block by Block) ---")
    
    for i, block in enumerate(plaintext_matrix):
        # 1. Show the characters in the current block
        block_chars = "".join([idx_to_chr[num] for num in block])
        print(f"Step {i+1}: Block '{block_chars}' -> Numerical Vector: {block}")
        
        # 2. Raw Matrix Multiplication
        raw_dot = np.dot(block, key_matrix)
        print(f"   -> Math: {block} x Key Matrix = {raw_dot}")
        
        # 3. Apply Modulo 26
        encrypted_block = raw_dot % 26
        print(f"   -> Modulo 26: {raw_dot} % 26 = {encrypted_block}")
        
        # 4. Convert back to characters
        enc_chars = "".join([idx_to_chr[num] for num in encrypted_block])
        print(f"   -> Resulting Cipher Block: {encrypted_block} -> '{enc_chars}'\n")
        
        encrypted_text += enc_chars
        
    return encrypted_text

# ==========================================
# Step-by-Step Decryption
# ==========================================
def hill_decrypt_verbose(ciphertext, key_matrix):
    m = key_matrix.shape[0]
    try:
        inverse_key = matrix_mod_inverse(key_matrix, 26)
        print(f"\n[+] Calculated Inverse Key Matrix for Decryption:\n{inverse_key}")
    except ValueError as e:
        return str(e)

    ciphertext_matrix = text_to_matrix(ciphertext, m)
    
    decrypted_text = ""
    print("\n--- Decryption Steps (Block by Block) ---")
    
    for i, block in enumerate(ciphertext_matrix):
        block_chars = "".join([idx_to_chr[num] for num in block])
        print(f"Step {i+1}: Cipher Block '{block_chars}' -> Vector: {block}")
        
        raw_dot = np.dot(block, inverse_key)
        print(f"   -> Math: {block} x Inverse Matrix = {raw_dot}")
        
        decrypted_block = raw_dot % 26
        print(f"   -> Modulo 26: {raw_dot} % 26 = {decrypted_block}")
        
        dec_chars = "".join([idx_to_chr[num] for num in decrypted_block])
        print(f"   -> Resulting Plain Block: {decrypted_block} -> '{dec_chars}'\n")
        
        decrypted_text += dec_chars
        
    return decrypted_text

# --- Main Execution Block ---
if __name__ == "__main__":
    print("=== Hill Cipher Step-by-Step Visualizer ===")
    
    message = input("Enter your message (e.g., PAYMOREMONEY): ")
    
    print("\n1. Use the Given Key (3x3)")
    print("2. Generate a Random Key")
    choice = input("Choice (1 or 2): ")
    
    if choice == '1':
        key = np.array([
            [17, 17, 5],
            [21, 18, 21],
            [2, 2, 1]
        ])
    else:
        m_size = int(input("Enter matrix size (e.g., 3 for Trigraphs, 2 for Digraphs): "))
        key = generate_random_key(m_size)
        
    print(f"\n[+] Active Key Matrix:\n{key}")
    
    # Run Encrypt
    cipher = hill_encrypt_verbose(message, key)
    print(f"[FINAL] Encrypted Output: {cipher}")

    # Run Decrypt
    original = hill_decrypt_verbose(cipher, key)
    print(f"[FINAL] Decrypted Output: {original}")
    
    
    # ==========================================
# 1. 5x5 Matrix Generation
# ==========================================
def create_matrix(key):
    # Convert to uppercase and replace J with I
    key = key.upper().replace("J", "I")
    matrix_chars = []
    
    # Add unique characters from the key
    for char in key:
        if char.isalpha() and char not in matrix_chars:
            matrix_chars.append(char)
            
    # Add the remaining letters of the alphabet (excluding J)
    for ascii_val in range(65, 91):  # A to Z
        char = chr(ascii_val)
        if char == "J":
            continue
        if char not in matrix_chars:
            matrix_chars.append(char)
            
    # Convert the 1D list into a 5x5 2D matrix
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(matrix_chars[i:i+5])
        
    return matrix

# ==========================================
# 2. Text Preparation (Digraphs & Padding)
# ==========================================
def prepare_text(text):
    text = text.upper().replace("J", "I")
    clean_text = ""
    
    # Remove spaces and non-alphabetic characters
    for char in text:
        if char.isalpha():
            clean_text += char
            
    prepared_text = ""
    i = 0
    # Create pairs (digraphs)
    while i < len(clean_text):
        char1 = clean_text[i]
        char2 = ""
        
        if i + 1 < len(clean_text):
            char2 = clean_text[i+1]
            
        # Rule: If both letters in a pair are the same, insert 'X'
        if char1 == char2:
            prepared_text += char1 + "X"
            i += 1  # Process only the first character, 'char2' will be used in the next pair
        else:
            if char2 != "":
                prepared_text += char1 + char2
                i += 2  # Move to the next pair
            else:
                # Odd length text, pad with 'X' at the end
                prepared_text += char1 + "X"
                i += 1
                
    return prepared_text

# ==========================================
# 3. Helper: Find position in matrix
# ==========================================
def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return -1, -1

# ==========================================
# 4. Core Encryption & Decryption Logic
# ==========================================
def playfair_process(text, matrix, mode="encrypt"):
    result = ""
    # Shift right/down for encrypt (+1), left/up for decrypt (-1)
    shift = 1 if mode == "encrypt" else -1
    
    for i in range(0, len(text), 2):
        char1 = text[i]
        char2 = text[i+1]
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        # Rule 1: Same Row -> Shift right (or left if decrypting)
        if row1 == row2:
            result += matrix[row1][(col1 + shift) % 5]
            result += matrix[row2][(col2 + shift) % 5]
            
        # Rule 2: Same Column -> Shift down (or up if decrypting)
        elif col1 == col2:
            result += matrix[(row1 + shift) % 5][col1]
            result += matrix[(row2 + shift) % 5][col2]
            
        # Rule 3: Rectangle -> Swap columns
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]
            
    return result

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    print("=== Playfair Cipher Tool ===")
    key = input("Enter Keyword: ")
    message = input("Enter Message: ")
    
    # 1. Generate Matrix
    matrix = create_matrix(key)
    print("\n[+] 5x5 Key Matrix:")
    for row in matrix:
        print(" ".join(row))
        
    # 2. Prepare Text
    prepared_msg = prepare_text(message)
    print(f"\n[+] Prepared Plaintext (Pairs): {prepared_msg}")
    
    # 3. Encrypt
    encrypted_msg = playfair_process(prepared_msg, matrix, mode="encrypt")
    print(f"[+] Encrypted Ciphertext: {encrypted_msg}")
    
    # 4. Decrypt
    decrypted_msg = playfair_process(encrypted_msg, matrix, mode="decrypt")
    print(f"[+] Decrypted Message: {decrypted_msg}")
    
    
# ==========================================
# 1. 5x5 Matrix Generation
# ==========================================
def create_matrix(key):
    # Convert to uppercase and replace J with I
    key = key.upper().replace("J", "I")
    matrix_chars = []
    
    # Add unique characters from the key
    for char in key:
        if char.isalpha() and char not in matrix_chars:
            matrix_chars.append(char)
            
    # Add the remaining letters of the alphabet (excluding J)
    for ascii_val in range(65, 91):  # A to Z
        char = chr(ascii_val)
        if char == "J":
            continue
        if char not in matrix_chars:
            matrix_chars.append(char)
            
    # Convert the 1D list into a 5x5 2D matrix
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(matrix_chars[i:i+5])
        
    return matrix

# ==========================================
# 2. Text Preparation (Digraphs & Padding)
# ==========================================
def prepare_text(text):
    text = text.upper().replace("J", "I")
    clean_text = ""
    
    # Remove spaces and non-alphabetic characters
    for char in text:
        if char.isalpha():
            clean_text += char
            
    prepared_text = ""
    i = 0
    # Create pairs (digraphs)
    while i < len(clean_text):
        char1 = clean_text[i]
        char2 = ""
        
        if i + 1 < len(clean_text):
            char2 = clean_text[i+1]
            
        # Rule: If both letters in a pair are the same, insert 'X'
        if char1 == char2:
            prepared_text += char1 + "X"
            i += 1  # Process only the first character, 'char2' will be used in the next pair
        else:
            if char2 != "":
                prepared_text += char1 + char2
                i += 2  # Move to the next pair
            else:
                # Odd length text, pad with 'X' at the end
                prepared_text += char1 + "X"
                i += 1
                
    return prepared_text

# ==========================================
# 3. Helper: Find position in matrix
# ==========================================
def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return -1, -1

# ==========================================
# 4. Core Encryption & Decryption Logic
# ==========================================
def playfair_process(text, matrix, mode="encrypt"):
    result = ""
    # Shift right/down for encrypt (+1), left/up for decrypt (-1)
    shift = 1 if mode == "encrypt" else -1
    
    for i in range(0, len(text), 2):
        char1 = text[i]
        char2 = text[i+1]
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        # Rule 1: Same Row -> Shift right (or left if decrypting)
        if row1 == row2:
            result += matrix[row1][(col1 + shift) % 5]
            result += matrix[row2][(col2 + shift) % 5]
            
        # Rule 2: Same Column -> Shift down (or up if decrypting)
        elif col1 == col2:
            result += matrix[(row1 + shift) % 5][col1]
            result += matrix[(row2 + shift) % 5][col2]
            
        # Rule 3: Rectangle -> Swap columns
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]
            
    return result

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    print("=== Playfair Cipher Tool ===")
    key = input("Enter Keyword: ")
    message = input("Enter Message: ")
    
    # 1. Generate Matrix
    matrix = create_matrix(key)
    print("\n[+] 5x5 Key Matrix:")
    for row in matrix:
        print(" ".join(row))
        
    # 2. Prepare Text
    prepared_msg = prepare_text(message)
    print(f"\n[+] Prepared Plaintext (Pairs): {prepared_msg}")
    
    # 3. Encrypt
    encrypted_msg = playfair_process(prepared_msg, matrix, mode="encrypt")
    print(f"[+] Encrypted Ciphertext: {encrypted_msg}")
    
    # 4. Decrypt
    decrypted_msg = playfair_process(encrypted_msg, matrix, mode="decrypt")
    print(f"[+] Decrypted Message: {decrypted_msg}")
    
def xor_string(s1: str, s2: str) -> str:
    """XORs two strings of equal length character by character and returns the new string."""
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def pad_data(text: str, block_size: int = 8) -> str:
    """Pads the plaintext with 'X' to ensure its length is a multiple of the block size."""
    if len(text) % block_size == 0:
        return text
    pad_len = block_size - (len(text) % block_size)
    return text + ('X' * pad_len)

# ==========================================
# CBC Mode Encryption & Decryption
# ==========================================

def cbc_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_block = iv
    
    print("\n--- Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # Step 1: XOR plaintext block with IV or previous ciphertext block
        xored_with_prev = xor_string(p_block, prev_block)
        
        # Step 2: "Encrypt" by XORing with the Key
        c_block = xor_string(xored_with_prev, key)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # Save the current ciphertext block to use in the next round
        prev_block = c_block 
        
    return cipher_blocks

def cbc_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_block = iv
    
    print("\n--- Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # Step 1: "Decrypt" by XORing with the Key
        decrypted_step = xor_string(c_block, key)
        
        # Step 2: XOR with IV or previous ciphertext block to recover the original plaintext
        p_block = xor_string(decrypted_step, prev_block)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # Save the current ciphertext block to use in the next round
        prev_block = c_block 
        
    # Remove the 'X' padding characters at the end to return the actual original plaintext
    return plaintext.rstrip('X')

# ==========================================
# ECB Mode Encryption & Decryption
# ==========================================

def ecb_encrypt(plaintext: str, key: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    
    print("\n--- ECB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ECB-তে সরাসরি Key দিয়ে XOR করা হয় (কোনো IV লাগে না)
        c_block = xor_string(p_block, key)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
    return cipher_blocks

def ecb_decrypt(cipher_blocks: list, key: str) -> str:
    plaintext = ""
    
    print("\n--- ECB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ECB-তে সরাসরি Key দিয়ে XOR করলেই প্লেইনটেক্সট পাওয়া যায়
        p_block = xor_string(c_block, key)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
    return plaintext.rstrip('X')

# ==========================================
# CFB Mode Encryption & Decryption
# ==========================================

def cfb_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_block = iv # শুরুতে IV দিয়ে কাজ শুরু হয়
    
    print("\n--- CFB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ধাপ ১: আগের সাইফার ব্লক (বা IV) কে Key দিয়ে "Encrypt" করা হয়
        encrypted_prev = xor_string(prev_block, key)
        
        # ধাপ ২: সেই এনক্রিপ্টেড রেজাল্টের সাথে বর্তমান প্লেইনটেক্সট XOR করা হয়
        c_block = xor_string(p_block, encrypted_prev)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # পরবর্তী ব্লকের জন্য বর্তমান সাইফার ব্লককে সেভ করা হয়
        prev_block = c_block
        
    return cipher_blocks

def cfb_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_block = iv
    
    print("\n--- CFB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ধাপ ১: আগের সাইফার ব্লক (বা IV) কে Key দিয়ে "Encrypt" করা হয় (ঠিক এনক্রিপশনের মতো)
        encrypted_prev = xor_string(prev_block, key)
        
        # ধাপ ২: সেই রেজাল্টের সাথে বর্তমান সাইফার ব্লক XOR করলে প্লেইনটেক্সট পাওয়া যায়
        p_block = xor_string(c_block, encrypted_prev)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # পরবর্তী ব্লকের জন্য বর্তমান সাইফার ব্লককে সেভ করা হয়
        prev_block = c_block
        
    return plaintext.rstrip('X')


# ==========================================
# OFB Mode Encryption & Decryption
# ==========================================

def ofb_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_output = iv # এখানে আউটপুট ফিডব্যাক হিসেবে কাজ করে
    
    print("\n--- OFB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ধাপ ১: আগের আউটপুটকে (বা IV) Key দিয়ে এনক্রিপ্ট করে "Keystream" তৈরি করা হয়
        keystream_block = xor_string(prev_output, key)
        
        # ধাপ ২: সেই Keystream-এর সাথে প্লেইনটেক্সট XOR করে সাইফার তৈরি করা হয়
        c_block = xor_string(p_block, keystream_block)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # পরবর্তী রাউন্ডের জন্য "এনক্রিপশন আউটপুট" সেভ করা হয় (সাইফারটেক্সট নয়!)
        prev_output = keystream_block
        
    return cipher_blocks

def ofb_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_output = iv
    
    print("\n--- OFB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ধাপ ১: একই ভাবে Keystream তৈরি করা হয়
        keystream_block = xor_string(prev_output, key)
        
        # ধাপ ২: সাইফারের সাথে Keystream XOR করলে প্লেইনটেক্সট ফিরে আসে
        p_block = xor_string(c_block, keystream_block)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # ফিডব্যাক হিসেবে আউটপুট আপডেট করা হয়
        prev_output = keystream_block
        
    return plaintext.rstrip('X')

# ==========================================
# CTR Mode Encryption & Decryption
# ==========================================

def ctr_encrypt(plaintext: str, key: str, nonce: str, block_size: int = 8) -> list:
    # CTR একটি স্ট্রিম সাইফার মোড বলে এতে প্যাডিং বাধ্যতামূলক নয়, 
    # তবে আমরা ব্লক অনুযায়ী দেখানোর জন্য প্যাড করে নিচ্ছি।
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    counter = 0 
    
    print("\n--- CTR Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ১. কাউন্টার ব্লক তৈরি (Nonce + Counter)
        # এখানে Nonce এবং Counter-কে মিলিয়ে একটি ৮-অক্ষরের ব্লক বানানো হচ্ছে
        counter_block = (nonce + str(counter).zfill(8-len(nonce)))[:block_size]
        
        # ২. কাউন্টার ব্লককে Key দিয়ে এনক্রিপ্ট করে Keystream তৈরি করা
        keystream = xor_string(counter_block, key)
        
        # ৩. প্লেইনটেক্সট ব্লকের সাথে Keystream XOR করা
        c_block = xor_string(p_block, keystream)
        
        cipher_blocks.append(c_block)
        print(f"Counter {counter} ('{counter_block}') -> C{(i//block_size)+1}: '{c_block}'")
        
        # কাউন্টার ১ বাড়িয়ে দেওয়া (এটিই পরের ব্লকের ইনপুট)
        counter += 1
        
    return cipher_blocks

def ctr_decrypt(cipher_blocks: list, key: str, nonce: str, block_size: int = 8) -> str:
    # এখানে block_size: int = 8 যোগ করা হয়েছে যাতে ফাংশনটি এটি চিনতে পারে
    plaintext = ""
    counter = 0
    
    print("\n--- CTR Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # এখন block_size চিনতে পারায় আর NameError আসবে না
        counter_block = (nonce + str(counter).zfill(8-len(nonce)))[:block_size]
        keystream = xor_string(counter_block, key)
        
        p_block = xor_string(c_block, keystream)
        
        plaintext += p_block
        print(f"C{i+1} XOR Keystream_{counter} -> P{i+1}: '{p_block}'")
        counter += 1
        
    return plaintext.rstrip('X')
# ==========================================
# Main Program (User Input Mode)
# ==========================================
def get_user_input(prompt: str, default_val: str) -> str:
    """Function to take user input. Uses the default value if the user just presses Enter."""
    user_val = input(f"{prompt} (Default: '{default_val}'): ")
    return user_val if user_val else default_val

if __name__ == "__main__":
    print("=========================================")
    print("      CBC Mode XOR Encryption Tool       ")
    print("=========================================\n")
    print("Instructions: Provide your data below. To use the assignment's default data, just press Enter.\n")

    # Take user input
    plaintext = get_user_input("Enter Plaintext", "ICEDEPT@RU")
    
    # IV and Key must be exactly 8 characters
    while True:
        iv = get_user_input("Enter 8-character IV", "ABCDEFGH")
        if len(iv) == 8: break
        print("Invalid input! IV must be exactly 8 characters long.")
        
    while True:
        key = get_user_input("Enter 8-character Key", "12345678")
        if len(key) == 8: break
        print("Invalid input! Key must be exactly 8 characters long.")
    
    print("\n[Input Summary]")
    print(f"Plaintext : {plaintext}")
    print(f"IV        : {iv}")
    print(f"Key       : {key}")
    
    # 1. Encryption
    encrypted_blocks = cbc_encrypt(plaintext, key, iv)
    print("\n[Final Encrypted Output]")
    for i, block in enumerate(encrypted_blocks):
        print(f"C{i+1} = \"{block}\"")
        
    # 2. Decryption
    decrypted_text = cbc_decrypt(encrypted_blocks, key, iv)
    print(f"\n[Final Decrypted Output]")
    print(f"Recovered Plaintext: {decrypted_text}")
    
    # ------------------------------------------
    # ECB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing ECB Mode ")
    print("="*20)

    # 1. ECB Encryption
    ecb_encrypted = ecb_encrypt(plaintext, key)
    
    # 2. ECB Decryption
    ecb_decrypted = ecb_decrypt(ecb_encrypted, key)
    print(f"\n[ECB Final Output] Recovered: {ecb_decrypted}")
    
    # ------------------------------------------
    # CFB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing CFB Mode ")
    print("="*20)

    # 1. CFB Encryption
    cfb_encrypted = cfb_encrypt(plaintext, key, iv)
    
    # 2. CFB Decryption
    cfb_decrypted = cfb_decrypt(cfb_encrypted, key, iv)
    print(f"\n[CFB Final Output] Recovered: {cfb_decrypted}")
    
    # ------------------------------------------
    # OFB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing OFB Mode ")
    print("="*20)

    # 1. OFB Encryption
    ofb_encrypted = ofb_encrypt(plaintext, key, iv)
    
    # 2. OFB Decryption
    ofb_decrypted = ofb_decrypt(ofb_encrypted, key, iv)
    print(f"\n[OFB Final Output] Recovered: {ofb_decrypted}")
    
    # ------------------------------------------
    # CTR Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing CTR Mode ")
    print("="*20)

    nonce = "ABC" # ৩ অক্ষরের নন্স, বাকি ৫ ঘর কাউন্টার দিয়ে পূরণ হবে
    
    # 1. CTR Encryption
    ctr_encrypted = ctr_encrypt(plaintext, key, nonce)
    
    # 2. CTR Decryption
    ctr_decrypted = ctr_decrypt(ctr_encrypted, key, nonce)
    print(f"\n[CTR Final Output] Recovered: {ctr_decrypted}")
    
import random
import math

# ==========================================
# 1. Miller-Rabin Primality Test
# ==========================================
def miller_rabin_test(n, k_iterations=5):
    """
    Checks if a number is prime using the Miller-Rabin probabilistic test.
    """
    # Basic edge cases
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n <= 1: return False

    # Step 1: Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Step 2: Witness Loop
    for _ in range(k_iterations):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d % n

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite
            
    return True  # Probably Prime

# ==========================================
# 2. Extended Euclidean Algorithm
# ==========================================
def extended_gcd(a, b):
    """
    Returns (g, x, y) such that ax + by = g = gcd(a, b).
    This is used to find the modular inverse.
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(e, phi):
    """
    Calculates d such that (d * e) % phi == 1 using Extended Euclidean Algo.
    """
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist (e and phi are not coprime)')
    else:
        # Ensure result is positive
        return (x % phi + phi) % phi

# ==========================================
# 3. Encryption & Decryption Functions
# ==========================================
def encrypt(message, public_key):
    e, n = public_key
    cipher_ints = []
    
    for char in message:
        m = ord(char)  # Convert char to ASCII integer
        
        # Check if n is large enough
        if m >= n:
            raise ValueError(f"Error: n ({n}) is too small to encrypt character '{char}' ({m}). Choose larger primes.")
            
        # Formula: c = m^e mod n
        c = pow(m, e, n)
        cipher_ints.append(c)
        
    return cipher_ints

def decrypt(cipher_ints, private_key):
    d, n = private_key
    decrypted_msg = ""
    
    for c in cipher_ints:
        # Formula: m = c^d mod n
        m = pow(c, d, n)
        decrypted_msg += chr(m)  # Convert integer back to char
        
    return decrypted_msg

# ==========================================
# 4. Main Execution
# ==========================================
if __name__ == "__main__":
    print("=== RSA Implementation (Miller-Rabin & Extended Euclidean) ===\n")

    try:
        # --- Step 1: Input Primes ---
        print("--- Key Generation ---")
        p = int(input("Enter Prime Number p: "))
        q = int(input("Enter Prime Number q: "))

        # Check Primes using Miller-Rabin
        if not miller_rabin_test(p):
            print(f"Error: {p} is NOT a prime number!")
            exit()
        if not miller_rabin_test(q):
            print(f"Error: {q} is NOT a prime number!")
            exit()
        if p == q:
            print("Error: p and q must be different!")
            exit()

        # --- Step 2: Calculate n and phi ---
        n = p * q
        phi = (p - 1) * (q - 1)
        print(f"Calculated n = {n}")
        print(f"Calculated phi(n) = {phi}")

        # --- Step 3: Choose Public Key e ---
        print("\nChoose 'e' such that 1 < e < phi(n) and gcd(e, phi) = 1")
        
        # Show some valid suggestions for e
        suggestions = [k for k in range(3, min(100, phi), 2) if math.gcd(k, phi) == 1]
        print(f"Suggested e values: {suggestions[:10]}...")
        
        e = int(input("Enter Public Exponent e: "))

        if math.gcd(e, phi) != 1:
            print("Error: 'e' is not coprime with phi!")
            exit()

        # --- Step 4: Calculate Private Key d ---
        # Using Extended Euclidean Algorithm
        d = mod_inverse(e, phi)

        print(f"\n[+] Public Key (e, n): ({e}, {n})")
        print(f"[+] Private Key (d, n): ({d}, {n})")

        # --- Step 5: Encryption ---
        print("\n--- Encryption ---")
        msg = input("Enter message to encrypt: ")
        encrypted_data = encrypt(msg, (e, n))
        print(f"Ciphertext (Encrypted): {encrypted_data}")

        # --- Step 6: Decryption ---
        print("\n--- Decryption ---")
        decrypted_data = decrypt(encrypted_data, (d, n))
        print(f"Decrypted Message: {decrypted_data}")

    except ValueError as ve:
        print(ve)

import math

# ল্যাব শিটে বলা হয়েছে gcd(e, phi) = 1 হতে হবে। 
# তোমার রেফারেন্স কোডেও math.gcd ব্যবহার করা হয়েছে, যা এখানে কার্যকর।

def solve_lab_assignment():
    print("--- RSA Public Exponent Verifier ---")
    
    while True:
        try:
            # ইনপুট ফরম্যাট: p q n (p, q হলো প্রাইম এবং n হলো কতটি e চেক করতে হবে)
            line = input().split()
            if not line:
                continue
            
            p = int(line[0])
            q = int(line[1])
            n_candidates = int(line[2])

            # ইনপুট শেষ করার শর্ত: 0 0 0
            if p == 0 and q == 0 and n_candidates == 0:
                break

            # তোমার রেফারেন্স কোডের মতো phi গণনা
            phi = (p - 1) * (q - 1)

            # n সংখ্যক ক্যান্ডিডেট এক্সপোনেন্ট চেক করা
            for _ in range(n_candidates):
                try:
                    e = int(input())
                    
                    # ল্যাব শিটের শর্ত অনুযায়ী ভ্যালিডেশন:
                    # ১. 1 < e < phi(n)
                    # ২. gcd(e, phi(n)) == 1
                    if 1 < e < phi and math.gcd(e, phi) == 1:
                        print("YES")
                    else:
                        print("NO")
                except ValueError:
                    continue
            
            # টেস্ট কেস শেষে একটি খালি লাইন (ল্যাব শিট অনুযায়ী)
            print()

        except EOFError:
            break
        except Exception as e_msg:
            print(f"Error: {e_msg}")
            break

if __name__ == "__main__":
    solve_lab_assignment()

import math

def get_private_key(e, phi):
    # Calculate d (modular inverse of e mod phi)
    return pow(e, -1, phi)

def number_to_text(n):
    # Converts a number to text based on the 01=A, 27=Space rule
    s = str(n)
    if len(s) % 2 != 0: s = '0' + s # Pad with leading zero if needed
    
    text = ""
    for i in range(0, len(s), 2):
        val = int(s[i:i+2])
        if 1 <= val <= 26:
            text += chr(ord('A') + val - 1)
        elif val == 27:
            text += " "
    return text

def rsa_task():
    # Given Values
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q: "))
    e,n = map(int, input("Enter public key (e n): ").split(','))
    c_example = int(input("Enter the cipher: "))
    
    # i. Key Generation
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # ii. Private Key calculation
    d = get_private_key(e, phi)
    print(f"Public Key (PU): {{e={e}, n={n}}}")
    print(f"Private Key (PR): {{d={d}, n={n}}}")

    # iii. Decryption
    # formula: M = C^d mod n
    m_decrypted = pow(c_example, d, n)
    print(f"\nDecrypted Number: {m_decrypted}")
    print(f"Decrypted Text: {number_to_text(m_decrypted)}")

    # iv. Encryption of Initials (Example: Initial 'K' is 11)
    # formula: C = M^e mod n
   # Change this part in your code:
    initials_input = input("Enter the numeric value of your initials (e.g., 718 for GR): ")
    initial_val = int(initials_input) 

    # The code then calculates C = M^e mod n
    c_encrypted = pow(initial_val, e, n)
    print(f"\nEncrypted value (C): {c_encrypted}")

if __name__ == "__main__":
    rsa_task()
    
def mod(a, p):
    return (a % p + p) % p

# def mod_inverse(a, p):
#     a = mod(a, p)
#     for i in range(1, p):
#         if mod(a * i, p) == 1:
#             return i
#     return -1

def mod_inverse(a,p):
    a=mod(a,p)
    if a==0:
        return -1
    return pow(a,p-2,p)

class Point:
    def __init__(self, x=0, y=0, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __str__(self):
        if self.infinity:
            return "Infinity"
        return f"({self.x}, {self.y})"

def infinity_point():
    return Point(infinity=True)

def point_add(P, Q, a, p):
    if P.infinity:
        return Q
    if Q.infinity:
        return P

    # Point at infinity condition
    if P.x == Q.x and mod(P.y + Q.y, p) == 0:
        return infinity_point()

    # Point doubling (P + P)
    if P.x == Q.x and P.y == Q.y:
        num = mod(3 * P.x * P.x + a, p)
        den = mod_inverse(2 * P.y, p)
        if den == -1: return infinity_point()
        lam = mod(num * den, p)
    # Point addition (P + Q)
    else:
        num = mod(Q.y - P.y, p)
        den = mod_inverse(Q.x - P.x, p)
        if den == -1: return infinity_point()
        lam = mod(num * den, p)

    xr = mod(lam * lam - P.x - Q.x, p)
    yr = mod(lam * (P.x - xr) - P.y, p)
    return Point(xr, yr)

# def is_on_curve(P, a, b, p):
#     """Checks if a point P lies on the elliptic curve y^2 = x^3 + ax + b (mod p)"""
#     if P.infinity:
#         return True # Infinity point তাত্ত্বিকভাবে কার্ভের ওপর থাকে
    
#     # বামপক্ষ (LHS) = y^2 mod p
#     lhs = mod(P.y * P.y, p)
    
#     # ডানপক্ষ (RHS) = (x^3 + ax + b) mod p
#     rhs = mod(P.x**3 + a * P.x + b, p)
    
#     return lhs == rhs

def scalar_multiply(P, k, a, p):
    result = infinity_point()
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return result

def compute_order(G, a, p):
    """Calculates the order 'n' of a generator point G."""
    temp = G
    n = 1
    # Keep adding G to itself until it reaches the point at infinity
    while not temp.infinity:
        temp = point_add(temp, G, a, p)
        n += 1
    return n

def solve_ecdh(alpha, beta, p, a, G_point, sample_num):
    print(f"--- Sample {sample_num} Calculation ---")
    
    # Alline-এর পাবলিক কী গণনা
    Pa = scalar_multiply(G_point, alpha, a, p)
    print(f"Alline's Public Key (Pa): {alpha} * {G_point} = {Pa}")

    # Bose-এর পাবলিক কী গণনা
    Pb = scalar_multiply(G_point, beta, a, p)
    print(f"Bose's Public Key (Pb)  : {beta} * {G_point} = {Pb}")

    # শেয়ারড সিক্রেট কী (K) গণনা
    K_alline = scalar_multiply(Pb, alpha, a, p)
    K_bose = scalar_multiply(Pa, beta, a, p)

    print(f"Alline calculates K: {alpha} * {Pb} = {K_alline}")
    print(f"Bose calculates K  : {beta} * {Pa} = {K_bose}")
    
    if str(K_alline) == str(K_bose):
        print(f"Result: Verified! Shared Secret Key K = {K_alline}\n")
    else:
        print("Result: Failed! Keys do not match.\n")

# ================= Main Program =================
def main():
    # ==========================================
    # GIVEN PARAMETERS
    # ==========================================
    p = 17
    a = 1
    # b = 2 (Implicit, not needed for addition math)
    G = Point(9, 3)
    P_M = Point(13, 6)
    k = 10
    P_B = Point(10, 3)
    
    
    p1 = 751
    a1 = -1
    G1 = Point(0, 376)
    P_M1 = Point(443, 253)
    k1 = 111
    P_B1 = Point(318, 79)
    
    

    print(f"--- ECC Calculations for E_{p}({a}, 2) ---")

    # 1. Calculate G + P_M
    G_plus_PM = point_add(G, P_M, a, p)
    print("\n1. Calculating G + P_M:")
    print(f"   {G} + {P_M} = {G_plus_PM}")

    # 2. Calculate Ciphertext P_C = [kG, P_M + kP_B]
    print("\n2. Calculating Ciphertext P_C:")

    kG = scalar_multiply(G, k, a, p)
    print(f"   Part 1 (kG)   : {k} * {G} = {kG}")

    kP_B = scalar_multiply(P_B, k, a, p)
    print(f"   Step 2a (kP_B): {k} * {P_B} = {kP_B}")

    P_M_plus_kP_B = point_add(P_M, kP_B, a, p)
    print(f"   Part 2 (P_M + kP_B): {P_M} + {kP_B} = {P_M_plus_kP_B}")

    print(f"\nFINAL ANSWER:")
    print(f"   P_C = [{kG}, {P_M_plus_kP_B}]")
    
    print(f"--- ECC Calculations for E_{p1}({a1}, 188) ---")
    

    # print(f"\n--- Verifying P_M1 on Curve E_{p1}({a1}, {b1}) ---")
    # if is_on_curve(P_M1, a1, b1, p1):
    #     print(f"Result: SUCCESS! Point {P_M1} is on the curve.")
    # else:
    #     print(f"Result: FAILED! Point {P_M1} is NOT on the curve.")
    
    
    # 1. Calculate Order n
    print("\n1. Calculating Order n (This might take a moment...):")
    n = compute_order(G1, a1, p1)
    print(f"   Result: n = {n}")
    
    
    print("\n2. Calculating Ciphertext P_C:")

    kG1 = scalar_multiply(G1, k1, a1, p1)
    print(f"   Part 1 (kG1)   : {k1} * {G1} = {kG1}")

    kP_B1 = scalar_multiply(P_B1, k1, a1, p1)
    print(f"   Step 2a (kP_B1): {k1} * {P_B1} = {kP_B1}")

    P_M_plus_kP_B1 = point_add(P_M1, kP_B1, a1, p1)
    print(f"   Part 2 (P_M1 + kP_B1): {P_M1} + {kP_B1} = {P_M_plus_kP_B1}")

    print(f"\nFINAL ANSWER:")
    print(f"   P_C1 = [{kG1}, {P_M_plus_kP_B1}]")
    
    solve_ecdh(7, 5, p, a, G, 1)
    

if __name__ == "__main__":
    main()


def mod(a, p):
    return (a % p + p) % p

def mod_inverse(a, p):
    a = mod(a, p)
    for i in range(1, p):
        if mod(a * i, p) == 1:
            return i
    return -1

class Point:
    def __init__(self, x=0, y=0, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __str__(self):
        if self.infinity:
            return "Infinity"
        return f"({self.x},{self.y})"

def infinity_point():
    return Point(infinity=True)

def is_on_curve(P, a, b, p):
    if P.infinity:
        return True
    return mod(P.y * P.y, p) == mod(P.x * P.x * P.x + a * P.x + b, p)

def point_add(P, Q, a, p):
    if P.infinity:
        return Q
    if Q.infinity:
        return P

    if P.x == Q.x and mod(P.y + Q.y, p) == 0:
        return Point(infinity=True)

    if P.x == Q.x and P.y == Q.y:
        num = mod(3 * P.x * P.x + a, p)
        den = pow(2*P.y, p-2, p)
        lam = mod(num * den, p)
    else:
        num = mod(Q.y - P.y, p)
        den = mod_inverse(Q.x - P.x, p)
        lam = mod(num * den, p)

    xr = mod(lam * lam - P.x - Q.x, p)
    yr = mod(lam * (P.x - xr) - P.y, p)
    return Point(xr, yr)

def scalar_multiply(P, k, a, p):
    result = infinity_point()
    while k > 0:
        if k & 1:
            result = point_add(result, P, a, p)
        P = point_add(P, P, a, p)
        k >>= 1
    return result

def compute_order(G, a, p):
    temp = G
    n = 1
    while not temp.infinity:
        temp = point_add(temp, G, a, p)
        n += 1
    return n

def find_affine_points(a, b, p):
    points = []
    for x in range(p):
        rhs = mod(x**3 + a*x + b, p)
        for y in range(p):
            if mod(y*y, p) == rhs:
                points.append(Point(x, y))
    return points

def xor_encrypt_decrypt(msg, key):
    return ''.join(chr(ord(c) ^ (key % 256)) for c in msg)

# ================= Main Program =================
def main():
    a = int(input("Enter curve parameter a: "))
    b = int(input("Enter curve parameter b: "))
    p = int(input("Enter prime p: "))

    if mod(4*a*a*a + 27*b*b, p) == 0:
        print("Invalid curve!")
        return

    # Display all affine points
    points = find_affine_points(a, b, p)
    print("\nAffine points on curve:")
    for pt in points:
        print(pt, end=" ")
    print(f"\nTotal points: {len(points)}\n")

    # Generator input
    while True:
        gx = int(input("Enter Generator Gx: "))
        gy = int(input("Enter Generator Gy: "))
        G = Point(gx, gy)
        if is_on_curve(G, a, b, p):
            break
        print("Point is NOT on curve. Try again.")

    n = compute_order(G, a, p)
    print(f"Order of Generator (n) = {n}")

    # Private keys
    alpha = int(input(f"Enter Alice private key (1 <= alpha < {n}): "))
    beta = int(input(f"Enter Bob private key (1 <= beta < {n}): "))

    # Public keys
    PA = scalar_multiply(G, alpha, a, p)
    PB = scalar_multiply(G, beta, a, p)

    print(f"\nAlice Public Key: {PA}")
    print(f"Bob Public Key: {PB}")

    # Shared secret
    sharedA = scalar_multiply(PB, alpha, a, p)
    sharedB = scalar_multiply(PA, beta, a, p)

    print(f"\nShared Secret (Alice): {sharedA}")
    print(f"Shared Secret (Bob):   {sharedB}")

    if sharedA.x == sharedB.x and sharedA.y == sharedB.y:
        print("\nKey Exchange Successful!")
    else:
        print("\nKey Exchange Failed!")
        return

    symmetric_key = sharedA.x

    message = input("\nEnter Message: ")
    encrypted = xor_encrypt_decrypt(message, symmetric_key)
    print(f"Encrypted: {encrypted}")
    decrypted = xor_encrypt_decrypt(encrypted, symmetric_key)
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()
    
import datetime

def caesar_encrypt(plaintext, shift):
    """অক্ষরগুলোকে শিফট করে এনক্রিপ্ট করার ফাংশন"""
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # বড় হাতের না ছোট হাতের তা নির্ধারণ করা
            start = ord('A') if char.isupper() else ord('a')
            # বর্ণমালার ২৬ অক্ষরের মধ্যে শিফট করা
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += shifted_char
        else:
            # স্পেস, @, : বা অন্য চিহ্ন অপরিবর্তিত রাখা
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    """ডিক্রিপ্ট করার জন্য এনক্রিপশন ফাংশনকেই নেগেটিভ শিফটে কল করা"""
    return caesar_encrypt(ciphertext, -shift)

def solve_part_a():
    print("--- Task (a): Encrypting Name and Current Time ---")
    
    # ১. নাম ইনপুট
    first_name = input("Enter your first name: ")
    
    # ২. বর্তমান সময় নেওয়া (HH:MMam/pm ফরম্যাটে)
    current_time = datetime.datetime.now().strftime("%I:%M%p").lower()
    
    # ৩. মেসেজ তৈরি করা: first_name@current-time
    plaintext = f"{first_name}@{current_time}"
    print(f"Original Plaintext: {plaintext}")
    
    # ৪. কী হিসেবে অক্ষর ইনপুট নেওয়া (যেমন: T)
    key_char = input("Enter a key letter (A-Z): ").upper()
    shift = ord(key_char) - ord('A') # A=0, B=1, C=2...
    
    # ৫. এনক্রিপশন
    encrypted_msg = caesar_encrypt(plaintext, shift)
    print(f"Using Key {key_char} (Shift {shift}): {encrypted_msg}\n")

def solve_part_b():
    print("--- Task (b): Brute Force Attack ---")
    ciphertext = "VruykmlxvnbmrterTgtefmlTmxVkxtmboxBg Max Ftkdxm Whftbg"
    
    print(f"Target Ciphertext: '{ciphertext}'")
    print("Attempting every possible shift (1-25)...\n")
    
    # ১ থেকে ২৫ পর্যন্ত সব কী চেক করা
    for shift in range(1, 26):
        attempt = caesar_decrypt(ciphertext, shift)
        key_letter = chr(ord('A') + shift) # শিফট ভ্যালুকে অক্ষরে রূপান্তর
        
        # আউটপুট প্রিন্ট করা
        print(f"Key {key_letter} (Shift {shift:02}): {attempt}")
    
    print("\n[Analysis Complete] Check the list to find the readable sentence.")

if __name__ == "__main__":
    # পার্ট (a) রান করা
    solve_part_a()
    
    # পার্ট (b) রান করা
    input("Press Enter to start Brute Force Attack on Part (b)...")
    solve_part_b()

# ==========================================
# Standard Diffie-Hellman Key Exchange
# ==========================================

def main():
    print("--- Diffie-Hellman Key Exchange ---\n")
    
    # Step 1: Publicly agreed variables (Shared over the internet)
    # In a real-world scenario, P would be a 2048-bit or 4096-bit prime number.
    P = int(input("Enter a prime number (P): "))
    G = int(input("Enter a generator / primitive root (G): "))
    
    print(f"\n[Publicly Shared] Prime (P) = {P}, Generator (G) = {G}\n")

    # Step 2: Private Keys (Kept secret on their own devices)
    a = int(input("Enter Alice's private key (a): "))
    b = int(input("Enter Bob's private key (b): "))

    # Step 3: Generating Public Keys
    # In Python, pow(base, exp, mod) is highly optimized for cryptography.
    # It calculates (base^exp) % mod without memory overflow.
    x = pow(G, a, P)  # Alice's public key
    y = pow(G, b, P)  # Bob's public key
    
    print(f"\n[Sending over Network] Alice sends Public Key (x) = {x}")
    print(f"[Sending over Network] Bob sends Public Key (y) = {y}\n")

    # Step 4: Generating the Shared Secret
    # Alice uses Bob's public key (y) and her private key (a)
    ka = pow(y, a, P)
    
    # Bob uses Alice's public key (x) and his private key (b)
    kb = pow(x, b, P)

    print(f"Alice's calculated Shared Secret: {ka}")
    print(f"Bob's calculated Shared Secret:   {kb}\n")

    # Verification
    if ka == kb:
        print("✅ Key Exchange Successful! The shared secret matches.")
        print(f"   Symmetric Key to be used for AES encryption: {ka}")
    else:
        print("❌ Key Exchange Failed!")

if __name__ == "__main__":
    main()