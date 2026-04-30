<script lang="ts">
  import StatusBadge from './StatusBadge.svelte';
  export let label = '';
  export let value: string | number = '0';
  export let hint = '';
  export let status = '';
</script>
<div class="card">
  <p>{label}</p><strong>{value}</strong>
  {#if hint}<small>{hint}</small>{/if}
  {#if status}<StatusBadge status={status} />{/if}
</div>
<style>
.card{border:1px solid var(--border);padding:.9rem;border-radius:12px;background:var(--bg)} p{margin:0;color:var(--muted)} strong{display:block;font-size:1.35rem;margin:.2rem 0}.card small{color:var(--muted)}
</style>
