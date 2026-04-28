<script lang="ts">
  export let label = 'Passer Pro';
  export let href = '/pricing';
</script>
<a class="btn" {href}>{label}</a>
<style>.btn{display:inline-block;background:var(--primary);color:var(--surface);padding:.6rem .9rem;border-radius:10px;font-weight:700;}</style>
