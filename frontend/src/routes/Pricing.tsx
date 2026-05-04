import PricingCard from '../components/ui/PricingCard';
export default function Pricing(){return <div><h1>Pricing</h1><div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:12}}><PricingCard name='Free' price='0€'/><PricingCard name='Pro' price='49€' featured/><PricingCard name='Studio' price='149€'/></div></div>}
