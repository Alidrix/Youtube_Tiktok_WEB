<script lang="ts">
  export let tabs = ['Toutes plateformes', 'YouTube', 'TikTok preview', 'Instagram preview'];
  export let active = tabs[0];
</script>
<div class="tabs">{#each tabs as tab}<span class:active={tab===active}>{tab}</span>{/each}</div>
<style>.tabs{display:flex;gap:.5rem;flex-wrap:wrap}.tabs span{padding:.35rem .65rem;background:var(--surface-soft);border-radius:999px;color:var(--muted)}.tabs .active{background:var(--primary-soft);color:var(--text)}</style>
