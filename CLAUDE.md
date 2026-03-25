# Sign of the Times — Contexte projet

## Sites gérés
- signofthetimes.watch → /var/www/steeve/
- potatochipsdelisandwich.com → /var/www/pcd/
- playamundomaya.land → /var/www/playamundomaya/

## Stack technique
- HTML/CSS statique + admin_api.py (Python HTTPServer, port 8084)
- Nginx en reverse proxy avec SSL Let's Encrypt
- Multilingue : EN / FR / RU (via JS data-i18n)
- Données montres dans watches.json (source unique de vérité)

## Architecture
```
/var/www/steeve/
├── index.html          ← homepage (multilingue EN/FR/RU)
├── collection.html     ← grille de toutes les montres
├── watch.html          ← page détail montre
├── decades.html        ← navigation par décennie
├── brand.html          ← navigation par marque
├── gone-too-soon.html  ← montres vendues
├── upgrade-trade.html  ← page upgrade/trade
├── admin/              ← panneau CMS (password: signoftimes2026)
├── admin_api.py        ← API backend (port 8084, @reboot cron)
├── watches.json        ← données des 12 montres (source de vérité)
└── images/             ← photos montres (watch01.jpg–watch18.jpg)
```

## Client
- Steeve (propriétaire)
- Email : steeve@signofthetimes.watch
- Téléphone : +351926650503
- Rappels hebdo (lun-ven 09:00 UTC) pour fournir données réelles

## Données en attente de Steeve
- Noms réels des montres
- Prix (ou confirmation "Price on request")
- Photos supplémentaires
- Accès Facebook page (pour admin)

## Admin CMS
- URL : https://signofthetimes.watch/admin/
- Mot de passe : signoftimes2026
- Fonctions : add/edit/delete watches, upload photos, mark sold
- API port 8084, cron @reboot

## Règles de sécurité (OBLIGATOIRES)
- Pas de credentials dans le code
- /admin/ accessible mais avec mot de passe
- Jamais de données sensibles dans le dossier public

## Règles de qualité (OBLIGATOIRES)
- Copyright © 2026 (EN + FR + RU dans les JSON de traduction)
- rel="noopener noreferrer" sur tous les target="_blank"
- JSON-LD complet : telephone +351926650503, domaine signofthetimes.watch
- Cohérence des données entre watches.json, index.html et collection.html
- Multilingue : toute modification de texte doit être faite dans les 3 langues

## Workflow de développement
1. Analyser → lister les problèmes avec leur gravité
2. Attendre validation avant de modifier
3. Corriger → vérifier que ça fonctionne
4. Confirmer avec preuve (curl, grep, test live)

## Règles d'économie de tokens

RÉPONSES :
- Sois concis — pas de phrases d'introduction inutiles
- Pas de "Je vais maintenant..." ou "Bien sûr, je vais..."
- Réponds directement sans reformuler la question
- Utilise des listes courtes plutôt que des paragraphes

CODE :
- Ne montre que les lignes modifiées, pas tout le fichier
- Utilise diff format quand possible (+/- lignes)
- Ne répète pas le code déjà montré

CONFIRMATION :
- Pour les petites tâches, juste "✅ fait" suffit
- Pas besoin d'expliquer chaque étape évidente

## Règle gestion contexte

RÈGLE ABSOLUE :
- /compact toutes les 10 messages
- /clear entre chaque projet différent
- Ne jamais laisser le contexte dépasser 50k tokens
- Vérifier avec /tokens avant chaque grosse tâche

## Règle lecture de fichiers

Ne jamais lire un fichier entier — utilise toujours :
- grep -n "terme" fichier (chercher)
- sed -n '10,50p' fichier (lire lignes 10-50 seulement)
- wc -l fichier (compter les lignes avant de lire)
