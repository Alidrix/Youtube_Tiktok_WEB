<script lang="ts">
  import AppShell from '$lib/components/AppShell.svelte';
  import { fetchConsents, saveConsent } from '$lib/api';
  import { onMount } from 'svelte';
  let consentRows: any[] = [];
  let marketing = false;
  onMount(async()=>{ try { consentRows = await fetchConsents(); } catch {} });
  async function update() { await saveConsent({ consent_type: 'marketing', granted: marketing, version: 'v1' }); }
</script>
<AppShell>
  <h1>Confidentialité</h1>
  <p>Voir et modifier vos consentements.</p>
  <label><input type="checkbox" bind:checked={marketing} on:change={update} /> Opt-in marketing</label>
  <p><a href="/privacy">Politique de confidentialité</a> · <a href="/cookies">Cookies</a></p>
  <pre>{JSON.stringify(consentRows, null, 2)}</pre>
</AppShell>
