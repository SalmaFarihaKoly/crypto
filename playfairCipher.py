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
        +
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