<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchPlans } from '$lib/api';
  import PublicHeader from '$lib/components/PublicHeader.svelte';
  import PublicFooter from '$lib/components/PublicFooter.svelte';

  const fallbackPlans = [
    { tier: 'free', price_eur_monthly: 0, recommended: false },
    { tier: 'pro', price_eur_monthly: 10, recommended: true },
    { tier: 'studio', price_eur_monthly: 18, recommended: false }
  ];
  let plans: any[] = fallbackPlans;

  onMount(async () => {
    try { plans = await fetchPlans(); } catch { plans = fallbackPlans; }
  });

  const features: Record<string, string[]> = {
    free: ['3 tendances visibles / jour', 'YouTube disponible', 'TikTok / Instagram preview', 'Stats basiques', 'Pas d’exports', 'Pas d’alertes', 'Pas de rapports'],
    pro: ['Tendances illimitées', 'Filtres plateforme / pays / catégorie', 'Vues par heure', 'Score tendance', 'Favoris', 'Notes privées', 'Historique 7 jours'],
    studio: ['Historique 90 jours', 'Alertes personnalisées', 'Rapports hebdomadaires', 'Exports CSV/PDF', 'Watchlist avancée', 'Scores avancés', 'Détection signaux faibles', 'Comparaison cross-platform']
  };
</script>

<PublicHeader />
<main class="pricing">
  <h1>Tarifs The Trend Scope</h1>
  <p>Repère les tendances avant les autres et crée du contenu au bon moment.</p>
  <div class="cards">
    {#each plans as plan}
      <article class:popular={plan.tier === 'pro' || plan.recommended}>
        {#if plan.tier === 'pro' || plan.recommended}<span>Le plus populaire</span>{/if}
        <h2>{String(plan.tier).toUpperCase()}</h2>
        <p class="price">{plan.price_eur_monthly} € /mois</p>
        <ul>{#each features[String(plan.tier)] ?? [] as item}<li>{item}</li>{/each}</ul>
        <a href="/subscription">{plan.tier === 'free' ? 'Commencer gratuitement' : plan.tier === 'pro' ? 'Passer Pro' : 'Choisir Studio'}</a>
      </article>
    {/each}
  </div>
  <section class="faq"><h3>FAQ</h3><p><strong>Puis-je commencer gratuitement ?</strong> Oui, avec le plan Free.</p><p><strong>Puis-je annuler quand je veux ?</strong> Oui, depuis Stripe.</p><p><strong>Est-ce que TikTok et Instagram sont inclus ?</strong> Oui en mode preview.</p><p><strong>Comment sont calculées les tendances ?</strong> Via scoring serveur basé sur signaux de croissance.</p><p><strong>Est-ce que ma clé YouTube est nécessaire ?</strong> Non, The Trend Scope collecte, nettoie et score les tendances côté serveur.</p></section>
</main>
<PublicFooter />

<style>
  .pricing{max-width:1100px;margin:0 auto;padding:1rem}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin-top:1rem}
  article{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1rem;position:relative}
  article span{position:absolute;top:-10px;right:10px;background:var(--primary);color:var(--surface);padding:.2rem .5rem;border-radius:999px;font-size:.72rem}
  .popular{border-color:var(--primary)}
  .price{font-size:1.5rem;font-weight:800}
  a{display:inline-block;margin-top:.6rem;background:var(--primary);color:var(--surface);padding:.55rem .8rem;border-radius:10px}
  .faq{margin-top:1.2rem;background:var(--surface-soft);border-radius:14px;padding:1rem}
</style>
