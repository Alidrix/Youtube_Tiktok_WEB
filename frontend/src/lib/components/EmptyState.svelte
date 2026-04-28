<script lang="ts">
  export let title = 'Aucune donnée';
  export let message = 'Les workers préparent les prochains signaux.';
</script>

<div class="empty">
  <h3>{title}</h3>
  <p>{message}</p>
</div>

<style>
  .empty { border: 1px dashed var(--border); border-radius: var(--radius-card); padding: 2rem; text-align: center; background: var(--surface); }
  h3 { color: var(--text); margin-bottom: 0.5rem; }
  p { color: var(--muted); margin: 0; }
</style>
