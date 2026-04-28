<script lang="ts">
  import { onMount } from 'svelte';
  import '$lib/styles/tokens.css';
  import { applyTheme, theme } from '$lib/stores/theme';

  onMount(() => {
    const unsubscribe = theme.subscribe((value) => applyTheme(value));
    return unsubscribe;
  });
</script>

<svelte:head>
  <style>
    :global(html) { background: var(--bg); color: var(--text); }
    :global(body) { margin: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
    :global(*) { box-sizing: border-box; }
    :global(a) { color: var(--text); text-decoration: none; }
  </style>
</svelte:head>

<slot />
