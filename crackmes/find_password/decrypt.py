encrypted_message = b'\x39\x4a\x3c\x71\x3d\x5e\x27\x3a\x68\x2a\x23\x2a\x64\x3a\x23\x2b\x4a\x68\x2a\x39\x29\x23\x27\x2b\x23\x3e\x29\x27\x42\x73'

decrypted_message = b''

for byte in encrypted_message :
    decrypted_byte = byte + 10
    decrypted_message += bytes([decrypted_byte])

print(decrypted_message)