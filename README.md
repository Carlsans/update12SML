# update12SML

> Files are commented in both English and French — read the comments before running anything.

---

## Requirements

- Arch-based Linux (cron job)
- The error notification system is **Linux only**
- Windows adaptation would require additional work

## Setup

**1. Virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Playwright** *(manual install required)*
```bash
pip install playwright
playwright install
```

**3. Credentials**

Add your WordPress username and password to `/src/credentials.json`.

**4. Configuration**

In `src/update12SML.py`, set:
- `WORDPRESS_URL`
- `MEETING_IMPORT_PAGE_URL`
- `SOURCE_COUNT` — adjust to match the number of sources you need to update

**5. Cron job**

Edit the last line of `/cron/updatemeetings.sh` to match your setup, then configure your cron task to use that file.

---

## Contributing

Pull requests are appreciated — making this work on Windows would be a great addition.

---
---

# update12SML

> Les fichiers sont commentés en anglais et en français — lisez les commentaires avant d'exécuter quoi que ce soit.

---

## Prérequis

- Linux basé sur Arch (tâche cron)
- Le système de notifications d'erreurs est **Linux uniquement**
- Une adaptation pour Windows nécessiterait des modifications supplémentaires

## Installation

**1. Environnement virtuel**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**2. Playwright** *(installation manuelle requise)*
```bash
pip install playwright
playwright install
```

**3. Identifiants**

Ajoutez votre nom d'utilisateur et mot de passe WordPress dans `/src/credentials.json`.

**4. Configuration**

Dans `src/update12SML.py`, définissez :
- `WORDPRESS_URL`
- `MEETING_IMPORT_PAGE_URL`
- `SOURCE_COUNT` — à ajuster selon le nombre de sources à mettre à jour

**5. Tâche cron**

Modifiez la dernière ligne de `/cron/updatemeetings.sh` selon votre configuration, puis configurez votre tâche cron pour utiliser ce fichier.

---

## Contribuer

Les pull requests sont les bienvenues — adapter le projet pour Windows serait une excellente contribution.
