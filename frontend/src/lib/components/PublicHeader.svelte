<script lang="ts">
  import ThemeToggle from '$lib/components/ThemeToggle.svelte';
</script>

<header class="header">
  <a class="brand" href="/">The Trend Scope <span>Create Success</span></a>
  <nav>
    <a href="/">Produit</a>
    <a href="/pricing">Tarifs</a>
    <a href="/login">Connexion</a>
    <a class="cta" href="/register">Créer un compte</a>
    <ThemeToggle />
  </nav>
</header>

<style>
  .header { display:flex; justify-content:space-between; align-items:center; padding:1rem 1.25rem; border-bottom:1px solid var(--border); background:var(--surface); }
  .brand { font-weight:800; color:var(--text); }
  .brand span { display:block; font-size:.72rem; color:var(--muted); font-weight:600; }
  nav { display:flex; align-items:center; gap:.9rem; }
  nav a { color:var(--text); font-weight:600; }
  .cta { background:var(--primary); color:var(--surface); padding:.45rem .75rem; border-radius:10px; }
</style>
