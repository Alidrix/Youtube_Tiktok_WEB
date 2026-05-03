<div class="grid">{#each Array(6) as _, i}<article class="cell"><p>Signal {i+1}</p><strong>{['Rising','Breakout','Fresh','Opportunity','Watch','Hot'][i]}</strong></article>{/each}</div>
<style>
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}
.cell{padding:.9rem;border-radius:14px;border:1px solid var(--border);background:linear-gradient(160deg,color-mix(in srgb,var(--brand-violet) 10%, var(--surface)),var(--surface));}
.cell p{margin:0;color:var(--muted);font-size:.8rem}.cell strong{font-size:1rem}
@media(max-width:768px){.grid{grid-template-columns:1fr 1fr}}
</style>
