<script lang="ts">
  import StatusBadge from './StatusBadge.svelte';
  type Column = { key: string; label: string; type?: 'text'|'status'|'date'|'url'|'number' };
  export let columns: Column[] = [];
  export let rows: Record<string, unknown>[] = [];
  export let emptyMessage = 'Aucune donnée disponible.';
  const fmt = (v: unknown, t='text') => { if (v==null||v==='') return '—'; if(t==='date') return new Date(String(v)).toLocaleString(); return String(v); };
</script>
{#if !rows.length}<p>{emptyMessage}</p>{:else}<div class="wrap"><table><thead><tr>{#each columns as c}<th>{c.label}</th>{/each}</tr></thead><tbody>{#each rows as r}<tr>{#each columns as c}<td>{#if c.type==='status'}<StatusBadge status={String(r[c.key] ?? 'pending')} />{:else if c.type==='url' && r[c.key]}<a href={String(r[c.key])} target="_blank" rel="noreferrer">{String(r[c.key])}</a>{:else}{fmt(r[c.key], c.type)}{/if}</td>{/each}</tr>{/each}</tbody></table></div>{/if}
<style>.wrap{overflow:auto}table{width:100%;border-collapse:collapse;min-width:700px}th,td{padding:.55rem;border-bottom:1px solid var(--border);text-align:left}th{color:var(--muted)}</style>
