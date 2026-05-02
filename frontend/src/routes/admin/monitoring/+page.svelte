<script lang="ts">
  import { onMount } from 'svelte';
  import AppShell from '$lib/components/AppShell.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import AdminToolbar from '$lib/components/AdminToolbar.svelte';
  import AdminSection from '$lib/components/AdminSection.svelte';
  import AdminStatCard from '$lib/components/AdminStatCard.svelte';
  import AdminStatusList from '$lib/components/AdminStatusList.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import { currentUser } from '$lib/stores/user';
  import { fetchAdminMonitoringStatus, type AdminMonitoringStatus } from '$lib/api';
  import { getErrorMessage } from '$lib/errors';
  let loading = true; let error = ''; let data: AdminMonitoringStatus | null = null;
  const load = async () => { loading = true; error = ''; try { data = await fetchAdminMonitoringStatus(); } catch (err: unknown) { error = getErrorMessage(err, 'Failed to load monitoring status'); } finally { loading = false; } };
  const endpointRows = () => Object.entries(data?.endpoints ?? {}).map(([service, url]) => ({ service, url }));
  const columns = [{ key: 'service', label: 'Service' }, { key: 'url', label: 'URL' }];
  onMount(load);
</script>
<AppShell>{#if $currentUser?.role !== 'admin'}<p>Accès restreint</p>{:else}
<PageHeader title="Admin monitoring" subtitle="Observabilité runtime read-only" />
<AdminToolbar {loading} {error}><button type="button" on:click={load} disabled={loading}>Refresh</button></AdminToolbar>
<AdminSection title="Résumé monitoring"><div class="stats-grid"><AdminStatCard label="Global status" value={data?.status ?? 'unknown'} status={data?.status ?? 'warning'} />{#each [['Prometheus','prometheus'],['Grafana','grafana'],['Loki','loki'],['Alertmanager','alertmanager'],['Blackbox','blackbox'],['Node Exporter','node_exporter'],['cAdvisor','cadvisor']] as [label,key]}<AdminStatCard {label} value={data?.services?.[key] ?? 'unknown'} status={data?.services?.[key] ?? 'warning'} />{/each}</div></AdminSection>
<AdminSection title="Services"><AdminStatusList items={Object.entries(data?.services ?? {}).map(([label, status]) => ({ label, status }))} /></AdminSection>
<AdminSection title="Endpoints"><DataTable {columns} rows={endpointRows()} /></AdminSection>
<AdminSection title="Commandes opérateur"><ul><li><code>./scripts/prod-monitoring-check.sh</code></li><li><code>REQUIRE_MONITORING_RUNNING=1 ./scripts/prod-monitoring-check.sh</code></li><li><code>SKIP_MONITORING_CHECK=1 ./scripts/prod-go-no-go.sh</code></li><li><code>docker compose --env-file .env.production -f docker-compose.prod.yml -f docker-compose.monitoring.yml ps</code></li></ul></AdminSection>
<AdminSection title="Documentation"><p><code>docs/monitoring.md</code></p></AdminSection>{/if}
</AppShell>
<style>.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.75rem;}</style>
