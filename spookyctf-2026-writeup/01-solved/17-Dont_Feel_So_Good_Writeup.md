# I D0n't Feel S0 G00d — SpookyCTF 2026

- **Category:** Crypto / Classical cryptography
- **Challenge files:** `chemicals.txt`, `antidotes.txt`
- **Flag format:** `spooky{...}`
- **Flag candidate:** `spooky{poison_is_bad_for_you}`
- **Verification status:** Derived from the supplied files; platform acceptance has not been independently confirmed.

## 1. Challenge clues

The challenge provides the number sequence:

```text
84 53 16 8 28 16 11 6 7
```

It also provides two text files and the note:

> Don't forget to move the neon!

The additional hint confirms that `antidotes.txt` uses a Caesar cipher.

## 2. Identify the poison from the periodic table

Interpret each number as an atomic number:

| Atomic number | Element symbol |
|---:|:---|
| 84 | Po |
| 53 | I |
| 16 | S |
| 8 | O |
| 28 | Ni |
| 16 | S |
| 11 | Na |
| 6 | C |
| 7 | N |

This spells:

```text
POISON IS NaCN
```

`NaCN` is sodium cyanide. In `chemicals.txt`, **Sodium Cyanide is entry 52** when counted from 1.

The sequence ends in nitrogen (`N`), whose atomic number is **7**. Applying that final 7 as the list offset gives:

```text
52 + 7 = 59
```

Therefore, inspect **line 59** of `antidotes.txt`.

## 3. Decode the selected antidote entry

Neon (`Ne`) has atomic number **10**. This supplies the Caesar shift: decrypt the letters by shifting them **10 positions backwards** (ROT-10).

Line 59 of `antidotes.txt` is:

```text
z01c0x_15_l4n_p0b_i0e
```

After Caesar ROT-10 and then leetspeak substitution (`0 → o`, `1 → i`, `4 → a`, `5 → s`), it becomes:

```text
poison_is_bad_for_you
```

The resulting flag candidate is:

```text
spooky{poison_is_bad_for_you}
```

## 4. Reproducible Python solver

Save this as `solve.py` in the same directory as `chemicals.txt` and `antidotes.txt`:

```python
from pathlib import Path
import re

CHEMICALS_FILE = Path("chemicals.txt")
ANTIDOTES_FILE = Path("antidotes.txt")
CAESAR_SHIFT = 10  # Neon has atomic number 10

# Digits used as letters in the decoded text.
LEET = {
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "6": "g",
    "7": "t",
}


def caesar_decode(text: str, shift: int) -> str:
    """Decode lowercase Caesar text by shifting letters backwards."""
    result = []
    for char in text:
        if "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
        else:
            result.append(char)
    return "".join(result)


def decode_antidote_line(ciphertext: str) -> str:
    """Apply ROT-10, then convert the digit-based leetspeak."""
    shifted = caesar_decode(ciphertext, CAESAR_SHIFT)
    return "".join(LEET.get(char, char) for char in shifted)


def main() -> None:
    if not CHEMICALS_FILE.is_file() or not ANTIDOTES_FILE.is_file():
        raise SystemExit("Place chemicals.txt and antidotes.txt beside solve.py")

    chemicals = [line.strip() for line in CHEMICALS_FILE.read_text().splitlines() if line.strip()]
    antidotes = [line.strip() for line in ANTIDOTES_FILE.read_text().splitlines() if line.strip()]

    poison = "Sodium Cyanide"
    try:
        poison_position = next(
            index for index, name in enumerate(chemicals, start=1)
            if name.casefold() == poison.casefold()
        )
    except StopIteration:
        raise SystemExit(f"{poison!r} was not found in chemicals.txt")

    nitrogen_atomic_number = 7
    target_position = poison_position + nitrogen_atomic_number

    if not 1 <= target_position <= len(antidotes):
        raise SystemExit(f"Calculated line {target_position} is outside antidotes.txt")

    ciphertext = antidotes[target_position - 1]
    plaintext = decode_antidote_line(ciphertext)
    flag = f"spooky{{{plaintext}}}"

    print(f"Poison: {poison}")
    print(f"Chemical-list position (1-based): {poison_position}")
    print(f"Nitrogen offset: +{nitrogen_atomic_number}")
    print(f"Selected antidotes.txt line: {target_position}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decoded text: {plaintext}")
    print(f"Flag candidate: {flag}")

    if not re.fullmatch(r"spooky\{[a-z0-9_]+\}", flag):
        raise SystemExit("Decoded result does not match the expected flag syntax")


if __name__ == "__main__":
    main()
```

Run it with:

```bash
python3 solve.py
```

Expected key output:

```text
Chemical-list position (1-based): 52
Nitrogen offset: +7
Selected antidotes.txt line: 59
Ciphertext: z01c0x_15_l4n_p0b_i0e
Decoded text: poison_is_bad_for_you
Flag candidate: spooky{poison_is_bad_for_you}
```

## 5. Notes and verification

- The Caesar step is **ROT-10 backwards**, because Neon has atomic number 10.
- The line selection uses the sodium-cyanide position (52) plus the final nitrogen atomic number (7), selecting line 59.
- The leetspeak conversion is applied **after** Caesar decoding; applying digit substitutions first produces incorrect text.
- The files contain several decoy lines with similar wording. In particular, line 52 decodes to `poison_is_bag_for_you`, while line 59 decodes to `poison_is_bad_for_you`.
- The flag above is the result of the documented decoding path. It should be labelled **unverified** until the CTF submission checker accepts it.
