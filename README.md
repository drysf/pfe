# Escape Game Cyber - PFE L3B Groupe 3

**Escape game numérique cybersécurité** - VM avec 5 défis (SQLi/crypto/stego/réseau/mdp)

## 📋 Équipe
| Membre | Rôle |
|--------|------|
| Younes Beouch | Chef projet + Dev Python/Flask |
| Drys Ferhi | VM Vagrant/Docker |
| Sami Diah | Concepteur énigmes |
| Ryan Hassani | Testeur/intégrateur |

## 🎯 Objectif
VM autonome avec 5 défis progressifs menant au flag final : `CTF{GROUPE3_2026}`

## 📁 Structure projet
```
escape-game-cyber/
├── scripts/          # Python Flask : SQLi, crypto, stego, réseau
├── vm/               # Vagrantfile + Docker (Drys)
├── docs/             # Fiche projet + mémoire
├── tests/            # Scripts de test (Ryan)
└── README.md
```

## 🚀 Installation rapide
```bash
# Clone + lancement VM
git clone [repo]
cd vm/
vagrant up

# Accès aux défis
# Web :    http://localhost:5000
# Réseau : nc localhost 1337
```

## 🏆 Les 5 Défis
| # | Défi | Accès | Indice |
|---|------|-------|--------|
| 1 | **Mot de passe faible** | `/login` | `admin:password123` |
| 2 | **Injection SQL** | `/search` | `' OR 1=1 --` |
| 3 | **Cryptographie** | `/crypto` | déchiffrer `flag.enc` |
| 4 | **Stéganographie** | `/stego` | analyser `secret.png` |
| 5 | **Réseau** | `nc localhost 1337` | capturer le trafic |

## 📊 Avancement
- [x] Fiche projet Blackboard
- [x] Tableau Trello
- [ ] Développement défis (semaine prochaine)
- [ ] Tests d'intégration
- [ ] Livraison finale

## 🛠️ Technologies
- **Backend** : Python 3 / Flask
- **VM** : Vagrant + VirtualBox / Docker
- **OS cible** : Ubuntu Server 22.04
- **Outils** : Wireshark, Steghide, OpenSSL

---
*PFE L3B Groupe 3 — Année 2025/2026*
