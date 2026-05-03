<script lang="ts">
  export let status = 'neutral';
  export let label = status;

  const tone = (s: string) => {
    if (['ok', 'online', 'healthy', 'success'].includes(s)) return 'ok';
    if (['warning', 'degraded', 'unknown'].includes(s)) return 'warn';
    if (['error', 'offline', 'failed'].includes(s)) return 'err';
    return 'neutral';
  };
</script>

<span class={`pill ${tone(status)}`}>{label}</span>

<style>
  .pill { padding: .2rem .55rem; border-radius: 999px; border: 1px solid var(--border); font-size: .75rem; font-weight: 700; }
  .ok { color: var(--success); }
  .warn { color: var(--warning); }
  .err { color: var(--danger); }
  .neutral { color: var(--muted-strong); }
</style>
