
#include <iostream>
#include <vector>
using namespace std;

// 🔐 Toy block cipher (XOR-based)
int encrypt_block(int data, int key) {
    return data ^ key;
}

int decrypt_block(int data, int key) {
    return data ^ key;
}

// 1️⃣ ECB
vector<int> ECB_encrypt(vector<int> plaintext, int key) {
    vector<int> ciphertext;
    for (int p : plaintext)
        ciphertext.push_back(encrypt_block(p, key));
    return ciphertext;
}

vector<int> ECB_decrypt(vector<int> ciphertext, int key) {
    vector<int> plaintext;
    for (int c : ciphertext)
        plaintext.push_back(decrypt_block(c, key));
    return plaintext;
}

// 2️⃣ CBC
vector<int> CBC_encrypt(vector<int> plaintext, int key, int IV) {
    vector<int> ciphertext;
    int prev = IV;

    for (int p : plaintext) {
        int c = encrypt_block(p ^ prev, key);
        ciphertext.push_back(c);
        prev = c;
    }
    return ciphertext;
}

vector<int> CBC_decrypt(vector<int> ciphertext, int key, int IV) {
    vector<int> plaintext;
    int prev = IV;

    for (int c : ciphertext) {
        int p = decrypt_block(c, key) ^ prev;
        plaintext.push_back(p);
        prev = c;
    }
    return plaintext;
}

// 3️⃣ CFB
vector<int> CFB_encrypt(vector<int> plaintext, int key, int IV) {
    vector<int> ciphertext;
    int prev = IV;

    for (int p : plaintext) {
        int c = p ^ encrypt_block(prev, key);
        ciphertext.push_back(c);
        prev = c;
    }
    return ciphertext;
}

vector<int> CFB_decrypt(vector<int> ciphertext, int key, int IV) {
    vector<int> plaintext;
    int prev = IV;

    for (int c : ciphertext) {
        int p = c ^ encrypt_block(prev, key);
        plaintext.push_back(p);
        prev = c;
    }
    return plaintext;
}

// 4️⃣ OFB
vector<int> OFB_encrypt(vector<int> plaintext, int key, int IV) {
    vector<int> ciphertext;
    int prev = IV;

    for (int p : plaintext) {
        prev = encrypt_block(prev, key);
        ciphertext.push_back(p ^ prev);
    }
    return ciphertext;
}

vector<int> OFB_decrypt(vector<int> ciphertext, int key, int IV) {
    return OFB_encrypt(ciphertext, key, IV);
}

// 5️⃣ CTR
vector<int> CTR_encrypt(vector<int> plaintext, int key, int nonce) {
    vector<int> ciphertext;

    for (int i = 0; i < plaintext.size(); i++) {
        int keystream = encrypt_block(nonce + i, key);
        ciphertext.push_back(plaintext[i] ^ keystream);
    }
    return ciphertext;
}

vector<int> CTR_decrypt(vector<int> ciphertext, int key, int nonce) {
    return CTR_encrypt(ciphertext, key, nonce);
}

// 🔍 Print function
void print(vector<int> data) {
    for (int x : data) cout << x << " ";
    cout << endl;
}

// 🚀 MAIN
int main() {
    int n, key, IV, nonce;

    cout << "Enter number of blocks: ";
    cin >> n;

    vector<int> plaintext(n);
    cout << "Enter plaintext blocks: ";
    for (int i = 0; i < n; i++) cin >> plaintext[i];

    cout << "Enter key: ";
    cin >> key;

    cout << "Enter IV (for CBC/CFB/OFB): ";
    cin >> IV;

    cout << "Enter nonce (for CTR): ";
    cin >> nonce;

    cout << "\n===== Encryption Results =====\n";

    auto ecb = ECB_encrypt(plaintext, key);
    cout << "ECB: "; print(ecb);

    auto cbc = CBC_encrypt(plaintext, key, IV);
    cout << "CBC: "; print(cbc);

    auto cfb = CFB_encrypt(plaintext, key, IV);
    cout << "CFB: "; print(cfb);

    auto ofb = OFB_encrypt(plaintext, key, IV);
    cout << "OFB: "; print(ofb);

    auto ctr = CTR_encrypt(plaintext, key, nonce);
    cout << "CTR: "; print(ctr);

    cout << "\n===== Decryption Results =====\n";

    cout << "ECB: "; print(ECB_decrypt(ecb, key));
    cout << "CBC: "; print(CBC_decrypt(cbc, key, IV));
    cout << "CFB: "; print(CFB_decrypt(cfb, key, IV));
    cout << "OFB: "; print(OFB_decrypt(ofb, key, IV));
    cout << "CTR: "; print(CTR_decrypt(ctr, key, nonce));

    return 0;
}