<script lang="ts">
  import Sidebar from './Sidebar.svelte';
  import Topbar from './Topbar.svelte';
  export let isAdmin = false;
  export let plan = 'free';
</script>

<div class="shell">
  <Topbar {plan} />
  <div class="main">
    <Sidebar {isAdmin} />
    <section class="content"><slot /></section>
  </div>
</div>

<style>
  .shell { min-height:100vh; background:var(--bg); color:var(--text); }
  .main { display:flex; min-height:calc(100vh - 60px); }
  .content { flex:1; padding:1rem; }
</style>
