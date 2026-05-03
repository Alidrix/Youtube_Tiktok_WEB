<script lang="ts">export let title='';export let subtitle='';</script><section><header><h2>{title}</h2>{#if subtitle}<p>{subtitle}</p>{/if}</header><slot/></section>
<style>section{display:grid;gap:.75rem}h2{margin:0}p{margin:.2rem 0 0;color:var(--muted)}</style>
