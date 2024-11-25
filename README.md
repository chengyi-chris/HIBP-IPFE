# [HIBP-IPFE](https://doi.org/10.1049/2024/5535196)

This is an official implementation of HIBP-IPFE proposed by our paper "[Privacy-enhanced Data Sharing Systems from Hierarchical ID-based Puncturable Functional Encryption with Inner Product Predicates](https://doi.org/10.1049/2024/5535196)". 

This project provides PoC implementations to evaluate the performance of the following schemes, which adopts the PBC library with Type-A pairing (160, 512) for 80-bit security.

- Our scheme: Hierarchical identity-based puncturable inner product functional encryption (HIBP-IPFE)
- SDH+21's work: [Hierarchical identity-based inner product functional encryption](https://doi.org/10.1016/j.ins.2021.05.062)


## Required libraries

- [GMP 5.x](http://gmplib.org/)
- [PBC](http://crypto.stanford.edu/pbc/news.html)
- [OPENSSL](http://www.openssl.org/)
- [Charm-crypto](https://jhuisi.github.io/charm/install_source.html)

## Run

1. SDH+21:

   ```
   python3 HIB-IPFE.py
   ```

2. Ours:

   ```
   python3 HIBP-IPFE.py
   ```

## Test

```
## Key generation algorithm
python3 ./Test performance/keygen.py

## Encryption algorithm
python3 ./Test performance/enc.py

## Decryption algorithm
python3  ./Test performance/dec.py

## Key delegation algorithm
python3  ./Test performance/keydel.py

## Key puncture algorithm
python3  ./Test performance/keypun.py
```

## Results


|   Key Generation  |   Encryption    |   Decryption   |
| ----------------- | --------------------- | ------------------- |
| ![keygen](./keygen.png) | ![enc](./enc.png) | ![dec](./dec.png) |

|   Key Delegation  |      Key Puncture     | 
| ----------------- | --------------------- |
| ![keydel](./keydel.png) | ![keypun](./keypun.png) |
