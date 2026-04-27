# Guide Etudiant - Escape Game Cyber

Bienvenue agent ! Sophie Dupont (`s.dupont@mega-corp.local`) a ete victime
d'une compromission. Vous etes l'equipe d'investigation. Reconstituez la
chaine d'attaque, recuperez les flags et atteignez le tresor final.

## Regles

- Chaque defi resolu fournit un **flag** au format `FLAG{...}` et un
  **indice** pour le suivant.
- Notez les flags au fur et a mesure. Le tresor final ne se debloque
  qu'avec les informations cumulees.
- Pas de force brute massive : la solution intellectuelle suffit.

## Point de depart

Une seule URL vous est fournie :

```
http://127.0.0.1:5000/mail
```

Bonne chasse.

## Outils utiles

- Navigateur + outils developpeur (clic-droit "Code source").
- `curl`, `nc` (netcat).
- Python 3 pour les decodages crypto / stegano.
- `xxd`, `strings`, `file`.

## Comment soumettre

Remettez vos 5 flags + le `FLAG_FINAL` dans un fichier `solution.txt`.
