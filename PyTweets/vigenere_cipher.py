

def vigenere_cipher(string, keys):
    result = ""
    for i, c in enumerate(string):
        shift = keys[i % len(keys)]
        cipher_i = (ord(c) - 97 + shift) % 26
        result += (chr(cipher_i + 97))
    return result


print(vigenere_cipher("helloworld", [3, 4, 1]))
print(vigenere_cipher("kimosxrvmg", [-3, -4, -1]))
