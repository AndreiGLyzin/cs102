def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    step = 3
    for s in plaintext:
        if ('A' <= s <= 'Z') or ('a' <= s <= 'z'):
            ss = ord(s) + step
            if (chr(ss) > 'Z') and (chr(ss) < 'a'):
                ss -= 26
            elif chr(ss) > 'z':
                ss -= 26
            ciphertext += chr(ss)
        else:
            ciphertext += s
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    step = 3
    for s in ciphertext:
        if ('A' <= s <= 'Z') or ('a' <= s <= 'z'):
            ss = ord(s) - step
            if (chr(ss) > 'Z') and (chr(ss) < 'a'):
                ss += 26
            elif chr(ss) < 'A':
                ss += 26
            plaintext += chr(ss)
        else:
            plaintext += s
    return plaintext
