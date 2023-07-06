from __future__ import print_function
import bitcoin
import hashlib
import base58

# Address we are trying to target
target_address = b'1QLbz7JHiBTspS962RLKV8h1234'

# Get the last 'n' digits from the address based on the amount being transferred
n = 2
theoretic_max = 58**n
target_suffix = target_address[-n:]

# Create instances of hash functions
sha256 = hashlib.sha256()
ripemd160 = hashlib.new('ripemd160')

# Counter for the number of addresses generated
counter = 0

while True:
    counter += 1
    # Generate a random private key
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N

    # Multiply the EC generator point G with the private key to get a public key point
    public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)

    # Compress public key, adjust prefix depending on whether y is even or odd
    (public_key_x, public_key_y) = public_key
    compressed_prefix = '02' if (public_key_y % 2) == 0 else '03'
    hex_compressed_public_key = compressed_prefix + (bitcoin.encode(public_key_x, 16).zfill(64))

    # SHA-256 Hash of the Public key
    sha256_hash = sha256.copy()
    sha256_hash.update(bytearray.fromhex(hex_compressed_public_key))

    # RIPEMD-160 Hash of the SHA-256 Hash
    ripemd160_hash = ripemd160.copy()
    ripemd160_hash.update(sha256_hash.digest())

    # Adding network byte to RIPEMD-160 Hash
    network_byte = b'\00'
    network_bitcoin_public_key = network_byte + ripemd160_hash.digest()

    # Double SHA-256 Hash of the networked public key
    network_bitcoin_public_key_sha256 = sha256.copy()
    network_bitcoin_public_key_sha256.update(network_bitcoin_public_key)
    network_bitcoin_public_key_sha256_2 = sha256.copy()
    network_bitcoin_public_key_sha256_2.update(network_bitcoin_public_key_sha256.digest())

    # Adding first 4 bytes of the double SHA-256 as checksum
    checksum = network_bitcoin_public_key_sha256_2.digest()[:4]
    bitcoin_binary_address = network_bitcoin_public_key + checksum

    # Converting binary to base58 to get the Bitcoin address
    bitcoin_address = base58.b58encode(bitcoin_binary_address)

    # Print the generated address
    #   print(f'Generated Bitcoin Address ({counter}): {bitcoin_address}')

    # Check the last 'n' digits of the generated address with the target address
    if bitcoin_address[-n:] == target_suffix:
        print(f'Collision found after {counter} tries!')
        print(f'Generated Bitcoin Address: {bitcoin_address}')
        break

    # For the sake of the example, let's stop the loop after the theoretic maximum
    if counter >= theoretic_max:
        print(f'No collision found after {theoretic_max} tries.')
        break
