import PageHero from '../components/ui/PageHero';

export default function AdminOps() {
  return (
    <div>
      <PageHero title='AdminOps' subtitle='Pilotage opérationnel compact pour le go-live.' />

      <section className='card'>
        <h3>Tests d'intégration</h3>
        <p>Suivi des checks backend/frontend et dépendances critiques.</p>
      </section>

      <section className='card'>
        <h3>Smoke interne</h3>
        <p>Validation des flux essentiels avant release.</p>
      </section>

      <section className='card'>
        <h3>Résultats des tests</h3>
        <p>Dernier statut: ONLINE. Aucun affichage brut de payload.</p>
      </section>

      <section className='card'>
        <h3>Logs email</h3>
        <p>Résumé des envois et erreurs opérationnelles.</p>
      </section>

      <section className='card'>
        <h3>Notifications</h3>
        <p>Canaux actifs: web, email, telegram.</p>
      </section>

      <section className='card'>
        <h3>Exports</h3>
        <p>Traçabilité des exports avec champs normalisés: error_message, file_url.</p>
      </section>
    </div>
  );
}
