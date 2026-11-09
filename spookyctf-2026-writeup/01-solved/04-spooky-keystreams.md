# Spooky Keystreams — AES-CTR nonce reuse

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{cs351JKS}
```

## Challenge

`backup.py` encrypts messages with AES in CTR mode. The flag is one of the encrypted messages. Recover it without the key.

## Files

- `challenge-files/backup.py` — the encryption code and ciphertexts

## Vulnerability

`backup.py` uses AES-CTR with:

- a fixed nonce, `b"ghost123"`
- `initial_value=0`
- messages padded to 64 bytes with spaces

In CTR mode AES becomes a keystream. With the same key **and** the same nonce, every message is encrypted with the *exact same keystream*. That is the whole vulnerability: a known plaintext reveals the keystream, and the keystream decrypts everything else.

## Solution

1. Take a message whose plaintext is known and its ciphertext.
2. XOR them: `known_plaintext XOR ciphertext = keystream`.
3. XOR that keystream with the encrypted flag: `keystream XOR flag_ciphertext = flag`.

Because every message is padded to the same 64 bytes and uses the same nonce, the recovered keystream covers the full flag.

## Flag

```
spooky{cs351JKS}
```

Submitted on the platform and accepted.
