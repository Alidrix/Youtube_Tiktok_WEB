<script lang='ts'>
import MetricCard from '$lib/components/ui/MetricCard.svelte';
export let label=''; export let value: string|number='0'; export let hint=''; export let status='';
</script>
<MetricCard {label} {value} {hint} status={status || 'neutral'} />
