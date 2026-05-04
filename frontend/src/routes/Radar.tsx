import { motion, useReducedMotion } from 'framer-motion';
import MetricCard from '../components/ui/MetricCard';
export default function Radar(){const r=useReducedMotion();return <div><h1>Radar du jour</h1><div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:12}}><MetricCard label='Trends' value='24'/><MetricCard label='Views/h' value='1.2M'/><MetricCard label='Opportunities' value='8'/></div><motion.div whileHover={r?undefined:{scale:1.01}} className='card'>Premium trend grid</motion.div></div>}
