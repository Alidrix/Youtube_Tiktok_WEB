<script lang='ts'>export let title='';export let description=''; import SurfacePanel from '$lib/components/ui/SurfacePanel.svelte'; import SectionShell from '$lib/components/ui/SectionShell.svelte';</script>
<SurfacePanel elevated><SectionShell {title} subtitle={description}><div class='actions'><slot name='actions'/></div><div class='content'><slot/></div></SectionShell></SurfacePanel>
<style>.actions{display:flex;justify-content:flex-end}.content{display:grid;gap:.75rem}</style>
