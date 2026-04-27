# Architecture du projet

```
pfe/
|-- scripts/                Code source des 5 defis
|   |-- common.py           Constantes partagees (flags, cles, ports)
|   |-- challenge1_web.py   Defi 1 - Flask + SQL Injection
|   |-- challenge2_crypto.py Defi 2 - Chiffre de Vigenere
|   |-- challenge3_stego.py  Defi 3 - Steganographie LSB (Pillow)
|   |-- challenge4_socket.py Defi 4 - Serveur TCP authentifie
|   |-- challenge5_final.py  Defi 5 - AES-256-GCM (cryptography)
|   |-- generate_assets.py   Genere tresor.aes / secret.enc / image
|   |-- orchestrator.py      Lance defis 1 + 4 dans un meme process
|   `-- requirements.txt
|-- assets/                 Artefacts generes (binaires, images)
|-- tests/                  Tests pytest (unitaires + chaine complete)
|-- vm/                     Dockerfile + docker-compose
|-- docs/                   Guides etudiants et walkthrough
|-- Makefile                Cibles install / run / test / docker-up
`-- README.md
```

## Domaines de cybersecurite couverts

| Defi | Domaine          | Outils etudies            |
|------|------------------|---------------------------|
| 1    | Web / OWASP A03  | Burp / curl / DevTools    |
| 2    | Cryptographie    | CyberChef, scripts Python |
| 3    | Forensic / Stego | Pillow, exiftool, binwalk |
| 4    | Reseau           | nmap, netcat              |
| 5    | Crypto symetrique| openssl, cryptography     |

## Logique de chainage

Chaque defi expose une information indispensable pour le suivant :

```
SQLi  -> cle Vigenere "SOPHIE"
Vigenere -> passphrase + chemin image
Stego -> token + endpoint TCP
Socket TCP -> mot de passe AES
AES -> FLAG_FINAL
```

L'equipe doit donc cooperer et progresser lineairement (criteres
pedagogiques de la fiche projet).

## Repartition equipe (PFE L3B Groupe 3)

- **Younes** : `challenge1_web.py` (Flask, SQLi).
- **Drys**   : `vm/` (Dockerfile, compose, deploiement).
- **Sami**   : `challenge2_crypto.py`, `challenge3_stego.py`.
- **Ryan**   : `tests/` (pytest), `challenge4_socket.py`,
  `challenge5_final.py`, documentation.
