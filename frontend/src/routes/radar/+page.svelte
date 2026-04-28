<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { token } from '$lib/stores/auth';
  import { fetchDailyRadar, scanVideos } from '$lib/api';
  import AppShell from '$lib/components/AppShell.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import KpiCard from '$lib/components/KpiCard.svelte';
  import PlatformTabs from '$lib/components/PlatformTabs.svelte';
  import FilterBar from '$lib/components/FilterBar.svelte';
  import TrendCard from '$lib/components/TrendCard.svelte';
  import LockedTrendCard from '$lib/components/LockedTrendCard.svelte';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import UpgradeModal from '$lib/components/UpgradeModal.svelte';

  let loading = true;
  let data: any = { trends: [], plan: 'free' };
  let error: string | null = null;
  let isAdmin = false;

  onMount(async () => {
    token.subscribe((value) => { if (!value) goto('/login'); })();
    try { data = await fetchDailyRadar(); } catch (e) { error = (e as Error).message; } finally { loading = false; }
  });
</script>

<AppShell {isAdmin} plan={data.plan || 'free'}>
  <PageHeader title="Radar du jour" subtitle="Aujourd’hui, les tendances qui accélèrent le plus." />

  <div class="kpis">
    <KpiCard label="Tendances détectées" value={String(data.trends?.length || 0)} />
    <KpiCard label="Vues/h moyennes" value={String(Math.round((data.trends?.reduce((a:number,t:any)=>a+(t.views_per_hour||0),0)/(data.trends?.length||1)) || 0))} />
    <KpiCard label="Niches en hausse" value="4" />
    <KpiCard label="Opportunités fortes" value="2" />
  </div>

  <PlatformTabs />
  <FilterBar />

  {#if loading}
    <p>Chargement du radar...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if !data.trends?.length}
    <EmptyState title="Aucune tendance disponible pour le moment." message="Les workers préparent les prochains signaux." />
    {#if isAdmin}<button on:click={scanVideos}>Lancer un scan</button>{/if}
  {:else}
    <div class="grid">
      {#each data.trends.slice(0, data.plan === 'free' ? 3 : data.trends.length) as trend}
        <TrendCard {trend} />
      {/each}
      {#if data.plan === 'free'}
        <LockedTrendCard /><LockedTrendCard />
      {/if}
    </div>
  {/if}
</AppShell>

<UpgradeModal visible={data.upgrade_required} message={data.message || ''} />

<style>
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.7rem;margin:1rem 0}
  .grid { display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.9rem;margin-top:.8rem }
  .error{color:var(--youtube)}
</style>
