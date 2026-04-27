# Walkthrough (CONFIDENTIEL - encadrants uniquement)

Solution complete des 5 defis.

## Defi 1 - Injection SQL

- Aller sur `http://127.0.0.1:5000/mail`. Le code source contient le
  commentaire `<!-- DEBUG: requete brute => SELECT * FROM users WHERE
  username='?' AND password='?' -->`.
- Sur `/`, payload classique :

  ```
  username: ' OR '1'='1' --
  password: n'importe
  ```

- Reponse : `FLAG{M41L_P1R4T3_SQL1}` + indice : *cle Vigenere = SOPHIE,
  fichier `assets/secret.enc`*.

## Defi 2 - Vigenere

```bash
python scripts/challenge2_crypto.py decrypt SOPHIE
```

Affiche : `FLAG{C35AR_3T_V1G3N3R3_S0NT_M0RTS}` + passphrase `pixels2026`
+ chemin `assets/carte_postale.png`.

## Defi 3 - Steganographie LSB

```bash
python scripts/challenge3_stego.py extract assets/carte_postale.png
```

Affiche : `FLAG{P1X3LS_QU1_PARL3NT}` + endpoint `127.0.0.1:4242` + token
`TOKEN-LSB-OK`.

## Defi 4 - Service TCP

```bash
nc 127.0.0.1 4242
> AUTH TOKEN-LSB-OK
```

Renvoie : `FLAG{S0CK3T_M4ST3R_2026}` + mot de passe AES `k1ng_0f_th3_h1ll`.

## Defi 5 - Tresor AES-256-GCM

```bash
python scripts/challenge5_final.py decrypt k1ng_0f_th3_h1ll
```

Affiche : `FLAG{ESC4P3_G4M3_PFE_L3B_G3_W1N}`.

## Verification automatique

```bash
make test
```

Le test `test_chaine_complete_de_bout_en_bout` rejoue toute la chaine.
