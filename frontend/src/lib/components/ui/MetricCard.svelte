<script lang="ts">
  export let label = '';
  export let value: string | number = '';
  export let hint = '';
  export let status = 'neutral';

  const tone = (s: string) => {
    if (['ok', 'online', 'healthy', 'success'].includes(s)) return 'success';
    if (['warning', 'degraded', 'unknown'].includes(s)) return 'warning';
    if (['error', 'offline', 'failed'].includes(s)) return 'danger';
    return 'neutral';
  };
</script>

<article class={`card ${tone(status)}`}>
  <p>{label}</p>
  <strong>{value}</strong>
  {#if hint}
    <small>{hint}</small>
  {/if}
</article>

<style>
  .card {
    border: 1px solid var(--border);
    border-left: 4px solid var(--muted);
    padding: 0.9rem;
    border-radius: var(--radius-lg);
    background: var(--surface-soft);
  }
  .success { border-left-color: var(--success); }
  .warning { border-left-color: var(--warning); }
  .danger { border-left-color: var(--danger); }
  p { margin: 0; color: var(--muted); }
  strong { display: block; font-size: 1.35rem; }
  small { color: var(--muted); }
</style>
