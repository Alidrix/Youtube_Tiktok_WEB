<script lang="ts">export let active=false;</script>
<div class:active class="wrap"><slot /></div>
<style>
.wrap{padding:1px;border-radius:16px;background:linear-gradient(120deg,transparent,transparent);transition:all var(--transition-base)}
.wrap.active,.wrap:hover{background:var(--gradient-brand);box-shadow:var(--glow-violet)}
.wrap :global(> *){border-radius:15px}
</style>
