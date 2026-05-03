<script lang="ts">export let lines=3;</script>{#each Array(lines) as _,i}<div class='line' style={`width:${100-(i*12)}%`}></div>{/each}
<style>.line{height:.9rem;margin:.45rem 0;border-radius:8px;background:linear-gradient(90deg,var(--surface-soft),var(--border),var(--surface-soft));background-size:200% 100%;animation:sh 1.2s linear infinite}@keyframes sh{to{background-position:-200% 0}}</style>
