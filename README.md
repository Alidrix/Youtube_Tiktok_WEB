# Viral Radar

Viral Radar est une plateforme SaaS de veille virale destinée à détecter les tendances émergentes sur YouTube, puis à terme sur TikTok et Instagram.

L'objectif produit est simple : permettre aux créateurs, influenceurs, agences et marques d'identifier les contenus qui commencent à exploser avant qu'ils soient saturés.

La plateforme doit rester claire, accessible et orientée action : l'utilisateur se connecte, arrive sur son radar du jour, voit immédiatement les tendances utiles, puis peut passer à une offre payante pour débloquer l'accès complet.

## Stack

- Backend : Rust, Axum, SQLx, PostgreSQL
- Frontend : SvelteKit, TypeScript, Vite
- Infra : Docker Compose
- Base : PostgreSQL / Supabase
- Source actuelle : YouTube Data API v3
- Sources cibles : YouTube, TikTok, Instagram

## Vision produit

Viral Radar doit évoluer vers une plateforme publique à abonnement permettant d'accéder à :

- des vidéos en forte croissance ;
- des classements par plateforme ;
- des tendances par pays, catégorie et niche ;
- des métriques simples comme les vues par heure ;
- des scores de potentiel viral ;
- des signaux faibles avant saturation ;
- des recommandations exploitables pour créer du contenu.

Le produit ne doit pas seulement afficher les contenus déjà populaires. Il doit surtout faire remonter les contenus en accélération.

Phrase produit cible :

> Repère les tendances avant les autres et crée du contenu au bon moment.

## Positionnement SaaS

Architecture cible pour une exposition publique :

| Bloc | Rôle |
| --- | --- |
| Frontend public | Landing page, tarifs, inscription, connexion |
| Dashboard abonné | Radar, tendances, filtres, statistiques, favoris |
| Backend API privé | Agrégation, scoring, authentification, quotas utilisateur |
| Worker de scan | Collecte planifiée YouTube, TikTok, Instagram |
| Base de données | Vidéos, statistiques, utilisateurs, plans, limites |
| Paiement | Abonnements mensuels, contrôle des accès |
| Admin | Supervision utilisateurs, quotas API, workers et logs |

Le frontend public peut être visible par tous. Les données avancées restent derrière authentification et abonnement.

## Offres commerciales retenues

La gamme retenue repose sur 3 offres simples : Free, Pro et Studio.

| Plan | Prix | Cible | Accès |
| --- | ---: | --- | --- |
| Free | 0 € | Découverte | 3 tendances visibles par jour |
| Pro | 10 €/mois | Créateurs et influenceurs | Tendances illimitées + filtres + favoris + statistiques standards |
| Studio | 18 €/mois | Créateurs avancés, agences, marques | Statistiques avancées + alertes + rapports + historique étendu |

### Plan Free

Objectif : permettre à l'utilisateur de tester rapidement la valeur du produit.

Limite recommandée :

- 3 tendances visibles par jour ;
- idéalement 1 YouTube + 1 TikTok + 1 Instagram lorsque les 3 plateformes seront disponibles ;
- données basiques uniquement ;
- pas d'historique long ;
- pas d'export ;
- pas d'alertes ;
- upgrade visible vers le plan Pro.

Données affichées en Free :

- plateforme ;
- thumbnail ;
- titre ;
- catégorie ;
- score tendance simplifié ;
- vues par heure simplifiées.

Message de limite :

```txt
Tu as consulté tes 3 tendances gratuites du jour.
Passe en Pro pour débloquer toutes les tendances.
```

### Plan Pro — 10 €/mois

Objectif : offre principale du produit.

Fonctionnalités :

- tendances illimitées ;
- accès YouTube, TikTok et Instagram à terme ;
- filtres par plateforme ;
- filtres par pays ;
- filtres par catégorie ;
- filtres par format ;
- score tendance ;
- vues par heure ;
- favoris ;
- notes privées ;
- historique court, par exemple 7 jours ;
- dashboard complet.

Le plan Pro doit être l'offre mise en avant.

### Plan Studio — 18 €/mois

Objectif : apporter de la décision et de l'analyse avancée, pas seulement plus de données.

Fonctionnalités recommandées :

- historique étendu 30 à 90 jours ;
- courbes d'évolution ;
- alertes personnalisées ;
- rapports hebdomadaires ;
- exports CSV/PDF ;
- tendances cross-platform ;
- comparaison YouTube / TikTok / Instagram ;
- score d'opportunité ;
- score de saturation ;
- détection des signaux faibles ;
- top créateurs ou chaînes en accélération ;
- watchlist de niches ;
- recommandations d'angles de contenu ;
- analyse des catégories montantes.

Promesse Studio :

> Ne regarde pas seulement ce qui buzz. Comprends pourquoi ça buzz et quoi publier ensuite.

## Règles d'accès produit

Le backend doit gérer les droits selon le plan utilisateur.

Modèle fonctionnel cible :

```txt
user_plan = free | pro | studio
daily_trend_limit = 3 | unlimited | unlimited
platform_access = limited | all | all
stats_access_level = basic | standard | advanced
history_days = 0 | 7 | 90
exports_enabled = false | false | true
alerts_enabled = false | false | true
reports_enabled = false | false | true
```

Les limitations doivent être appliquées côté backend. Le frontend peut masquer ou flouter certains éléments, mais ne doit pas être le seul mécanisme de contrôle.

## Expérience utilisateur cible

Parcours idéal :

1. l'utilisateur arrive sur la landing page ;
2. il crée un compte ou se connecte ;
3. il arrive directement sur le Radar du jour ;
4. il voit ses 3 tendances gratuites ;
5. il peut filtrer simplement par plateforme ;
6. lorsqu'il atteint la limite, un écran d'upgrade lui propose le plan Pro ;
7. après paiement, il débloque les tendances illimitées.

La page principale après connexion doit être le Radar, pas une page technique.

Navigation cible :

```txt
Radar
Plateformes
Favoris
Alertes
Rapports
Abonnement
Paramètres
```

Pour le MVP, garder une navigation plus courte :

```txt
Radar
Favoris
Abonnement
Paramètres
```

## Dashboard cible

La page principale doit répondre à une question :

> Qu'est-ce qui est en train d'exploser aujourd'hui ?

Structure recommandée :

```txt
Bonjour 👋
Voici les tendances qui accélèrent aujourd'hui.

[ YouTube ] [ TikTok ] [ Instagram ] [ Toutes ]

KPI :
- tendances détectées
- niches en hausse
- tendances cross-platform
- opportunités fortes

Liste des tendances :
- thumbnail
- titre
- plateforme
- score tendance
- vues par heure
- catégorie
- pays
- bouton favoris
- bouton détails
```

Pour le plan Free, afficher 3 cartes visibles puis verrouiller ou flouter le reste.

## Scores métier à prévoir

Les scores doivent simplifier la lecture des données.

| Score | Utilité |
| --- | --- |
| Trend Score | Potentiel viral global |
| Velocity Score | Vitesse de progression |
| Freshness Score | Opportunité encore récente |
| Saturation Score | Niveau de saturation de la tendance |
| Opportunity Score | Intérêt à créer du contenu maintenant |
| Category Rank | Position dans une catégorie donnée |
| Region Rank | Position dans un pays ou une zone |
| Channel Momentum | Progression d'une chaîne ou d'un créateur |

Exemple d'affichage :

```txt
Trend Score : 92/100
Opportunité : Très forte
Saturation : Faible
```

## Direction artistique

Le produit ne doit pas donner une impression d'outil IA générique.

À éviter :

- robots ;
- wording trop IA ;
- effets néon excessifs ;
- fond violet/bleu trop générique ;
- particules futuristes ;
- dashboard trop chargé ;
- jargon technique visible par l'utilisateur final.

À privilégier :

- interface claire et premium ;
- style social analytics ;
- thumbnails bien visibles ;
- cartes lisibles ;
- accents YouTube rouge, TikTok cyan/rose, Instagram gradient léger ;
- typographie moderne et simple ;
- beaucoup d'espace ;
- filtres faciles ;
- données transformées en décisions.

Références d'esprit :

- YouTube Studio ;
- Spotify for Artists ;
- Stripe Dashboard ;
- Linear ;
- Notion ;
- Metricool ;
- Later ;
- HypeAuditor.

## Gestion de la clé API YouTube

Pour un vrai modèle SaaS, la plateforme utilise une ou plusieurs clés YouTube contrôlées par l'éditeur de Viral Radar.

Les clients ne doivent pas renseigner leur propre clé API dans l'offre standard.

Avantages :

- expérience utilisateur plus simple ;
- aucun paramétrage Google Cloud demandé au client ;
- cache global partagé entre les abonnés ;
- meilleure maîtrise des quotas ;
- meilleure qualité de donnée.

Contraintes :

- surveiller les quotas YouTube ;
- éviter les scans inutiles ;
- mettre en cache les résultats ;
- dédupliquer les appels API ;
- ne jamais exposer la clé au frontend.

Option future : permettre à un client entreprise ou self-hosted d'ajouter sa propre clé API.

## Moteur de détection des tendances

Le moteur de tendance doit évoluer au-delà d'un simple classement par vues.

Métriques recommandées :

| Métrique | Description |
| --- | --- |
| `views_per_hour` | Nombre moyen de vues gagnées par heure depuis la publication |
| `velocity_score` | Score d'accélération basé sur la progression récente |
| `trend_score` | Score global combinant vues, âge, catégorie et croissance |
| `freshness_score` | Priorise les contenus récents encore exploitables |
| `category_rank` | Classement par catégorie ou domaine |
| `region_rank` | Classement par pays ou zone géographique |
| `shorts_ratio` | Part des Shorts dans les tendances détectées |
| `channel_momentum` | Détection des chaînes en forte progression |

Objectif : identifier non seulement ce qui est déjà viral, mais surtout ce qui est en train de le devenir.

## Utilisateurs cibles

| Segment | Besoin |
| --- | --- |
| Influenceurs | Trouver des idées de contenus à fort potentiel |
| Créateurs YouTube/TikTok | Comprendre les formats et sujets qui performent |
| Agences social media | Préparer des recommandations clients basées sur la donnée |
| Marques | Surveiller les tendances de marché et opportunités éditoriales |
| Growth marketers | Identifier rapidement des angles de contenu exploitables |
| Veilleurs / analystes | Suivre les mouvements culturels ou commerciaux émergents |

## Fonctionnalités SaaS à prévoir

Fonctionnalités publiques :

- landing page marketing ;
- page tarifs ;
- inscription ;
- connexion ;
- démonstration limitée ;
- aperçu de quelques tendances gratuites.

Fonctionnalités abonnés :

- dashboard complet ;
- classement mondial ;
- filtres par pays, catégorie, thème, durée, format ;
- statistiques vues par heure ;
- détection des tendances émergentes ;
- historique de progression ;
- favoris ;
- notes privées ;
- exports CSV/PDF ;
- alertes personnalisées ;
- recommandations de niches et catégories.

Fonctionnalités admin :

- gestion des utilisateurs ;
- gestion des plans d'abonnement ;
- suivi des quotas API ;
- supervision des jobs de scan ;
- logs techniques ;
- état des sources YouTube/TikTok/Instagram ;
- désactivation temporaire d'une source en cas de quota ou incident.

## Priorités MVP commercial

Ordre de développement recommandé :

1. système utilisateur + plan d'abonnement ;
2. limite Free à 3 tendances par jour ;
3. page Pricing ;
4. page Radar du jour ;
5. cartes tendances propres avec thumbnails ;
6. score tendance simple ;
7. filtres plateforme / pays / catégorie ;
8. favoris ;
9. page abonnement ;
10. paiement Stripe ;
11. watchlist ;
12. alertes Studio ;
13. rapports Studio.

MVP vendable :

- landing page ;
- pricing ;
- inscription / connexion ;
- plan gratuit limité ;
- dashboard Radar ;
- YouTube fonctionnel ;
- TikTok et Instagram prévus dans l'UI ;
- cartes tendances avec score ;
- favoris ;
- upgrade Pro.

## Roadmap produit long terme

### Phase 1 — Stabilisation YouTube

- stabiliser Docker et CI ;
- fiabiliser le scan YouTube ;
- calculer les vues par heure ;
- ajouter les catégories, régions et thumbnails ;
- créer un premier scoring de tendance ;
- améliorer le dashboard.

### Phase 2 — SaaS public

- ajouter une landing page publique ;
- ajouter inscription et gestion utilisateur ;
- ajouter plans d'abonnement ;
- connecter un prestataire de paiement ;
- protéger les routes premium ;
- créer un dashboard abonné ;
- ajouter une limite d'accès selon le plan.

### Phase 3 — Intelligence de tendance

- ajouter un moteur de scoring avancé ;
- historiser la croissance des vidéos ;
- détecter les signaux faibles ;
- ajouter des alertes personnalisées ;
- créer des recommandations par niche ;
- ajouter des rapports automatiques.

### Phase 4 — TikTok

- ajouter une source TikTok ;
- normaliser les données TikTok dans le même modèle que YouTube ;
- créer un classement TikTok ;
- comparer les tendances YouTube et TikTok ;
- détecter les tendances cross-platform.

### Phase 5 — Instagram

- ajouter une source Instagram ;
- intégrer Reels et contenus courts ;
- créer des statistiques par compte, catégorie et format ;
- centraliser YouTube, TikTok et Instagram dans un seul radar.

### Phase 6 — Plateforme complète

- API publique ou API partenaire ;
- webhooks ;
- exports avancés ;
- espace agence ;
- multi-utilisateurs par organisation ;
- dashboard marque blanche ;
- recommandations d'angles de contenu.

## Démarrage rapide

```bash
cp .env.example .env
docker compose build --no-cache
docker compose up -d
docker compose ps
```

Services :

- Frontend : http://localhost:5173
- Backend : http://localhost:4443/api/v1
- Health : http://localhost:4443/api/v1/health

## Procédure complète — Démarrer l'infrastructure et accéder à la plateforme

### 1. Cloner le projet

```bash
git clone https://github.com/Alidrix/Youtube_Tiktok_WEB.git
cd Youtube_Tiktok_WEB
```

Si vous travaillez depuis la branche de développement de la PR :

```bash
git checkout codex/fix-docker-backend-build-issues
```

### 2. Préparer le fichier d'environnement

```bash
cp .env.example .env
nano .env
```

Variables minimales à vérifier :

| Variable | Rôle | Exemple attendu |
| --- | --- | --- |
| `APP_USERNAME` | Identifiant du compte initial | `admin` |
| `APP_PASSWORD` | Mot de passe du compte initial | mot de passe robuste |
| `SECRET_KEY` | Secret utilisé pour signer les JWT | résultat de `openssl rand -hex 32` |
| `DATABASE_URL` | Connexion PostgreSQL Supabase | doit contenir `sslmode=require` |
| `YOUTUBE_API_KEY` | Clé API YouTube Data API v3 | clé générée côté Google Cloud |
| `REGIONS` | Régions à scanner | `FR,US,ES` |
| `THEMES` | Thèmes à surveiller | `business,drole,voiture` |
| `FRONTEND_ORIGIN` | Origine autorisée du frontend | `http://localhost:5173` |

Générer un secret applicatif :

```bash
openssl rand -hex 32
```

Ne jamais commiter le fichier `.env`.

### 3. Construire les images Docker

```bash
docker compose build --no-cache
```

### 4. Démarrer l'infrastructure

```bash
docker compose up -d
docker compose ps
```

État attendu :

```txt
backend    running / healthy
frontend   running
```

### 5. Vérifier que l'API répond

```bash
curl -i http://localhost:4443/api/v1/health
curl -i http://localhost:4443/api/v1/auth/status
```

### 6. Accéder à la plateforme

Ouvrir :

```txt
http://localhost:5173
```

Puis :

1. ouvrir la page de connexion ;
2. se connecter avec `APP_USERNAME` et `APP_PASSWORD` ;
3. accéder au dashboard ;
4. cliquer sur **Scanner maintenant** ;
5. vérifier que les vidéos remontent dans le radar.

### 7. Consulter les logs

```bash
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
```

### 8. Redémarrer ou arrêter

```bash
docker compose restart
docker compose down
```

Rebuild complet :

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## Exposition publique et prérequis production

Avant exposition publique, prévoir :

- reverse proxy HTTPS ;
- domaine dédié ;
- authentification renforcée ;
- stockage serveur des clés API ;
- aucun secret dans le navigateur ;
- rate limiting ;
- système d'abonnement ;
- contrôle d'accès backend ;
- monitoring des quotas YouTube ;
- logs applicatifs ;
- sauvegardes PostgreSQL ;
- politique de cache ;
- supervision des workers de scan.

La clé YouTube doit rester côté serveur. Elle ne doit jamais être exposée dans le frontend, les réponses API publiques ou le navigateur.

## API

- `GET /api/v1/health`
- `GET /api/v1/auth/status`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/videos` (auth)
- `POST /api/v1/videos` (auth, compat historique)
- `POST /api/v1/videos/scan` (auth, scan YouTube réel)
- `POST /api/v1/notes` (auth)

Réponse scan :

```json
{
  "message": "scan completed",
  "inserted": 12,
  "updated": 8,
  "total": 20
}
```

## Qualité locale

```bash
cd backend
cargo fmt --check
cargo clippy -- -D warnings
cargo test

cd ../frontend
npm ci
npm run check
npm run build

cd ..
docker compose build
```

## CI

Workflow GitHub Actions : `.github/workflows/ci.yml`

- job backend : fmt, clippy, test ;
- job frontend : npm ci, check, build ;
- job docker : docker compose build.

## Troubleshooting

| Problème | Vérification |
| --- | --- |
| Backend KO | vérifier `DATABASE_URL`, `sslmode=require` et logs backend |
| Frontend KO | vérifier que le port `5173` est disponible |
| Dashboard vide | vérifier `YOUTUBE_API_KEY`, quotas API et bouton **Scanner maintenant** |
| Login KO | vérifier `APP_USERNAME` et `APP_PASSWORD` |
| API inaccessible | vérifier `VITE_API_BASE` et `docker compose ps` |

## Roadmap courte

- Stabiliser le score de tendance YouTube
- Ajouter un système d'abonnement Free / Pro / Studio
- Ajouter la limite Free à 3 tendances par jour
- Ajouter une page Pricing
- Ajouter Stripe
- Ajouter un worker de scan planifié
- Ajouter TikTok côté backend
- Ajouter Instagram côté backend
- Ajouter les alertes Studio
- Ajouter les rapports Studio
