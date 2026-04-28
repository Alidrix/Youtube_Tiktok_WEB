<script lang="ts">
  export let label = '';
  export let value = '';
</script>
<article><p>{label}</p><strong>{value}</strong></article>
<style>article{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:.9rem;}p{margin:0;color:var(--muted);}strong{font-size:1.2rem;}</style>
