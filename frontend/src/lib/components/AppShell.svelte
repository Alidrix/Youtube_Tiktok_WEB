<script lang='ts'>
import { onMount } from 'svelte'; import { get } from 'svelte/store'; import Sidebar from './Sidebar.svelte'; import Topbar from './Topbar.svelte'; import { token } from '$lib/stores/auth'; import { currentUser, loadCurrentUser } from '$lib/stores/user';
onMount(async()=>{ if(get(token)) await loadCurrentUser();});
</script>
<div class='shell'><Topbar />{#if $currentUser && $currentUser.email_verified===false}<div class='verify-banner'>Votre email n'est pas vérifié. Vérifiez votre boîte mail pour activer pleinement le compte.</div>{/if}<div class='main'><Sidebar /><section class='content'><slot /></section></div></div>
<style>.shell{min-height:100vh;background:var(--bg);color:var(--text)}.verify-banner{background:color-mix(in srgb,var(--warning) 20%, transparent);color:var(--text);padding:.65rem 1rem;border-bottom:1px solid color-mix(in srgb,var(--warning) 40%, var(--border));}.main{display:flex;min-height:calc(100vh - 60px)}.content{flex:1;padding:1rem 1.2rem;max-width:1400px}@media(max-width:900px){.main{display:block}}</style>
