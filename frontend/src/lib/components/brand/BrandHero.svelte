<script lang="ts">
  import RadarOrb from './RadarOrb.svelte';
  export let eyebrow=''; export let title=''; export let subtitle=''; export let primaryCta=''; export let primaryHref=''; export let secondaryCta=''; export let secondaryHref='';
</script>
<section class="hero"><div><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="subtitle">{subtitle}</p><div class="cta"><a class="primary" href={primaryHref}>{primaryCta}</a><a class="ghost" href={secondaryHref}>{secondaryCta}</a></div></div><RadarOrb /></section>
<style>
.hero{display:grid;grid-template-columns:1.2fr auto;gap:1.2rem;align-items:center;padding:2rem;border:1px solid var(--border);border-radius:24px;background:var(--surface-glass);backdrop-filter:blur(8px)}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:var(--brand-cyan);font-size:.75rem}.subtitle{color:var(--muted);max-width:62ch}
h1{font-size:clamp(2rem,5vw,3.3rem);letter-spacing:-.04em;background:var(--gradient-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.cta{display:flex;gap:.65rem;flex-wrap:wrap}.primary,.ghost{padding:.7rem 1rem;border-radius:12px;font-weight:700}.primary{background:var(--gradient-brand);color:#041019}.ghost{border:1px solid var(--border)}
@media(max-width:900px){.hero{grid-template-columns:1fr}.hero :global(.orb){margin-inline:auto}}
</style>
