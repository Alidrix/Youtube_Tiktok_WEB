export const getToken=()=>localStorage.getItem('token');
export const setToken=(t:string)=>localStorage.setItem('token',t);
export const logout=()=>localStorage.removeItem('token');
