import { createContext, useContext, useEffect, useState } from 'react';
const Ctx=createContext({theme:'dark',toggle:()=>{}});
export function ThemeProvider({children}:{children:React.ReactNode}){const [theme,setTheme]=useState(localStorage.getItem('theme')||'dark');useEffect(()=>{document.documentElement.dataset.theme=theme;localStorage.setItem('theme',theme)},[theme]);return <Ctx.Provider value={{theme,toggle:()=>setTheme(theme==='dark'?'light':'dark')}}>{children}</Ctx.Provider>}
export const useTheme=()=>useContext(Ctx);
