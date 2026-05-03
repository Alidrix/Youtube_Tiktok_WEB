<script lang='ts'>
  import StatusPill from '$lib/components/ui/StatusPill.svelte';
  export let status='pending'; export let label: string | undefined=undefined; export let tone: string | undefined=undefined;
  const labels:Record<string,string>={ok:'OK',error:'Erreur',warning:'Attention',manual:'Manuel',configured:'Configuré',not_configured:'Non configuré',coming_soon:'Bientôt',configured_but_not_implemented:'Configuré (non implémenté)',active:'Actif',inactive:'Inactif',pending:'En attente',completed:'Terminé',failed:'Échec',sent:'Envoyé',skipped:'Ignoré',logged:'Journalisé'};
</script>
<StatusPill status={tone ?? status} label={label ?? labels[status] ?? status} />
