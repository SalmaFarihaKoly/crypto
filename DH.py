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