import { Navigate, Route, Routes } from 'react-router-dom';
import PublicLayout from './components/layout/PublicLayout';
import AppShell from './components/layout/AppShell';
import Landing from './routes/Landing';
import Pricing from './routes/Pricing';
import Login from './routes/Login';
import Register from './routes/Register';
import Radar from './routes/Radar';
import Dashboard from './routes/Dashboard';
import Favorites from './routes/Favorites';
import Watchlist from './routes/Watchlist';
import Alerts from './routes/Alerts';
import Reports from './routes/Reports';
import Subscription from './routes/Subscription';
import Settings from './routes/Settings';
import PrivacySettings from './routes/PrivacySettings';
import DataSettings from './routes/DataSettings';
import AdminOverview from './routes/AdminOverview';
import AdminOps from './routes/AdminOps';
import AdminSystem from './routes/AdminSystem';
import AdminBilling from './routes/AdminBilling';
import AdminBackups from './routes/AdminBackups';
import AdminIncidents from './routes/AdminIncidents';
import AdminMonitoring from './routes/AdminMonitoring';
import AdminGoLive from './routes/AdminGoLive';
import AdminAudit from './routes/AdminAudit';

export default function App() {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path='/' element={<Landing />} />
        <Route path='/pricing' element={<Pricing />} />
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
      </Route>
      <Route element={<AppShell />}>
        <Route path='/radar' element={<Radar />} />
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/favorites' element={<Favorites />} />
        <Route path='/watchlist' element={<Watchlist />} />
        <Route path='/alerts' element={<Alerts />} />
        <Route path='/reports' element={<Reports />} />
        <Route path='/subscription' element={<Subscription />} />
        <Route path='/settings' element={<Settings />} />
        <Route path='/settings/profile' element={<Settings />} />
        <Route path='/settings/privacy' element={<PrivacySettings />} />
        <Route path='/settings/data' element={<DataSettings />} />
        <Route path='/notifications' element={<Alerts />} />
        <Route path='/admin' element={<AdminOverview />} />
        <Route path='/admin/ops' element={<AdminOps />} />
        <Route path='/admin/system' element={<AdminSystem />} />
        <Route path='/admin/billing' element={<AdminBilling />} />
        <Route path='/admin/backups' element={<AdminBackups />} />
        <Route path='/admin/incidents' element={<AdminIncidents />} />
        <Route path='/admin/monitoring' element={<AdminMonitoring />} />
        <Route path='/admin/go-live' element={<AdminGoLive />} />
        <Route path='/admin/audit' element={<AdminAudit />} />
      </Route>
      <Route path='*' element={<Navigate to='/' replace />} />
    </Routes>
  );
}
