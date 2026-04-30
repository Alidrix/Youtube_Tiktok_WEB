<script lang="ts">
  import StatusBadge from './StatusBadge.svelte';
  type LocalGoLiveItem = { key: string; label: string; status: 'ok'|'warning'|'error'|'manual'; blocking: boolean };
  export let items: LocalGoLiveItem[] = [];
  const note = (s:string)=>({ok:'prêt',warning:'à vérifier',error:'à corriger',manual:'contrôle manuel requis'}[s] ?? s);
  $: blocking = items.filter((i)=>i.blocking);
  $: optional = items.filter((i)=>!i.blocking);
</script>
<h3>Blocking checks</h3>{#each blocking as item}<p>{item.label} <StatusBadge status={item.status}/> <small>{note(item.status)}</small></p>{/each}
<h3>Optional checks</h3>{#each optional as item}<p>{item.label} <StatusBadge status={item.status}/> <small>{note(item.status)}</small></p>{/each}
