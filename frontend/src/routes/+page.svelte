<script lang="ts">
  import PublicHeader from '$lib/components/PublicHeader.svelte';
  import PublicFooter from '$lib/components/PublicFooter.svelte';
</script>

<PublicHeader />
<main class="landing">
  <section class="hero">
    <p class="eyebrow">The Trend Scope</p>
    <h1>Repère les tendances avant les autres.<br />Crée du contenu au bon moment.</h1>
    <p>Détecte les vidéos qui accélèrent sur YouTube, puis TikTok et Instagram, avant qu’elles soient saturées.</p>
    <div class="actions">
      <a class="primary" href="/register">Commencer gratuitement</a>
      <a class="ghost" href="/pricing">Voir les offres</a>
      <a class="ghost" href="/login">Se connecter</a>
    </div>
  </section>

  <section class="grid">
    <article><h3>Comment ça marche</h3><ol><li>Les workers analysent les tendances</li><li>Le moteur calcule les scores</li><li>Tu consultes ton Radar du jour</li><li>Tu crées du contenu au bon moment</li></ol></article>
    <article><h3>Pour qui ?</h3><ul><li>Créateurs</li><li>Influenceurs</li><li>Agences social media</li><li>Marques</li><li>Growth marketers</li></ul></article>
    <article><h3>Preuve de valeur</h3><p>Radar du jour, score de tendance, vues/h, niches en hausse et upgrade simple vers Pro/Studio.</p></article>
  </section>

  <section class="cta"><h2>Prêt à publier au bon moment ?</h2><a class="primary" href="/pricing">Voir les plans</a></section>
</main>
<PublicFooter />

<style>
  .landing { max-width: 1100px; margin: 0 auto; padding: 0 1rem 2rem; }
  .hero { padding: 4rem 0 2rem; text-align: center; }
  .eyebrow { color: var(--youtube); font-weight: 700; }
  h1 { font-size: clamp(2rem, 4.5vw, 3.3rem); margin: .2rem 0 .6rem; }
  .hero p { color: var(--muted); }
  .actions { display:flex; gap:.7rem; justify-content:center; flex-wrap:wrap; margin-top:1rem; }
  .primary { background: var(--primary); color: var(--surface); padding:.7rem 1rem; border-radius:12px; font-weight:700; }
  .ghost { border:1px solid var(--border); background: var(--surface); padding:.7rem 1rem; border-radius:12px; }
  .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:1rem; }
  article { background: var(--surface); border:1px solid var(--border); border-radius:16px; padding:1rem; }
  .cta { margin-top:1rem; text-align:center; background:var(--surface-soft); border-radius:16px; padding:1.4rem; }
</style>
