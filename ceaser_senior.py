def caesar_cipher(text, shift, mode):
    """
    এনক্রিপশন এবং ডিক্রিপশন উভয়ই এই একটি ফাংশন দিয়ে করা সম্ভব।
    ডিক্রিপশন হলে শিফট ভ্যালু নেগেটিভ করে দেওয়া হয়।
    """
    if mode.upper() == 'D':
        shift = -shift
        
    result = ""
    for char in text:
        if char.isalpha():
            # Uppercase/Lowercase হ্যান্ডেল করা
            start = ord('A') if char.isupper() else ord('a')
            # Wrapping এবং Negative shift হ্যান্ডেল করা
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result += shifted_char
        else:
            # সংখ্যা, স্পেস এবং চিহ্ন অপরিবর্তিত রাখা
            result += char
    return result

def main():
    print("--- Caesar Cipher Program ---")
    
    # ইনপুট সেকশন (ছবির রিকোয়ারমেন্ট অনুযায়ী)
    mode = input("User choice: 'E' for Encrypt, 'D' for Decrypt: ").upper()
    text = input("Text: ")
    try:
        shift = int(input("Shift: "))
    except ValueError:
        print("Error: Shift must be an integer.")
        return

    # প্রসেসিং
    output = caesar_cipher(text, shift, mode)
    
    # আউটপুট প্রিন্ট
    print(f"Output: \"{output}\"")

if __name__ == "__main__":
    main()