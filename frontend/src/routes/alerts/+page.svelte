<script lang="ts">
  import { onMount } from 'svelte';
  import AppShell from '$lib/components/AppShell.svelte';
  import { createAlert, deleteAlert, fetchAlerts } from '$lib/api';
  import { currentUser } from '$lib/stores/user';

  const channels = [
    { value: 'web', label: 'Notification web' },
    { value: 'email', label: 'Email' },
    { value: 'telegram', label: 'Telegram' }
  ];

  let alerts: any[] = [];
  let loading = false;
  let error = '';
  let name = '';
  let platform = 'youtube';
  let region = 'FR';
  let category = 'business';
  let keyword = '';
  let min_views_per_hour = 10000;
  let min_trend_score = 70;
  let channel = 'web';
  let telegram_chat_id = '';
  let enabled = true;

  async function load() {
    loading = true;
    try {
      const r = await fetchAlerts();
      alerts = r.alerts || [];
    } catch (e) {
      error = (e as Error).message;
    } finally {
      loading = false;
    }
  }

  async function create() {
    await createAlert({ name, platform, region, category, keyword, min_views_per_hour, min_trend_score, channel, telegram_chat_id: telegram_chat_id || undefined, enabled });
    await load();
  }

  async function remove(id: string) {
    await deleteAlert(id);
    await load();
  }

  onMount(load);
</script>

<AppShell><h1>Alertes</h1>
{#if $currentUser?.plan !== 'studio'}<p>Alertes réservées Studio. <a href="/subscription">Passer Studio</a></p>
{:else}
<input bind:value={name} placeholder="Nom de l’alerte"/>
<select bind:value={platform}><option>youtube</option><option>tiktok</option><option>instagram</option></select>
<input bind:value={region} placeholder="Région"/>
<input bind:value={category} placeholder="Catégorie"/>
<input bind:value={keyword} placeholder="Mot-clé"/>
<input type="number" bind:value={min_views_per_hour} placeholder="Seuil vues / heure"/>
<input type="number" bind:value={min_trend_score} placeholder="Seuil trend score"/>
<select bind:value={channel}>{#each channels as c}<option value={c.value}>{c.label}</option>{/each}</select>
{#if channel === 'telegram'}
  <input bind:value={telegram_chat_id} placeholder="Telegram Chat ID"/>
  <p>Le bot Telegram doit être configuré côté serveur. Le Chat ID peut correspondre à un utilisateur, un groupe ou un canal Telegram.</p>
{/if}
<label><input type="checkbox" bind:checked={enabled}/> Activée</label>
<button on:click={create}>Créer</button>
{#if loading}<p>Loading...</p>{/if}{#if error}<p>{error}</p>{/if}
{#each alerts as a}<p>{a.name} ({a.channel}) <button on:click={() => remove(a.id)}>Supprimer</button></p>{/each}
{/if}</AppShell>
