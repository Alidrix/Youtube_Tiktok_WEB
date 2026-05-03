<script lang='ts'>
import { onMount } from 'svelte'; import { get } from 'svelte/store'; import Sidebar from './Sidebar.svelte'; import Topbar from './Topbar.svelte'; import BrandBackground from '$lib/components/brand/BrandBackground.svelte'; import AnimatedPage from '$lib/components/brand/AnimatedPage.svelte';
import { token } from '$lib/stores/auth'; import { currentUser, loadCurrentUser } from '$lib/stores/user';
onMount(async()=>{ if(get(token)) await loadCurrentUser();});
</script>
<BrandBackground intensity="medium" />
<div class='shell'><Topbar />{#if $currentUser && $currentUser.email_verified===false}<div class='verify-banner'>Votre email n'est pas vérifié.</div>{/if}<div class='main'><Sidebar /><section class='content'><AnimatedPage><slot /></AnimatedPage></section></div></div>
<style>.shell{min-height:100vh;color:var(--text)}.verify-banner{background:color-mix(in srgb,var(--warning) 24%, transparent);padding:.65rem 1rem;border-bottom:1px solid color-mix(in srgb,var(--warning) 40%, var(--border));}.main{display:flex;min-height:calc(100vh - 66px)}.content{flex:1;padding:1.1rem;max-width:1500px}.content :global(> *){background:var(--surface-glass);backdrop-filter:blur(8px);border:1px solid var(--border);border-radius:20px;padding:1rem;box-shadow:var(--shadow-card)}@media(max-width:900px){.main{display:block}.content{padding:.8rem}}</style>
