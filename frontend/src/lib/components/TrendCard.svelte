<script lang="ts">
  import TrendScore from './TrendScore.svelte';
  export let trend: any;
  const score = Math.min(99, Math.max(55, Math.round((trend.views_per_hour || 0) / 350)));
</script>

<article class="card">
  <img src={trend.thumbnail_url || 'https://placehold.co/480x270?text=Trend'} alt={trend.title} />
  <div class="body">
    <p class="platform">YouTube</p>
    <h3>{trend.title}</h3>
    <p class="meta">{trend.category} • {trend.region || 'Global'}</p>
    <div class="stats">
      <TrendScore {score} />
      <span>{Math.round(trend.views_per_hour || 0).toLocaleString()} vues/h</span>
    </div>
  </div>
</article>

<style>
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
  img { width: 100%; aspect-ratio: 16/9; object-fit: cover; background: var(--surface-soft); }
  .body { padding: 0.9rem; }
  .platform { font-size: 0.78rem; color: var(--youtube); font-weight: 700; margin: 0 0 .4rem; }
  h3 { margin: 0; font-size: 1rem; color: var(--text); }
  .meta { color: var(--muted); font-size: .85rem; margin: .4rem 0 .5rem; }
  .stats { display: flex; justify-content: space-between; align-items:center; font-size: .82rem; color: var(--text); }
</style>
