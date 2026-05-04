import PageHero from '../components/ui/PageHero';

export default function Alerts() {
  return (
    <div>
      <PageHero title='Alerts' subtitle='Configure actionable notifications for your team.' />
      <section className='card'>
        <h3>Canaux actifs</h3>
        <ul>
          <li>Web notifications</li>
          <li>Email notifications</li>
          <li>Telegram notifications</li>
        </ul>
      </section>
    </div>
  );
}
