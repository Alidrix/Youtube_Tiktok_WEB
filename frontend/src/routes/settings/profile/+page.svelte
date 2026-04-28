<script lang="ts">import AppShell from '$lib/components/AppShell.svelte';</script>
<AppShell>
  <h1>Profil</h1>
  <form class="grid">
    <input placeholder="Nom affiché" />
    <input placeholder="Email" />
    <input placeholder="Pays" />
    <input placeholder="Fuseau horaire" />
    <input placeholder="Type de profil" />
    <input placeholder="Objectif principal" />
    <button type="button">Enregistrer</button>
  </form>
</AppShell>
<style>.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem}input{padding:.6rem;border-radius:10px;border:1px solid var(--border);background:var(--surface)}button{width:max-content;background:var(--primary);color:var(--surface);border:none;border-radius:10px;padding:.55rem .8rem}</style>
