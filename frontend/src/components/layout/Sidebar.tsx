import { NavLink } from 'react-router-dom';
const links=['/radar','/dashboard','/favorites','/watchlist','/alerts','/reports','/subscription','/settings','/admin'];
export default function Sidebar(){return <aside>{links.map(l=><NavLink key={l} to={l}>{l.replace('/','')||'home'}</NavLink>)}</aside>}
