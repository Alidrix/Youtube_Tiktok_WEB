# Monitoring The Trend Scope

## Objectif

La stack monitoring est optionnelle mais recommandée en préproduction et sur VPS.

## Services inclus

| Service | Rôle | Exposition |
| --- | --- | --- |
| Prometheus | Collecte métriques / règles | Interne |
| Alertmanager | Réception alertes Prometheus | Interne |
| Grafana | Dashboards | Via Traefik + Basic Auth |
| Loki | Logs | Interne |
| Promtail | Collecte logs | Interne |
| Node Exporter | Métriques hôte | Interne |
| cAdvisor | Métriques containers | Interne |
| Blackbox Exporter | Probes HTTP | Interne |

## Démarrage complet

```bash
docker compose --env-file .env.production \
  -f docker-compose.prod.yml \
  -f docker-compose.monitoring.yml \
  up -d prometheus alertmanager grafana loki promtail node-exporter cadvisor blackbox
```

## Vérification config

```bash
./scripts/prod-monitoring-check.sh
```

## Vérification stricte runtime

```bash
REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-monitoring-check.sh
```

## Test Alertmanager manuel

```bash
./scripts/prod-alerting-test.sh
```

```bash
REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-alerting-test.sh
```

## Dashboards

- Trend Scope Overview
- Trend Scope Infra

## Page admin monitoring

`/admin/monitoring`

Cette page est read-only, ne déclenche aucune commande Docker et affiche les endpoints et états runtime.

## Notifications Alertmanager

Par défaut, Alertmanager utilise un receiver neutre pour valider la chaîne Prometheus → Alertmanager sans notification externe.

Fichier actif :

```txt
infra/alertmanager/alertmanager.yml
```

Exemple webhook interne :

```txt
infra/alertmanager/alertmanager.webhook.example.yml
```

Ne jamais commiter de secrets SMTP, Telegram, webhook ou tokens dans les fichiers Alertmanager.
