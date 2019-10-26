def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    step = 0
    for s in plaintext:
        if ('A' <= s <= 'Z') or ('a' <= s <= 'z'):
            if 'A' <= s <= 'Z':
                ss = ord(s) + ord(keyword[step % len(keyword)]) - ord('A')
                if chr(ss) > 'Z':
                    ss -= 26
            else:
                ss = ord(s) + ord(keyword[step % len(keyword)]) - ord('a')
                if chr(ss) > 'z':
                    ss -= 26
            ciphertext += chr(ss)
        else:
            ciphertext += s
        step += 1
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    step = 0
    for s in ciphertext:
        if ('A' <= s <= 'Z') or ('a' <= s <= 'z'):
            if 'A' <= s <= 'Z':
                ss = ord(s) - ord(keyword[step % len(keyword)]) + ord('A')
                if chr(ss) < 'A':
                    ss += 26
            else:
                ss = ord(s) - ord(keyword[step % len(keyword)]) + ord('a')
                if chr(ss) < 'a':
                    ss += 26
            plaintext += chr(ss)
        else:
            plaintext += s
        step += 1
    return plaintext
