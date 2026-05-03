<script lang='ts'>export let title='';export let subtitle='';</script>
<header><h1>{title}</h1>{#if subtitle}<p>{subtitle}</p>{/if}</header>
<style>header{padding:.4rem 0 1rem}h1{margin:0 0 .3rem;font-size:clamp(1.35rem,2vw,1.8rem)}p{margin:0;color:var(--muted)}</style>
