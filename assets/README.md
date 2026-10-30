# Bannières, Badges et Statistiques du profil

## Bannières vectorielles

`zebda-banner.svg` et `zebda-footer.svg` sont des compositions vectorielles locales : texte, géométrie et palette graphite/violet de la présentation. Elles ne contiennent aucun script, suivi externe ou ressource distante. La bannière promotionnelle ImmoAlert est servie depuis les assets publics du dépôt ImmoAlert.

## Badges locaux (assets/badges/)

Tous les badges de stack technique (React 19, TypeScript, Vite, Python, Docker, etc.) ainsi que le badge Discord sont stockés localement en SVG dans `assets/badges/`.
Cela élimine tout appel réseau externe vers Shields.io lors du chargement de la page et résout définitivement les erreurs de proxy Camo (HTTP 504 Gateway Timeout).

## Statistiques GitHub et Streak

- `github-streak.svg` : généré quotidiennement par l'action GitHub Readme Streak Stats.
- `github-stats.svg` : résumé des étoiles, commits, PRs, issues et dépôts contribués.
- `top-langs.svg` : répartition des principaux langages utilisés.

Les cartes sont générées et validées automatiquement chaque jour à 03:15 UTC via le workflow `.github/workflows/streak-stats.yml` (script `.github/scripts/generate_stats.py`).
Le README lit directement les fichiers SVG locaux du dépôt et ne dépend plus d'instances tierces publiques instables (comme `github-readme-stats.vercel.app` sujette aux pannes Vercel / rate-limits).
