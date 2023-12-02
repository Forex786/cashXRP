from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

"""
In symmetric key encryption schemes like AES, both the key and the initialization vector (IV) 
are required for decryption. The key is used to perform the actual encryption and decryption operations, 
while the IV is used to add an extra layer of randomness to each encryption, making it more secure.

When you encrypt a message, the IV is often generated randomly for each encryption operation, and it needs 
to be kept along with the ciphertext for later decryption. If you lose the IV or use the wrong IV during 
decryption, the decryption process will likely produce incorrect results.

So, when you decrypt a message, you need both the key and the corresponding IV to successfully recover 
the original plaintext. Ensure that you securely store and manage both the key and the IV to maintain the 
confidentiality and integrity of your encrypted data.

"""

# Function to generate a random key ( use this if you are not providing a user password )
def generate_key():
    return get_random_bytes(16)  # 16 bytes for AES-128, 24 bytes for AES-192, 32 bytes for AES-256

# Function to encrypt a message
def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext, cipher.iv

# Function to decrypt a ciphertext
def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()


# Function to convert IV to hex and back
def iv_to_hex(iv):
    return iv.hex()

def hex_to_iv(hex_iv):
    return bytes.fromhex(hex_iv)


# Example usage
# key =  b'hello my this is my key!' # generate_key() #
# print("key: ",key)

# message = "sEdVsHGvgKtVGX3ntj2CggKg44HewEM"
# print(f"Original message: {message}")
# # Encryption
# ciphertext, iv = encrypt(message, key)
# print("iv(hex): ",iv.hex())
# print(f"Ciphertext(hex): {ciphertext.hex()}")


# Decryption
# decrypted_message = decrypt(ciphertext, key, iv)
# print(f"Decrypted message: {decrypted_message}")




""" multi line comments start/end

key = input("Enter new AES password (max 32 chars): ")

# NB: key MUST be 24 characters long, so add extra digits if required.
key = key + "12345678901234567890123456789012"
key = key[0:32]

# commnet out for a new p/w key
key = "cashXRP1234567890123456789012345"

key = key.encode('utf-8')
print ("key encoded : ",key)

# provides XRPL SEEDS to encrypt for saving to dB.
# while True:

#     seed = input("\nEnter XRPL SEED (type 'n' to exit): ")

#     if seed.lower() == 'n':
#         print("Exiting the loop.")
#         break

#     pKey = input("Enter XRPL public key : ")
    
#     type = input("PreFund / PTS (f=PreFund) : ")

#     if type.lower() == 'f':
#         type = "PreFund"qweryu
#     else:
#         type = "PTS"

#     message = seed
#     # Encryption
#     ciphertext, iv = encrypt(message, key)
#     # print("SEED: ", message)
#     # print("AES p/w: ",key)
#     # print("iv(hex): ",iv.hex())
#     # print(f"Ciphertext(hex): {ciphertext.hex()}")

#     print(f"\nDELETE FROM PTS_wallets WHERE XRPL_address='{pKey}';")
#     print(f"INSERT INTO `cashXRP`.`PTS_wallets` (`XRPL_address`, `XRPL_SEED_hash`, `AES_IV`, `actual_balance`, `net_balance`, `wallet_type`, `allocation_status`, `allocated_to_process_ID`)" 
#           f"VALUES ('{pKey}','{ciphertext.hex()}','{iv.hex()}', '0', '0', '{type}', '0', '0');\n")
    


three_strings_list = [
    ["sEdVsHGvgKtVGX3ntj2CggKg44HewEM", "rUxi1XtG7521a8eHH6gzcaMXBE6bCAzjqm", "PreFund"],
    ["sEdTezUkhfzBo21GVFxFhVGokTR5shy", "rLgWybVe8hgY6yNAXCmyxJiobX4b11e6hC", "PTS"],
    ["sEdTDUu8LGkwfGefWk9ipdx8RPjtk51", "rUBfUoui7NM9DzVy1a3MeLAAG8s7H2Thch", "PTS"],
    ["sEd7F2YeTEWGkS5EH4cEPpbYEZrRUUM", "rNQYFraewsTkwGfqgMrge8BKfuPQSTpkRQ", "PTS"]
                    ]

# Accessing elements of the list
for wallet in three_strings_list:
    seed = wallet[0]
    pKey = wallet[1]
    type = wallet[2]

    # Encryption
    ciphertext, iv = encrypt(wallet[0], key)
    # print("SEED: ", message)
    # print("AES p/w: ",key)
    # print("iv(hex): ",iv.hex())
    # print(f"Ciphertext(hex): {ciphertext.hex()}")

    print(f"\nDELETE FROM PTS_wallets WHERE XRPL_address='{pKey}';")
    print(f"INSERT INTO `cashXRP`.`PTS_wallets` (`XRPL_address`, `XRPL_SEED_hash`, `AES_IV`, `actual_balance`, `net_balance`, `wallet_type`, `allocation_status`, `allocated_to_process_ID`)" 
          f"VALUES ('{pKey}','{ciphertext.hex()}','{iv.hex()}', '0', '0', '{type}', '0', '0');\n")
   
# Decryption with p/w = cashXRP1234567890123456789012345
ciphertext="fc60dfb27f92b7f5f3240252375ad7b0907bb4db38d6dcb0cb489d2fa2a56ebd"	
iv = "193575b9d4bec5ea802e5910ec90e050"

 # PTS wallet seed:  078611350b0039cd9cc7e22a45f4b052d250c677b48def243e7a72fd0600c527  
 # iv:  eb958132b5c8d9719abefdf48a17e4a5

ciphertext="078611350b0039cd9cc7e22a45f4b052d250c677b48def243e7a72fd0600c527"	
iv = "eb958132b5c8d9719abefdf48a17e4a5"

decrypted_message = decrypt(hex_to_iv(ciphertext), key, hex_to_iv(iv))
print(f"Decrypted message: {decrypted_message}")

# """