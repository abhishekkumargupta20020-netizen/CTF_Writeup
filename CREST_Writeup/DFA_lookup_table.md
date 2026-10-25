# CREST CTF Writeup: DFA Lookup Tables Aren't Really Secret

## Flag

```text
CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}
```

## Challenge Overview

The flag suggests a challenge involving a deterministic finite automaton (DFA) and lookup tables. The central idea is that lookup tables used by a program are not necessarily secret merely because they are difficult to interpret or are embedded in the implementation.

## Approach

### 1. Identify the lookup-table implementation

Start by inspecting the provided source code, executable, or challenge files. Search for:

- Large constant arrays or lookup tables.
- State-transition logic.
- Input-processing loops.
- Encoded or transformed constants.
- References to table entries that affect the program's output.

The objective is to understand how the program processes input and how the tables contribute to that process.

### 2. Reconstruct the DFA

A deterministic finite automaton consists of a set of states, an input alphabet, a transition function, and accepting states.

Represent the relevant logic as:

\[
\delta(q, x) = q'
\]

where \(q\) is the current state, \(x\) is the input symbol, and \(q'\) is the next state.

If the transition function is represented by a lookup table, inspect how the program indexes that table and how it updates its state.

### 3. Analyze the acceptance condition

Determine which state or output condition causes the program to accept an input. Trace the transition logic to identify the required input sequence or any transformation that must be reversed.

If the table is recoverable from the binary or source code, it should be treated as observable implementation data rather than an independent secret.

### 4. Recover the flag

Use the reconstructed transition logic to determine the input accepted by the challenge, or to recover the flag if it is directly encoded in the implementation.

**Note:** The exact recovery method depends on the challenge binary or source code. The specific table structure and acceptance condition have not been provided here.

## Key Takeaway

Lookup tables can obscure program behavior, but obscurity is not equivalent to secrecy. If an attacker can inspect the implementation, the table and its transition logic may be recoverable.

## Flag

`CREST{dfa_l00kup_t4bl3s_ar3n7_r34lly_s3cr3t}`
