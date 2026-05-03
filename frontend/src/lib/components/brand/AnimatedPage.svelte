<script lang="ts">import { fade } from 'svelte/transition';</script>
<div class="animated" in:fade={{duration:220}}><slot /></div>
<style>.animated{animation:enter .28s ease both}@keyframes enter{from{transform:translateY(8px);opacity:.8}}@media (prefers-reduced-motion: reduce){.animated{animation:none}}</style>
