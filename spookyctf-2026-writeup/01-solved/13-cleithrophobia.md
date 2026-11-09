# Cleithrophobia — Star Trek pcap

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
Spooky{Be0m_Me_Up_Sc0tty_2266}
```

Note the capital `S` in `Spooky{...}` — this challenge uses a capital-S wrapper, unlike the usual lowercase `spooky{...}`.

## Challenge

A packet capture, `Cleithrophobia.pcap` (2,000 packets), themed around the Starship Enterprise. Find the flag.

## Files

- `challenge-files/Cleithrophobia.pcap` — the capture

## Solution

**1. Cut through the noise.**
Most of the capture is decoys: TLS traffic, repeated FTP logins for scotty, sulu, spock, mccoy and the rest, and random `warp_core_telemetry` / `deflector` values.

**2. Find the ignition attempts.**
There are 20 `POST /bridge/ignition` attempts. 19 of them return 401. Exactly one succeeds — the `captain.kirk` account — and returns "IGNITION AUTHORIZED".

**3. Reassemble the flag.**
The successful response's headers carry three Base64 `deflector_part` fragments. Concatenating and decoding them gives the flag.

## Flag

```
Spooky{Be0m_Me_Up_Sc0tty_2266}
```

Flag recovered during the event.
