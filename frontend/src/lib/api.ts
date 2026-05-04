const BASE=import.meta.env.VITE_API_BASE||'http://localhost:4443/api/v1';
export const api=(p:string,init?:RequestInit)=>fetch(`${BASE}${p}`,init).then(r=>r.json());
export const fetchPlans=()=>api('/plans').catch(()=>[{name:'Free'},{name:'Pro'},{name:'Studio'}]);
export const fetchDailyRadar=()=>api('/radar/daily');
export const scanVideos=()=>api('/videos/scan',{method:'POST'});
