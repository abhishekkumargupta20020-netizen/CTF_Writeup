# UDP evidence challenge — 52-round transformation reversal

- **Period:** 31 October 2026
- **Category:** Reverse engineering / packet-derived evidence
- **Status:** Solved / verified
- **Challenge title:** Not preserved in the recovered conversation record
- **Recovered flag:** `SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}`
- **Acceptance evidence:** The reconstructed candidate passed the challenge verifier, which printed `Authenticated. EXIT: 0`.

## Evidence recovered from the session

The investigation involved four evidence files and a packet capture containing 290 UDP packets. The solution required recovering the data and reversing a 52-round transformation. The recorded analysis identified substitution and forward-chain stages, followed by a backward-mixing stage.

## Reversal approach

The preserved technical outline is:

1. Inspect and correlate the four evidence files with the 290 UDP packets; treat the packet stream as structured input to the reconstruction rather than as unrelated network noise.
2. Recover the encoded material and identify the 52-round transformation pipeline.
3. Reverse the substitution stage using the inverse mapping implied by the challenge logic.
4. Undo the forward-chain dependency in reverse order so that each recovered value is available before it is needed by the preceding step.
5. Reverse the backward-mixing stage. During this step, an off-by-one error in the reverse indexing was identified and corrected; this correction was necessary for the recovered data to authenticate.
6. Run the reconstructed candidate through the supplied verifier and confirm the explicit success response.

## Result

```text
SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}
```

Observed verification response:

```text
Authenticated. EXIT: 0
```

## Reproducibility and evidence limits

The recovered conversation record confirms the packet count (290), four evidence files, 52-round transformation, substitution and forward-chain stages, the corrected backward-mixing off-by-one, final flag, and verifier output. It does not preserve the official challenge title, original filenames, packet field layout, round constants, substitution table, exact commands, solver source, or full intermediate values. These are not reconstructed speculatively. The original four evidence files and packet capture were not available in the recovered file set for this archive update.

## Key lesson

When reversing chained multi-round transforms, invert operations in strict dependency order and verify index boundaries independently. A single off-by-one in the reverse mixing stage can produce plausible-looking but unauthenticated output.
