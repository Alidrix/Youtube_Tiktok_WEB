<script lang="ts">
  import AppShell from '$lib/components/AppShell.svelte';
  import PageHeader from '$lib/components/PageHeader.svelte';
  import AdminToolbar from '$lib/components/AdminToolbar.svelte';
  import AdminSection from '$lib/components/AdminSection.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import { fetchAdminAuditLogs, type AdminAuditLog } from '$lib/api';
  let loading = true; let error = ''; let logs: AdminAuditLog[] = [];
  async function load() { loading = true; error = ''; try { const res = await fetchAdminAuditLogs(); logs = res.logs ?? []; } catch (e) { error = e instanceof Error ? e.message : 'Failed to load audit logs'; } finally { loading = false; } }
  load();
  const columns = [{ key: 'created_at', label: 'Date', type: 'date' as const },{ key: 'admin_username', label: 'Admin' },{ key: 'action', label: 'Action', type: 'status' as const },{ key: 'target', label: 'Target' },{ key: 'status', label: 'Status', type: 'status' as const }];
</script>
<AppShell>
  <PageHeader title="Admin Audit" subtitle="Dernières actions administrateur" />
  <AdminToolbar on:refresh={load} />
  <AdminSection title="Audit admin">
    {#if loading}<p>Chargement…</p>
    {:else if error}<p>{error}</p>
    {:else if logs.length === 0}<p>Aucun log d’audit pour le moment.</p>
    {:else}<DataTable {columns} rows={logs} /><p>Metadata disponible côté API, non affichée par défaut.</p>{/if}
  </AdminSection>
</AppShell>
