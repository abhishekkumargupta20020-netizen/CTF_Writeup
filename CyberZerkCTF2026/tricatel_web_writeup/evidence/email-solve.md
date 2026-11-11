# Tricatel HR email — spoofing — SOLVED from the user's own file 2026-11-10
File: /home/hatch/workspace/user/files/note_du_drh.eml (uploaded by user 2026-11-10 06:50 UTC)
Spoof evidence (headers, verbatim from file):
- From: "Direction des Ressources Humaines" <drh@tricatel-cyber.fr>
- Return-Path: <attaquant@mail-cheap-relay.ru>
- Reply-To: <attaquant@mail-cheap-relay.ru>
- Received: from vps-unknown.mail-cheap-relay.ru (vps-unknown.mail-cheap-relay.ru [45.83.12.207]) by mx.tricatel-cyber.fr
- Received-SPF: fail (domain of drh@tricatel-cyber.fr does not designate 45.83.12.207 as permitted sender)
- Authentication-Results: spf=fail smtp.mailfrom=attaquant@mail-cheap-relay.ru; dkim=none; dmarc=fail (p=quarantine) header.from=tricatel-cyber.fr
- Message-ID: <20261113031449.9F2A1@mail-cheap-relay.ru>
Attachment note_interne_rh.txt (base64, decoded with Python email parser):
  NOTE INTERNE - CONFIDENTIEL RH / Objet : surveillance des arrets maladie
  Consigne: contester systematiquement les arrets de plus de 3 jours et bloquer les acces informatiques du salarie.
  Preuve de l'ordre : CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}
Flag: CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}
Note: in-chat assistant replied to this .eml at 06:50:36 UTC with a "try again in 11 hours" block; the flag above was decoded locally from the file, no live service needed.
