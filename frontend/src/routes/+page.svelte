<script lang="ts">
  import PublicHeader from '$lib/components/PublicHeader.svelte'; import PublicFooter from '$lib/components/PublicFooter.svelte';
  import BrandBackground from '$lib/components/brand/BrandBackground.svelte'; import BrandHero from '$lib/components/brand/BrandHero.svelte'; import SignalGrid from '$lib/components/brand/SignalGrid.svelte';
</script>
<BrandBackground intensity="strong" />
<PublicHeader />
<main class="landing">
  <BrandHero eyebrow="Viral intelligence platform" title="Repère les tendances avant les autres. Crée avant saturation." subtitle="The Trend Scope transforme le bruit social en signaux actionnables pour créateurs, agences et équipes growth." primaryCta="Commencer gratuitement" primaryHref="/register" secondaryCta="Voir les offres" secondaryHref="/pricing" />
  <section class="bento"><article><h3>Detect</h3><p>Radar des accélérations, freshness, saturation et opportunités.</p></article><article><h3>Understand</h3><p>Score tendance, vues/h, régions et niches émergentes.</p></article><article><h3>Create</h3><p>Passe de l’insight au contenu pendant la fenêtre d’attention.</p></article><SignalGrid /></section>
</main>
<PublicFooter />
<style>
.landing{max-width:1150px;margin:0 auto;padding:1rem 1rem 2rem;display:grid;gap:1rem}.bento{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.bento article{padding:1rem;border:1px solid var(--border);border-radius:16px;background:var(--surface-glass);}
h3{margin:0 0 .4rem;letter-spacing:-.03em;}
p{margin:0;color:var(--muted);}
@media(max-width:900px){.bento{grid-template-columns:1fr;}
}
</style>
