# Escape Game Cyber - PFE L3B Groupe 3

Projet 2025/2026 - LSI L3B - Groupe 3.
Implementation du sujet **"Escape Game Cybersecurite"** (Fiche Projet Cyber).

## Equipe

- **Younes** - Defi 1 (Flask / SQLi)
- **Drys**   - Containerisation (Docker)
- **Sami**   - Defis 2 et 3 (Crypto / Stegano)
- **Ryan**   - Defis 4 et 5 (Socket / AES) + Tests + Docs

## Synopsis

Sophie Dupont, employee de MegaCorp, a ete piratee. Les etudiants doivent
reconstituer la chaine d'attaque a travers 5 defis chaines couvrant
**web, cryptographie, forensic / steganographie, reseau et crypto
symetrique**, jusqu'au tresor final.

## Demarrage rapide

```bash
# Installation
make install

# Generation des artefacts (image stego, fichier chiffre, tresor)
make assets

# Lancement (web port 5000 + socket port 4242)
make run

# Ou via Docker
make docker-up
```

Ouvrir ensuite `http://127.0.0.1:5000/mail`.

## Tests

```bash
make test
```

12 tests pytest dont un test de bout en bout qui rejoue les 5 defis.

## Documentation

- [Guide etudiant](docs/student_guide.md)
- [Walkthrough (encadrants)](docs/walkthrough.md)
- [Architecture](docs/architecture.md)

## Domaines couverts

Web (OWASP A03 - Injection), Cryptographie classique (Vigenere),
Steganographie (LSB sur PNG), Reseau (TCP authentifie),
Crypto moderne (AES-256-GCM + scrypt KDF).
