<script lang="ts">
  export let title = '';
  export let description = '';
</script>

<section class="admin-section">
  <header>
    <div>
      <h2>{title}</h2>
      {#if description}<p>{description}</p>{/if}
    </div>
    <div class="actions"><slot name="actions" /></div>
  </header>
  <div class="content"><slot /></div>
</section>

<style>
  .admin-section{margin-top:1rem;padding:1rem;border:1px solid var(--border);border-radius:14px;background:var(--surface)}
  header{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;margin-bottom:.8rem}
  h2{margin:0;font-size:1.05rem} p{margin:.2rem 0 0;color:var(--muted)} .content{display:grid;gap:.75rem}
</style>
