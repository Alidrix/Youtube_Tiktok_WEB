import { useTheme } from '../../lib/theme';
export function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>){return <button className='btn' {...props}/>}
export function ThemeToggle(){const {theme,toggle}=useTheme(); return <button className='btn' onClick={toggle}>{theme}</button>}
