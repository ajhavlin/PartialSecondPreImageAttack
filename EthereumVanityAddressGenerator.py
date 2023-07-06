import os
import binascii
from ethereum import utils

# Address we are trying to target
target_address = b'0x7E5F4552091A69125d5DfCb7b8C265902Bdf1234'

# Get the last 'n' digits from the address based on the amount being transferred
n = 2
theoretic_max = 16**n
target_suffix = target_address[-n:]

# Counter for the number of addresses generated
counter = 0

while True:
    counter += 1

    # Generate a random private key
    private_key = binascii.hexlify(os.urandom(32))

    # Generate public key
    public_key = utils.privtoaddr(private_key)

    # Format Ethereum address
    ethereum_address = '0x' + utils.checksum_encode(public_key)

    # Check the last 'n' digits of the generated address with the target address
    if ethereum_address[-n:].encode() == target_suffix:
        print(f'Collision found after {counter} tries!')
        print(f'Generated Ethereum Address: {ethereum_address}')
        break

    # For the sake of the example, let's stop the loop after the theoretic maximum
    if counter >= theoretic_max:
        print(f'No collision found after {theoretic_max} tries.')
        break
