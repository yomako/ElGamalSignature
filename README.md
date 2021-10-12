# ElGamalSignature
Project for Cryptography and Data Security lecture. 
Contains set of functions to message encryption/decryption and generation/verification
digital signature using ElGamal algorithm.

##General info
ElGamal system is an asymmetric key encryption algorithm. 
Is based on multiplicative groups of integers modulo *p* and discrete logarithms problem.
The process of keys creation involves choosing large prime number *p* and random *k* integer from
range 1 < *k* < *p*, then finding the generator of cyclic group *g* and computing value 
*b=g<sup>k</sup> mod p*. Private key is a set of (*p*, *g*, *k*, *b*) values and public key is (*p*, *g*, *b*).
More informations you can find on [Wikipedia](https://en.wikipedia.org/wiki/ElGamal_encryption).
##Example
Simple example of project functionality is located in example.py file. 
You can run it by passing in console:
     `python example.py`.

##Technology
- Python 3.7
    - NumPy 1.21
