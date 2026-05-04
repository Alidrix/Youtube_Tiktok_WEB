import { motion, useReducedMotion } from 'framer-motion';
import { Link } from 'react-router-dom';
export default function Landing(){const reduce=useReducedMotion();return <div><motion.section initial={reduce?false:{opacity:0,y:20}} animate={{opacity:1,y:0}}><h1>The Trend Scope</h1><p>Create Success</p><Link to='/radar'>Open Radar</Link></motion.section></div>}
