# HIBP-IPFE
This project provides PoC implementations to evaluate the performance of the following schemes:

1. SDH+21 - Information Science - [Hierarchical identity-based inner product functional encryption](https://doi.org/10.1016/j.ins.2021.05.062) 


The code implemention of Hierarchical identity-based puncturable inner product functional encryption

For the bilinear-pairing scheme (SDH+21 and ours), we implement them by using PBC library with Type-A pairing (160, 512) for 80-bit security.

## Required library

- [GMP 5.x](http://gmplib.org/)
- [PBC](http://crypto.stanford.edu/pbc/news.html)
- [OPENSSL](http://www.openssl.org/)
- [Charm-crypto](https://jhuisi.github.io/charm/install_source.html)

## Perform code

1. For bilinear-pairing scheme (SDH+21):

   ```
   python3 HIB-IPFE.py
   ```

2. For our HIBP-IPFE scheme:

   ```
   python3 HIBP-IPFE.py
   ```

To execute the time cost of scheme for 500 times: we add `cal_time() ` in each algorithm, you can perform which operations or algorithm for simple test.

## Test performance

To generate the performance for each algorithm, we provide the result code in the below folder.

```
## For key generation algorithm
python3 ./Test performance/keygen.py

## For encryption algorithm
python3 ./Test performance/enc.py

## For decryption algorithm
python3  ./Test performance/dec.py

## For key delegation algorithm
python3  ./Test performance/keydel.py

## For key puncture algorithm
python3  ./Test performance/keypun.py
```

## Results


|   Key Generation  |   Encryption    |   Decryption   |
| ----------------- | --------------------- | ------------------- |
| ![keygen](./keygen.png) | ![enc](./enc.png) | ![dec](./dec.png) |

|   Key Delegation  |      Key Puncture     | 
| ----------------- | --------------------- |
| ![keydel](./keydel.png) | ![keypun](./keypun.png) |