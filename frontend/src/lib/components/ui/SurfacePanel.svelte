<script lang="ts">export let elevated=false; export let interactive=false;</script>
<section class:elevated class:interactive><slot/></section>
<style>
section{background:var(--surface-glass);border:1px solid var(--border);border-radius:var(--radius-xl);padding:1rem;backdrop-filter:blur(8px);box-shadow:var(--shadow-soft);transition:transform var(--transition-base),border-color var(--transition-base)}
.elevated{box-shadow:var(--shadow-card)} .interactive:hover{transform:translateY(-2px);border-color:var(--border-strong)}
</style>
