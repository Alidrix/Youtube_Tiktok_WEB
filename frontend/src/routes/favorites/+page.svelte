<script lang="ts">
  import AppShell from '$lib/components/AppShell.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import EmptyState from '$lib/components/EmptyState.svelte';
  let favorites: any[] = [];
</script>

<AppShell>
  <PageHeader title="Favoris" subtitle="Retrouvez vos tendances sauvegardées." />
  {#if favorites.length === 0}
    <EmptyState title="Vous n’avez pas encore sauvegardé de tendance." message="Ajoutez des tendances depuis votre Radar du jour pour les retrouver ici." />
  {/if}
</AppShell>
