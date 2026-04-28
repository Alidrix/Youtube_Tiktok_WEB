<script lang="ts">
  export let plan = 'free';
</script>
<span class="badge">Plan {plan.toUpperCase()}</span>
<style>
  .badge { border:1px solid var(--border); background:var(--surface-soft); padding:.35rem .6rem; border-radius:999px; font-weight:700; font-size:.75rem; }
</style>
