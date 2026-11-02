# null_choir — custom 64-bit state-machine reversal

- **Period:** 31 October 2026
- **Category:** Reverse engineering
- **Status:** Solved / verified
- **Recovered flag:** `SecLeaf{th3_ch01r_s1ng5_1n_5h4d0w_m4ch1n35!!!!!}`
- **Acceptance evidence:** Running the recovered candidate against the challenge program produced `Harmony.`

## Challenge model recovered from the session

The challenge used a custom 64-bit state machine. The available trace, `echoes.trace`, exposed an interpreter with a 4,096-step instruction sequence and a 32-entry authenticated instruction table. The accepted input was not recovered by treating the trace as ordinary printable text; the solution required reversing the state transitions.

## Reversal approach

The recorded solution process was:

1. Treat the trace as an execution description for a 64-bit state machine rather than as a direct flag dump.
2. Reconstruct the 4,096 interpreter steps and the authenticated instruction-table semantics.
3. Reverse the transformations applied to the six-word state. Work backward through the state updates, respecting the width and ordering of each word.
4. Recover the final byte sequence by undoing the byte-wise comparison mask.
5. Validate the resulting candidate with the challenge executable. The program's `Harmony.` response is the preserved success signal.

## Result

```text
SecLeaf{th3_ch01r_s1ng5_1n_5h4d0w_m4ch1n35!!!!!}
```

Observed verification response:

```text
Harmony.
```

## Reproducibility and evidence limits

The prior session summary preserves the challenge name, `echoes.trace`, the 4,096-step interpreter, 32-entry authenticated instruction table, six-word state reversal, byte-wise comparison mask, final flag, and success output. It does **not** preserve the exact executable filename, full trace contents, constants, instruction-by-instruction dump, terminal commands, or original solver source. Those details are intentionally not invented here. The original executable and trace are not included in this archive because they were not available in the recovered file set at archive-update time.

## Key lesson

For custom VM/state-machine crackmes, identify the execution model first. A long trace can encode a deterministic program; reversing the state transitions and comparison layer is more reliable than searching the artifact for a flag-shaped string.
