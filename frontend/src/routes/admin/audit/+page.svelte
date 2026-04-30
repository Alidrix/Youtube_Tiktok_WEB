<script lang="ts">
  import { onMount } from 'svelte';
  import AppShell from '$lib/components/AppShell.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import AdminToolbar from '$lib/components/AdminToolbar.svelte';
  import AdminSection from '$lib/components/AdminSection.svelte';
  import AdminStatCard from '$lib/components/AdminStatCard.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import { fetchAdminAuditLogs, type AdminAuditLog, type AdminAuditLogFilters } from '$lib/api';
  import { getErrorMessage } from '$lib/errors';
  import { currentUser } from '$lib/stores/user';

  let loading = true;
  let error = '';
  let logs: AdminAuditLog[] = [];

  const defaultFilters: AdminAuditLogFilters = { limit: 100, action: '', status: '', admin_username: '' };
  let filters: AdminAuditLogFilters = { ...defaultFilters };

  const load = async () => {
    loading = true;
    error = '';
    try {
      const payload: AdminAuditLogFilters = {
        limit: filters.limit || 100,
        action: filters.action?.trim() || undefined,
        status: filters.status?.trim() || undefined,
        admin_username: filters.admin_username?.trim() || undefined
      };
      const res = await fetchAdminAuditLogs(payload);
      logs = res.logs ?? [];
    } catch (err: unknown) {
      error = getErrorMessage(err, 'Failed to load audit logs');
    } finally {
      loading = false;
    }
  };

  const resetFilters = async () => {
    filters = { ...defaultFilters };
    await load();
  };

  $: totalDisplayed = logs.length;
  $: lastAction = logs[0]?.action ?? '—';
  $: failedCount = logs.filter((l) => l.status === 'failed').length;
  $: okCount = logs.filter((l) => ['ok', 'sent', 'logged'].includes(l.status)).length;

  const columns = [
    { key: 'created_at', label: 'Date', type: 'date' as const },
    { key: 'admin_username', label: 'Admin' },
    { key: 'action', label: 'Action', type: 'status' as const },
    { key: 'target', label: 'Target' },
    { key: 'status', label: 'Status', type: 'status' as const },
    { key: 'user_agent', label: 'User-Agent' }
  ];

  onMount(load);
</script>

<AppShell>
  {#if $currentUser?.role !== 'admin'}
    <p>Accès restreint</p>
  {:else}
    <PageHeader title="Admin Audit" subtitle="Dernières actions administrateur" />

    <AdminToolbar {loading} {error}>
      <button type="button" disabled={loading} on:click={load}>Refresh</button>
    </AdminToolbar>

    <AdminSection title="Audit summary">
      <div class="stats-grid">
        <AdminStatCard label="Total affiché" value={totalDisplayed} />
        <AdminStatCard label="Dernière action" value={lastAction} />
        <AdminStatCard label="Actions failed" value={failedCount} status={failedCount > 0 ? 'failed' : 'ok'} />
        <AdminStatCard label="Actions ok/sent/logged" value={okCount} status="ok" />
      </div>
    </AdminSection>

    <AdminSection title="Filtres audit">
      <form class="filters" on:submit|preventDefault={load}>
        <input type="text" placeholder="Action" bind:value={filters.action} />
        <input type="text" placeholder="Status" bind:value={filters.status} />
        <input type="text" placeholder="Admin username" bind:value={filters.admin_username} />
        <input type="number" min="1" max="500" placeholder="Limit" bind:value={filters.limit} />
        <button type="submit" disabled={loading}>Apply filters</button>
        <button type="button" disabled={loading} on:click={resetFilters}>Reset</button>
      </form>
    </AdminSection>

    <AdminSection title="Audit admin">
      {#if loading}
        <p>Chargement…</p>
      {:else if logs.length === 0}
        <p>Aucun log d’audit pour le moment.</p>
      {:else}
        <DataTable {columns} rows={logs} />
      {/if}
    </AdminSection>
  {/if}
</AppShell>

<style>
  .filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 0.75rem;
    align-items: center;
  }
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.75rem;
  }
</style>
