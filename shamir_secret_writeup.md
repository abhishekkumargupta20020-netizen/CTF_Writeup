# Shamir Secret Sharing Writeup

## Challenge Summary

The server implements a Shamir secret sharing scheme over a prime field selected by the client.

For each query:

1. The client sends a prime `p` and a share count `n`.
2. The server creates a random polynomial of degree `n - 1` with the 256-bit secret as its constant term.
3. The server evaluates the polynomial at `x = 1, 2, ..., n`.
4. The server sends every share except the final one.

The secret is fixed for the lifetime of the connection. A 30-second alarm limits the total interaction time.

Goal: recover the 256-bit secret and submit it to receive the flag.

## Source Behavior

The relevant server logic is:

```python
class SecretSharing:
    def __init__(self, p, n, secret):
        self.p = p
        self.n = n
        self.poly = [secret] + [
            getRandomRange(0, self.p - 1) for _ in range(n - 1)
        ]

    def evaluate(self, x):
        return sum(
            self.poly[i] * pow(x, i, self.p)
            for i in range(len(self.poly))
        ) % self.p

    def get_shares(self):
        return [self.evaluate(i + 1) for i in range(self.n)]
```

After validating `p` and `n`, the server prints:

```python
shares = self.get_shares()[:-1]
```

Only `n - 1` shares are disclosed. The final evaluation is withheld.

An invalid `p` or `n` exits the query loop and asks for the secret.

## Vulnerability

A degree `n - 1` polynomial requires `n` points to interpolate uniquely. Since only `n - 1` shares are disclosed, one degree of freedom remains.

However, the unknown polynomial coefficients are constrained:

- Every nonconstant coefficient is chosen from `[0, p - 2]`.
- Therefore, no nonconstant coefficient may equal `p - 1 = -1 mod p`.

Choosing `n = p - 1` makes this one-degree-of-freedom structure especially simple and produces a small candidate set for the secret modulo `p`.

## Mathematics

### One Degree of Freedom

Let the disclosed points be:

```text
(1, y1), (2, y2), ..., (n - 1, y_{n - 1})
```

Define `R(x)` as the unique degree-at-most-`n-1` polynomial satisfying:

```text
R(i) = y_i    for i = 1, ..., n - 1
R(0) = 0
```

Then every polynomial that matches the disclosed shares can be written as:

```text
P(x) = R(x) + t * F(x)
```

where

```text
F(x) = product_{j=1}^{n-1} (x - j)
```

for a single unknown scalar `t mod p`.

Since `F(j) = 0` for every disclosed point, adding `t * F(x)` leaves all disclosed shares unchanged.

The secret is:

```text
P(0) = R(0) + t * F(0) = t * F(0)
```

### Choosing `n = p - 1`

Set:

```text
n = p - 1
```

Then:

```text
F(x) = product_{j=1}^{p-2} (x - j)
```

This polynomial has the simple form:

```text
F(x) = (x^(p - 1) - 1) / (x + 1)
     = x^(p - 2) - x^(p - 3) + ... - x + 1
     = sum_{i=0}^{p-2} (-1)^(i+1) * x^i
```

In particular:

```text
F(0) = -1
```

so the secret modulo `p` is:

```text
secret mod p = -t
```

### Eliminating Candidate Values of `t`

Let `R_i` be the coefficient of `x^i` in `R(x)`.

The coefficients of the unknown polynomial are:

```text
coeff_i(P) = R_i + t * F_i
```

For every nonconstant coefficient, the server requires:

```text
coeff_i(P) != -1 mod p
```

Therefore, for each `i = 1, ..., p - 2`:

```text
R_i + t * F_i != -1 mod p
```

Since `F_i` is either `1` or `-1`, each coefficient eliminates one candidate `t`:

```text
t != -(R_i + 1) * F_i^(-1) mod p
```

The true `t` is never eliminated because the server's polynomial satisfies all coefficient bounds.

Because each random coefficient constraint removes roughly one random `t` value, one query leaves approximately:

```text
p * (1 - 1/p)^(p - 2) approximately p / e
```

possible residues. Intersecting independent candidate sets reduces the expected size by a factor of about `e` per query.

### Combining Primes with CRT

Collect 40 primes from `17` through `199`:

```text
17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
157, 163, 167, 173, 179, 181, 191, 193, 197, 199
```

Their product is 258 bits, which is larger than `2^256`. Once the secret is uniquely determined modulo every prime, the Chinese Remainder Theorem gives a unique integer in the valid 256-bit secret range.

## Attack Procedure

1. Open one TCP connection and keep it open. The secret changes if the connection is recreated.
2. For each prime, query the server with `p = prime` and `n = p - 1`.
3. Parse the disclosed shares.
4. Interpolate `R(x)` including the point `(0, 0)`.
5. Build the candidate set of `t` values, then convert each to the corresponding secret residue `-t mod p`.
6. Intersect candidate sets for repeated queries on the same prime.
7. Start with 8 queries per prime. If a prime still has multiple candidates, issue adaptive extra batches.
8. Once every prime has a unique residue, apply CRT.
9. Submit the recovered secret.

The full attack completed in about 9.84 seconds, well inside the 30-second limit.

## Implementation Notes

The solver is in [`solve.py`](./solve.py).

Important implementation details:

- Consecutive interpolation points `0, 1, ..., p - 2` allow Newton forward differences with a binomial basis.
- `F(x)` is constructed directly from its alternating `1` and `-1` coefficients.
- Candidate elimination uses a `bytearray` mask indexed by `t`.
- Queries are pipelined in batches to avoid network round-trip overhead.
- All queries must use the same connection because the secret is generated once per server process.
- The server's `input("p = ")` prompt already contains the label, so the client must send raw values such as `17`, not `p = 17`.

The submission sequence is:

```text
0
0
<recovered secret>
```

The `0` values for `p` and `n` fail the server's validity check and break the query loop. The server then reads the secret and prints the flag if it matches.

## Result

```text
hitcon{even_off_by_one_is_leaky_in_SSS}
```

## Reproduction

From `E:\crypto`:

```powershell
python solve.py --selftest
python solve.py --simulate --k 8 --trials 2
python solve.py
```

Example successful output:

```text
pending [] 9.84s
n = secret = hitcon{even_off_by_one_is_leaky_in_SSS}
FLAG hitcon{even_off_by_one_is_leaky_in_SSS}
```

## Files

- `server_c03a6a86069546c05d3b4cb1fbe84805.py` - provided challenge server source.
- `solve.py` - local selftest, simulation, and remote exploit.
- `writeup.md` - this writeup.
