<script lang="ts">
  import { onMount } from 'svelte';

  import { fetchAdminMonitoringStatus, type AdminMonitoringStatus } from '$lib/api';
  import AdminSection from '$lib/components/AdminSection.svelte';
  import CommandBlock from '$lib/components/ui/CommandBlock.svelte';
  import EmptyState from '$lib/components/ui/EmptyState.svelte';
  import SkeletonBlock from '$lib/components/ui/SkeletonBlock.svelte';
  import AdminStatCard from '$lib/components/AdminStatCard.svelte';
  import AdminStatusList from '$lib/components/AdminStatusList.svelte';
  import AdminToolbar from '$lib/components/AdminToolbar.svelte';
  import AppShell from '$lib/components/AppShell.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import { getErrorMessage } from '$lib/errors';
  import { currentUser } from '$lib/stores/user';

  let loading = true;
  let error = '';
  let data: AdminMonitoringStatus | null = null;

  const serviceCards: Array<{ label: string; key: keyof NonNullable<AdminMonitoringStatus['services']> }> = [
    { label: 'Prometheus', key: 'prometheus' },
    { label: 'Grafana', key: 'grafana' },
    { label: 'Loki', key: 'loki' },
    { label: 'Alertmanager', key: 'alertmanager' },
    { label: 'Blackbox', key: 'blackbox' },
    { label: 'Node Exporter', key: 'node_exporter' },
    { label: 'cAdvisor', key: 'cadvisor' }
  ];

  const columns = [
    { key: 'service', label: 'Service' },
    { key: 'url', label: 'URL' }
  ];

  const load = async () => {
    loading = true;
    error = '';

    try {
      data = await fetchAdminMonitoringStatus();
    } catch (err: unknown) {
      error = getErrorMessage(err, 'Failed to load monitoring status');
    } finally {
      loading = false;
    }
  };

  const endpointRows = () =>
    Object.entries(data?.endpoints ?? {}).map(([service, url]) => ({
      service,
      url
    }));

  const strictModeCommand = 'REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-monitoring-check.sh';
  const strictModeStatus = 'disabled by default (REQUIRE_MONITORING_RUNNING=0)';

  onMount(load);
</script>

<AppShell>
  {#if $currentUser?.role !== 'admin'}
    <p>Accès restreint</p>
  {:else}
    <PageHeader title="Admin monitoring" subtitle="Observabilité runtime read-only" />
    {#if loading}<SkeletonBlock lines={4} />{/if}
    {#if !loading && error}<EmptyState title="Monitoring indisponible" message={error} tone="error" />{/if}
    <p class="helper-note">Cette page vérifie uniquement l’état runtime de la stack monitoring. Les commandes restent à exécuter manuellement sur le VPS.</p>

    <AdminToolbar {loading} {error}>
      <button type="button" on:click={load} disabled={loading}>Refresh</button>
    </AdminToolbar>

    <AdminSection title="Résumé monitoring">
      <div class="stats-grid">
        <AdminStatCard
          label="Global status"
          value={data?.status ?? 'unknown'}
          status={data?.status ?? 'warning'}
        />

        {#each serviceCards as service}
          <AdminStatCard
            label={service.label}
            value={data?.services?.[service.key] ?? 'unknown'}
            status={data?.services?.[service.key] ?? 'warning'}
          />
        {/each}
      </div>
    </AdminSection>

    <AdminSection title="Services">
      <AdminStatusList
        items={Object.entries(data?.services ?? {}).map(([label, status]) => ({
          label,
          status
        }))}
      />
    </AdminSection>

    <AdminSection title="Endpoints">
      <DataTable {columns} rows={endpointRows()} />
    </AdminSection>

    
    <AdminSection title="Go/No-Go monitoring">
      <CommandBlock command="./scripts/prod-monitoring-check.sh" />
      <CommandBlock command="REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-monitoring-check.sh" />
      <CommandBlock command="SKIP_ALERTING_TEST=0 REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-go-no-go.sh" />
    </AdminSection>

    <AdminSection title="Mode strict">
      <div class="strict-grid">
        <AdminStatCard label="Strict mode" value={strictModeStatus} status="warning" />
        <AdminStatCard
          label="Alertmanager runtime"
          value={data?.services?.alertmanager ?? 'unknown'}
          status={data?.services?.alertmanager ?? 'warning'}
        />
      </div>
      <CommandBlock command={strictModeCommand} />
    </AdminSection>

    <AdminSection title="Alerting test">
      <CommandBlock command="./scripts/prod-alerting-test.sh" />
      <CommandBlock command="REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-alerting-test.sh" />
    </AdminSection>

    <AdminSection title="Documentation">
      <CommandBlock command="docker compose --env-file .env.production -f docker-compose.prod.yml -f docker-compose.monitoring.yml ps" />
      <CommandBlock command="docs/monitoring.md" copyable={false} />
      <CommandBlock command="SKIP_MONITORING_CHECK=1 ./scripts/prod-go-no-go.sh" />
    </AdminSection>
  {/if}
</AppShell>



<style>
  .helper-note {
    margin: 0.25rem 0 1rem;
    color: var(--muted);
  }

  .stats-grid,
  .strict-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.75rem;
  }

</style>
