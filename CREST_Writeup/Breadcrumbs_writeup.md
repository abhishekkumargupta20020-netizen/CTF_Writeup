# CREST CTF Write-Up — Breadcrumbs2026Trail9X

## 1. Challenge Overview

**Category:** Digital Forensics / Linux Log Analysis  
**Objective:** Recover the authentic `CREST{...}` flag from system logs and recovery artifacts.  
**Flag:** `CREST{Breadcrumbs2026Trail9X}`

### Challenge premise

The investigation follows a sequence of privileged execution, account transitions, and application recovery activity. Multiple flag-shaped strings appear in routine logs and annotations, so identifying the correct flag requires correlating evidence across several artifacts rather than trusting the first matching string.

The key evidence comes from the audit log, authentication log, system log, worker state file, and recovery manifest.

## 2. Evidence Collection

The following artifacts establish the investigation trail:

| Artifact | Purpose |
|---|---|
| `var_log_audit_execve.log` | Records privileged command execution |
| `var_log_auth.log` | Records authentication and local session activity |
| `var_log_syslog.log` | Provides supporting system events |
| `var_tmp_stage_state.txt` | Contains worker recovery state |
| `var_lib_app_worker_recovery_manifest.conf` | Contains recovery metadata and an encoded token |

The analysis must consider these artifacts together because the recovery manifest's significance depends on its relationship to the earlier system events.

## 3. Step 1 — Identify the Privileged Execution

The audit log records the `deploy` account executing:

```bash
sudo /usr/local/bin/rotate-worker --recover
```

The command invokes the worker rotation utility with the `--recover` option under elevated privileges.

This is the first significant event in the chain. It establishes a privileged recovery operation that can be correlated with later worker activity.

**Finding:** The audit record identifies the recovery command and its privileged execution context.

## 4. Step 2 — Correlate the Account Transition

The authentication and system logs record a subsequent local `worker` session and a worker-context transition.

These events provide context for the recovery operation. Rather than treating the `deploy` and `worker` events as unrelated, the investigation uses their temporal and operational relationship to follow the recovery workflow.

Relevant artifacts:

- `var_log_auth.log`
- `var_log_syslog.log`

**Finding:** The logs document the transition from the privileged recovery invocation to subsequent worker-context activity.

The available summary supports the existence of these events, but exact timestamps and process identifiers should be included in a final evidence report only after checking the original log entries.

## 5. Step 3 — Correlate the Recovery State

The worker state file and recovery manifest share two identifiers:

| Field | Value |
|---|---|
| Checkpoint | `7f31c2a9` |
| Archive ID | `9c7d4e21` |
| Manifest source | `worker-history` |

The matching checkpoint and archive identifiers connect the worker state with the recovery manifest.

The `worker-history` source field provides additional context for the manifest's origin.

This correlation is important because it links the recovery artifact to the worker state involved in the earlier activity. The identifiers provide stronger evidence than the mere presence of a flag-shaped string.

**Finding:** The state file and manifest are associated through matching recovery identifiers.

## 6. Step 4 — Decode the Manifest's Base64 Fragment

The recovery manifest contains the following encoded value:

```text
Q1JFU1R7QnJlYWRjcnVtYnMyMDI2VHJhaWw5WH0=
```

Base64 is an encoding scheme that represents binary data using printable ASCII characters. Decode the value using the Linux command-line utility:

```bash
echo 'Q1JFU1R7QnJlYWRjcnVtYnMyMDI2VHJhaWw5WH0=' | base64 -d
```

Expected output:

```text
CREST{Breadcrumbs2026Trail9X}
```

Alternatively, use Python:

```python
import base64

encoded = "Q1JFU1R7QnJlYWRjcnVtYnMyMDI2VHJhaWw5WH0="
decoded = base64.b64decode(encoded, validate=True).decode("utf-8")

print(decoded)
```

Output:

```text
CREST{Breadcrumbs2026Trail9X}
```

The decoded string matches the required flag format.

## 7. Step 5 — Distinguish the Authentic Flag from Decoys

The challenge warns that routine logs and annotations contain other flag-shaped strings. Therefore, matching the `CREST{...}` syntax is not sufficient to establish authenticity.

The selected token is supported by the following evidence chain:

1. The audit log records the privileged recovery invocation.
2. Authentication and system logs document subsequent worker-context activity.
3. The worker state and recovery manifest share checkpoint `7f31c2a9` and archive ID `9c7d4e21`.
4. The manifest identifies its source as `worker-history`.
5. The manifest contains the Base64 fragment that decodes to `CREST{Breadcrumbs2026Trail9X}`.

This combination of provenance, identifier correlation, and decoding supports selecting the manifest's token over unrelated flag-shaped strings.

**Evidence limitation:** The decoded value and identifier matches are confirmed by the supplied findings. A claim that the manifest is cryptographically authenticated, or that every decoy has been exhaustively ruled out, would require additional evidence not provided in the summary.

## 8. Final Flag

```text
CREST{Breadcrumbs2026Trail9X}
```

## 9. Conclusion

The challenge was solved by correlating Linux audit and authentication events with application recovery artifacts, then decoding the Base64 token found in the recovery manifest.

The essential technique was **cross-artifact evidence correlation**: the privileged execution established the initiating event, the account-transition logs provided operational context, and the matching checkpoint and archive identifiers linked the worker state to the manifest containing the recovered token.

The final flag is:

**`CREST{Breadcrumbs2026Trail9X}`**
