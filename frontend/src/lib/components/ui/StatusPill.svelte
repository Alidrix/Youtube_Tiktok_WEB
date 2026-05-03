<script lang="ts">export let status='neutral'; export let label=status; const t=(s:string)=>['ok','online','healthy','success'].includes(s)?'ok':['warning','degraded','unknown'].includes(s)?'warn':['error','offline','failed'].includes(s)?'err':'neutral';</script>
<span class={`pill ${t(status)}`}>{label}</span>
<style>.pill{padding:.2rem .55rem;border-radius:999px;border:1px solid var(--border);font-size:.75rem;font-weight:700}.ok{color:var(--success)}.warn{color:var(--warning)}.err{color:var(--danger)}.neutral{color:var(--muted-strong)}</style>
