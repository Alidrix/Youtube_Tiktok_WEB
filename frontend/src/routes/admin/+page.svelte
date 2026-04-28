<script lang="ts">import AppShell from '$lib/components/AppShell.svelte'; const isAdmin=false;</script>
<AppShell {isAdmin}>{#if isAdmin}<h1>Dashboard admin</h1><p>Utilisateurs, abonnements, sources, jobs, quotas et santé système.</p>{:else}<h1>Accès restreint</h1><p>L’espace admin est réservé aux administrateurs.</p>{/if}</AppShell>
