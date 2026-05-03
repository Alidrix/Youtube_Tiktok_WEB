<script lang="ts">
  export let loading = false;
  export let error = '';
  export let refreshLabel = 'Refresh';
</script>

<div class="toolbar">
  <slot>
    <button disabled={loading} class="refresh-btn" type="button">{refreshLabel}</button>
  </slot>
  <div class="meta" aria-live="polite">
    {#if loading}
      <span>Chargement…</span>
    {/if}
    {#if error}
      <span class="error">{error}</span>
    {/if}
  </div>
</div>

<style>
  .toolbar { display: flex; flex-wrap: wrap; gap: .75rem; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
  .meta { display: flex; gap: .75rem; color: var(--muted); }
  .refresh-btn, :global(.toolbar button) { border: 1px solid var(--border); background: var(--surface); color: var(--text); border-radius: 10px; padding: .55rem .9rem; font-weight: 600; transition: all var(--transition-fast); }
  :global(.toolbar button:hover) { border-color: var(--border-strong); transform: translateY(-1px); }
  .error { color: var(--danger); font-weight: 600; }
</style>
