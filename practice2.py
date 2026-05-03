import datetime

def ceaser_encrypt(plaintext,shift):
    encrypted_text=""
    for char in plaintext:
        if char.isalpha():
            start=ord('A') if char.isupper() else ord('a')
            shifted_ord=chr((ord(char)-start+shift)%26+start)
            encrypted_text+=char
    return encrypted_text
    
    
def ceaser_decrypt(ciphertext,shift):
    return ceaser_encrypt(ciphertext,-shift)

def solve_part_a():
    first_name=input("Enter your first name:")
    currentime=datetime.datetime.now().strftime("%I:%M:%S").lower()
    plaintext=f"{first_name}@{currentime}"
    print(f"Plaintext={plaintext}")
    key_char=input("Enter a key in character:").upper()
    shift=ord(key_char)-ord('A')
    encrypted_msg=ceaser_encrypt(plaintext,shift)
     shift=ord(key_char)-ord('A')
    
def solve_part_b():
    print("Task b")
    ciphertext="VruykmlxvnbmrterTgtefmlTmxVkxtmboxBg Max Ftkdxm Whftbg"
    print(f"Target ciphertext:{ciphertext}")
    print("Attempting every possible shift from (1 to 25)\n")
    for shift in range(1,26):
        attempt=ceaser_decrypt(ciphertext,shift)
        key_letter=chr(ord('A')+shift)
        print(f"Key{key_letter}(Shift:{shift:02}):{attempt}")
    print("Analysis completed........")

if __name__=="__main__":
    solve_part_a()
    input("Press enter to continue part (b)")
    solve_part_b()