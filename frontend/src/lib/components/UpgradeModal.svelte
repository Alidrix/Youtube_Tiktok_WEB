<script lang="ts">
  export let visible = false;
  export let message = '';
</script>

{#if visible}
  <div class="backdrop">
    <div class="modal">
      <h3>Limite gratuite atteinte</h3>
      <p>{message || 'Passez à Pro pour continuer à explorer le radar de tendances.'}</p>
      <a href="/pricing">Passer en Pro</a>
    </div>
  </div>
{/if}

<style>
  .backdrop { position: fixed; inset: 0; background: color-mix(in srgb, var(--text) 40%, transparent); display: grid; place-items: center; }
  .modal { background: var(--surface); border:1px solid var(--border); border-radius: 16px; padding: 1.2rem; width: min(460px, 92vw); }
  h3 { margin: 0; color: var(--text); }
  p { color: var(--muted); }
  a { display: inline-block; margin-top: .5rem; background: var(--primary); color: var(--surface); padding: .6rem .9rem; border-radius: 10px; }
</style>
