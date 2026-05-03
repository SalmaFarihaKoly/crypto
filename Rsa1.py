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