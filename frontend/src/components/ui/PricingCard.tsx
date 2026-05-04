import { motion, useReducedMotion } from 'framer-motion';
export default function PricingCard({name,price,featured=false}:{name:string;price:string;featured?:boolean}){const r=useReducedMotion(); return <motion.article whileHover={r?undefined:{y:-4}} className={`card ${featured?'featured':''}`}><h3>{name}</h3><p>{price}</p></motion.article>}
