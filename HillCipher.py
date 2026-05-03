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