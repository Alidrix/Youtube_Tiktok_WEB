<script lang="ts">
  import AppShell from '$lib/components/AppShell.svelte';
  import { requestDataExport, requestDeleteAccount } from '$lib/api';
  let showConfirm = false;
</script>
<AppShell>
  <h1>Données personnelles</h1>
  <button on:click={() => requestDataExport()}>Demander un export de mes données</button>
  <button class="danger" on:click={() => (showConfirm = true)}>Demander la suppression de mon compte</button>
  {#if showConfirm}
    <div class="modal"><p>Confirmer la demande de suppression ?</p><button class="danger" on:click={() => requestDeleteAccount()}>Confirmer</button><button on:click={() => (showConfirm = false)}>Annuler</button></div>
  {/if}
</AppShell>
<style>button{margin-right:.5rem;background:var(--primary);color:var(--surface);border:none;border-radius:10px;padding:.55rem .8rem}.danger{background:var(--youtube)}.modal{margin-top:1rem;background:var(--surface);border:1px solid var(--border);padding:1rem;border-radius:12px}</style>
