# Chrome History Forensics — Evidence.zip

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** SOLVED and confirmed correct by Shikhu (2026-11-13)

## Flag

```
TVX{2,http://127.0.0.1:8000/review.html,completed,2026-10-10_22-16-02}
```

## Challenge

An employee was suspected of accessing an internal report through a local
web portal before downloading a document named `Q4_Report.txt`. The
incident response team recovered a Chrome browser History database and
the downloaded report. At first glance the records appear ordinary —
but a page remains referenced in the browser history that has no visit
record of its own.

File: `Evidence.zip` — Chrome History (SQLite) + `Q4_Report.txt`.

## Method

History SQLite, `urls` table:

```
1 = http://127.0.0.1:8000/portal.html
2 = http://127.0.0.1:8000/review.html
3 = http://127.0.0.1:8000/download.html
```

`visits` has id 1 (portal) and id 3 (download.html, `from_visit = 2`) —
visit id 2 is **missing** from `visits`. `context_annotations` still
retains `visit_id` 2, with review.html's timestamp, confirming visit 2
was review.html.

`downloads` id 10:

```
tab_referrer_url = http://127.0.0.1:8000/review.html
state = 1 (COMPLETE), received 89 / total 89 bytes
start_time = 13436144162088011 (Chrome time)
           = 2026-10-10 22:16:02 UTC
```

So the four answers:

- **Ans1 — 2:** the missing visit id.
- **Ans2 — http://127.0.0.1:8000/review.html:** the download row's
  `tab_referrer_url`.
- **Ans3 — completed:** the exact word in the question ("state = 1").
- **Ans4 — 2026-10-10_22-16-02:** the download start time.

## What was rejected first

`TVX{2,http://127.0.0.1:8000/review.html,complete,2026-10-10_22-16-02}`
and the `review.html` Ans2 form under "complete" were both rejected.
Ans1 and Ans4 were solid from the primary evidence, so the soft spot was
Ans3 — "complete" was the wrong word, not the page. Switching Ans3 to
"completed" (the exact word in the question) with Ans2 back to the full
URL as stored in `tab_referrer_url` was accepted. Shikhu confirmed:
"this is correct".

## Flag

```
TVX{2,http://127.0.0.1:8000/review.html,completed,2026-10-10_22-16-02}
```

Notes: `evidence/evidence-solve.txt`.
