<script lang="ts">
import {onMount} from 'svelte'; import AppShell from '$lib/components/AppShell.svelte'; import PageHeader from '$lib/components/PageHeader.svelte';
import AdminSection from '$lib/components/AdminSection.svelte'; import AdminStatCard from '$lib/components/AdminStatCard.svelte'; import DataTable from '$lib/components/DataTable.svelte'; import StatusBadge from '$lib/components/StatusBadge.svelte'; import {currentUser} from '$lib/stores/user';
import {fetchAdminSystem,fetchAdminEmailLogs,fetchAdminNotifications,fetchAdminExports,testAdminSmtp,testAdminTelegram,testAdminYoutube,testAdminStripe,fetchAdminSmoke} from '$lib/api';
let system:any={};let logs:any[]=[];let notifs:any={};let exportsData:any[]=[];let smoke:any=null;let smtpTo='';let chatId='';let loading:Record<string,boolean>={};let latest:Record<string,string>={};let history:{key:string;ok:boolean;message:string;date:string}[]=[];
const load=async()=>{system=await fetchAdminSystem();logs=(await fetchAdminEmailLogs()).logs||[];notifs=await fetchAdminNotifications();exportsData=(await fetchAdminExports()).exports||[]};
const record=(k:string,ok:boolean,m:string)=>{latest[k]=m;history=[{key:k,ok,message:m,date:new Date().toISOString()},...history].slice(0,20)};
const run=async(k:string)=>{loading[k]=true;try{const r= k==='smtp'?await testAdminSmtp({to:smtpTo}):k==='telegram'?await testAdminTelegram({chat_id:chatId||undefined}):k==='youtube'?await testAdminYoutube():await testAdminStripe();record(k,Boolean(r.ok ?? r.sent),r.message ?? r.reason ?? 'ok');}catch(e:any){record(k,false,e.message||'error')}finally{loading[k]=false}};
const runSmoke=async()=>{smoke=await fetchAdminSmoke()}; onMount(load);
</script>
<AppShell>{#if $currentUser?.role!=='admin'}<p>Accès restreint</p>{:else}<PageHeader title="Admin ops" subtitle="Cockpit d'exploitation"/><button on:click={load}>Refresh</button>
<AdminSection title="Tests d'intégration"><div class="g">
<AdminStatCard label="SMTP" value={system?.integrations?.smtp ?? 'not_configured'} status={system?.integrations?.smtp ?? 'not_configured'} hint={latest.smtp ?? ''}/><input bind:value={smtpTo} placeholder="Destinataire test"/><button disabled={loading.smtp} on:click={()=>run('smtp')}>Test SMTP</button>
<AdminStatCard label="Telegram" value={system?.integrations?.telegram ?? 'not_configured'} status={system?.integrations?.telegram ?? 'not_configured'} hint={latest.telegram ?? ''}/><input bind:value={chatId} placeholder="Chat ID optionnel"/><button disabled={loading.telegram} on:click={()=>run('telegram')}>Test Telegram</button>
<AdminStatCard label="YouTube API" value={system?.integrations?.youtube ?? 'not_configured'} status={system?.integrations?.youtube ?? 'not_configured'} hint={latest.youtube ?? ''}/><button disabled={loading.youtube} on:click={()=>run('youtube')}>testAdminYoutube</button>
<AdminStatCard label="Stripe" value={system?.integrations?.stripe ?? 'not_configured'} status={system?.integrations?.stripe ?? 'not_configured'} hint={latest.stripe ?? ''}/><button disabled={loading.stripe} on:click={()=>run('stripe')}>testAdminStripe</button>
</div></AdminSection>
<AdminSection title="Smoke interne"><button on:click={runSmoke}>Lancer smoke</button>{#if smoke}<p>ok: <StatusBadge status={smoke.ok?'ok':'error'} /></p>{#each Object.entries(smoke.checks||{}) as [k,v]}<p>{k}: <StatusBadge status={String(v)} /></p>{/each}{/if}</AdminSection>
<AdminSection title="Résultats des tests"><DataTable columns={[{key:'key',label:'Test'},{key:'ok',label:'OK'},{key:'message',label:'Message'},{key:'date',label:'Date',type:'date'}]} rows={history} /></AdminSection>
<AdminSection title="Logs email"><DataTable columns={[{key:'recipient',label:'Recipient'},{key:'subject',label:'Subject'},{key:'status',label:'Status',type:'status'},{key:'error',label:'Error'},{key:'created_at',label:'Date',type:'date'}]} rows={logs} /></AdminSection>
<AdminSection title="Notifications"><div class="g"><AdminStatCard label="Total" value={notifs?.total ?? 0}/><AdminStatCard label="Unread" value={notifs?.unread ?? 0}/></div></AdminSection>
<AdminSection title="Exports"><DataTable columns={[{key:'title',label:'Title'},{key:'format',label:'Format'},{key:'file_url',label:'File URL',type:'url'},{key:'created_at',label:'Created at',type:'date'}]} rows={exportsData} /></AdminSection>{/if}</AppShell>
<style>.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem}</style>
