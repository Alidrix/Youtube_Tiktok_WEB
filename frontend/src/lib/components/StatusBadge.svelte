<script lang="ts">
export let status='pending'; export let label: string | undefined=undefined; export let tone: string | undefined=undefined;
const labels:Record<string,string>={ok:'OK',error:'Erreur',warning:'Attention',manual:'Manuel',configured:'Configuré',not_configured:'Non configuré',coming_soon:'Bientôt',configured_but_not_implemented:'Configuré (non implémenté)',active:'Actif',inactive:'Inactif',pending:'En attente',completed:'Terminé',failed:'Échec',sent:'Envoyé',skipped:'Ignoré',logged:'Journalisé'};
</script>
<span class={`badge ${tone ?? status}`}>{label ?? labels[status] ?? status}</span>
<style>
.badge{padding:.2rem .6rem;border-radius:999px;font-size:.75rem;border:1px solid var(--border);color:var(--text)}
.ok,.configured,.sent,.completed,.active{background:color-mix(in srgb,#2f9e44 18%, transparent)}
.warning,.manual,.coming_soon,.pending,.logged,.skipped{background:color-mix(in srgb,#f08c00 18%, transparent)}
.error,.not_configured,.failed,.inactive{background:color-mix(in srgb,#c92a2a 18%, transparent)}
</style>
