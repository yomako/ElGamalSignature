from elgamal import *


private_key, public_key = generate_keys()
private_key.show()
print("p has {} digits".format(math.floor(math.log10(private_key.p))))
message1 = "It's me. Trust me."
signature = generate_signature(private_key=private_key, message=message1)
if verify_signature(public_key=public_key, message=message1, signature=signature):
    print('Signature is valid.')
else:
    print('Signature is not valid.')

message2 = "Top secret message."
encode_string(public_key=public_key, message=message2, filename='cryptogram.p')
decoded_message = decode_string(private_key=private_key, filename='cryptogram.p')
print('Decoded message:')
print(decoded_message)
