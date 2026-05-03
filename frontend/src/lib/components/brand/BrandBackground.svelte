<script lang="ts">
  export let intensity: 'soft' | 'medium' | 'strong' = 'medium';
</script>

<div class={`brand-bg ${intensity}`} aria-hidden="true">
  <div class="halo violet"></div><div class="halo cyan"></div><div class="halo gold"></div><div class="grid"></div><div class="ring"></div>
</div>

<style>
.brand-bg{position:fixed;inset:0;pointer-events:none;z-index:-1;overflow:hidden}
.halo{position:absolute;filter:blur(40px);opacity:.5;animation:drift 18s ease-in-out infinite alternate}
.violet{width:40vw;height:40vw;left:-10vw;top:-8vh;background:radial-gradient(circle,var(--brand-violet),transparent 70%)}
.cyan{width:36vw;height:36vw;right:-8vw;top:24vh;background:radial-gradient(circle,var(--brand-cyan),transparent 72%);animation-delay:3s}
.gold{width:30vw;height:30vw;left:45vw;bottom:-10vw;background:radial-gradient(circle,var(--brand-gold),transparent 74%);animation-delay:6s}
.grid{position:absolute;inset:0;background-image:linear-gradient(to right,rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(circle at 50% 20%, black, transparent 80%);opacity:.15}
.ring{position:absolute;inset:15% 20%;border:1px solid color-mix(in srgb,var(--brand-cyan) 40%, transparent);border-radius:999px;box-shadow:0 0 45px color-mix(in srgb,var(--brand-violet) 20%, transparent);opacity:.25;animation:pulse 11s linear infinite}
.soft{opacity:.55}.medium{opacity:.85}.strong{opacity:1}
@keyframes drift{to{transform:translate3d(1.5rem,-1rem,0) scale(1.08)}}
@keyframes pulse{50%{transform:scale(1.04);opacity:.32}}
@media (prefers-reduced-motion: reduce){.halo,.ring{animation:none}}
</style>
