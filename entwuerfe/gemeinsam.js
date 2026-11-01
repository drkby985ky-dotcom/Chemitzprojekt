/*
 * Was ist los in Chemnitz – gemeinsame Bausteine für alle drei Entwürfe
 * ---------------------------------------------------------------------
 * Hier stehen Dinge, die alle Entwürfe brauchen:
 *  1. Beispieldaten (erfunden – später kommen die echten Daten vom Freund)
 *  2. Merkliste (im Browser gespeichert, ohne Konto)
 *  3. "Lernen": welche Kategorien jemand oft anklickt
 *  4. Sortierung: Seltenes zuerst, dann nach persönlichen Interessen
 *  5. Detail-Fenster und Story-Bild zum Teilen
 */
(function () {
  'use strict';

  /* ---------- 1. Kategorien, Rhythmus, Beispieldaten ---------- */

  const CATEGORIES = [
    { id: 'musik',    name: 'Musik',           color: '#D6336C' },
    { id: 'markt',    name: 'Märkte',          color: '#E8590C' },
    { id: 'kultur',   name: 'Kultur',          color: '#8E44C9' },
    { id: 'fuehrung', name: 'Führungen',       color: '#127FA0' },
    { id: 'familie',  name: 'Familie',         color: '#2B9348' },
    { id: 'sport',    name: 'Sport',           color: '#2F6FEB' },
    { id: 'essen',    name: 'Essen & Trinken', color: '#B7791F' }
  ];

  // Je höher "weight", desto weiter oben steht die Veranstaltung.
  const RHYTHM = {
    einmalig:     { label: 'Einmalig',        weight: 300 },
    selten:       { label: 'Alle paar Jahre', weight: 260 },
    jaehrlich:    { label: 'Jährlich',        weight: 160 },
    regelmaessig: { label: 'Regelmäßig',      weight: 0 }
  };

  // day = Tage ab heute (0 = heute, 1 = morgen …). So bleiben die Beispiele immer aktuell.
  const RAW = [
    { id: 'e01', day: 0, time: '17:30', end: '21:00', cat: 'kultur', rhythm: 'selten', rhythmText: 'Alle 5 Jahre, zuletzt 2021',
      title: 'Lichterfahrt der historischen Straßenbahnen', place: 'Straßenbahnmuseum', district: 'Kappel', price: '6 €, Kinder frei',
      desc: 'Fünf restaurierte Straßenbahnwagen fahren beleuchtet in einer Kolonne durch das Depot und über das Museumsgleis. Mitfahrten in jedem Wagen möglich.' },
    { id: 'e02', day: 0, time: '10:00', end: '16:00', cat: 'markt', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr im Herbst',
      title: 'Apfelsortentag', place: 'Botanischer Garten', district: 'Altendorf', price: 'Eintritt frei',
      desc: 'Pomologen bestimmen mitgebrachte Äpfel aus dem eigenen Garten. Dazu frischer Most und über 80 alte Sorten zum Probieren.' },
    { id: 'e03', day: 0, time: '15:00', end: '16:00', cat: 'familie', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Kindertheater am Nachmittag', place: 'Fritz Theater', district: 'Zentrum', price: '8 €',
      desc: 'Kurze Stücke für Kinder ab 4 Jahren, gespielt vom Ensemble des Hauses.' },
    { id: 'e04', day: 0, time: '11:00', end: '12:00', cat: 'fuehrung', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Öffentliche Führung durch die Kunstsammlungen', place: 'Kunstsammlungen am Theaterplatz', district: 'Zentrum', price: 'Museumseintritt + 3 €',
      desc: 'Ein einstündiger Rundgang durch die Dauerausstellung mit wechselnden Schwerpunkten.' },

    { id: 'e05', day: 1, time: '21:00', end: '23:30', cat: 'musik', rhythm: 'einmalig', rhythmText: 'Einmalige Veranstaltung',
      title: 'Orgelnacht: Drei Orgeln, ein Abend', place: 'St. Jakobikirche', district: 'Zentrum', price: '12 €',
      desc: 'Zum Abschluss der Orgelsanierung spielen drei Organistinnen auf allen drei Instrumenten der Kirche – teils gleichzeitig. Kerzenlicht, freie Platzwahl.' },
    { id: 'e06', day: 1, time: '18:30', end: '19:30', cat: 'sport', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Lauftreff am Schloßteich', place: 'Schloßteich, Eingang Parkstraße', district: 'Schloßchemnitz', price: 'Kostenlos',
      desc: 'Lockere Runde um den Teich in zwei Tempogruppen. Keine Anmeldung nötig.' },
    { id: 'e07', day: 1, time: '08:00', end: '14:00', cat: 'markt', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Wochenmarkt', place: 'Markt', district: 'Zentrum', price: 'Eintritt frei',
      desc: 'Obst, Gemüse, Käse und Blumen von Händlern aus der Region.' },
    { id: 'e08', day: 1, time: '14:00', end: '18:00', cat: 'essen', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Backtag in der alten Mühle', place: 'Schlossmühle', district: 'Schloßchemnitz', price: 'Eintritt frei',
      desc: 'Der Holzbackofen wird angeheizt: Kürbisbrot, Zwiebelkuchen und Stollen-Vorkosten. Kinder dürfen selbst Teig kneten.' },

    { id: 'e09', day: 2, time: '20:00', end: '22:00', cat: 'musik', rhythm: 'einmalig', rhythmText: 'Einmaliges Konzert',
      title: 'Kellerkonzert unter dem Kaßberg', place: 'Kaßberg-Gänge', district: 'Kaßberg', price: '15 €, nur 60 Plätze',
      desc: 'Ein Streichquartett spielt in den historischen Bierkellern unter dem Kaßberg. Warme Kleidung empfohlen, der Keller hat 9 °C.' },
    { id: 'e10', day: 2, time: '16:00', end: '17:00', cat: 'fuehrung', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Hausführung im Schauspielhaus', place: 'Schauspielhaus', district: 'Kaßberg', price: '5 €',
      desc: 'Hinter die Kulissen: Bühnentechnik, Werkstätten und Garderoben.' },
    { id: 'e11', day: 2, time: '19:00', end: '20:30', cat: 'kultur', rhythm: 'regelmaessig', rhythmText: 'Jeden Monat',
      title: 'Lesung: Chemnitzer Stadtgeschichten', place: 'Stadtbibliothek im TIETZ', district: 'Zentrum', price: '4 €',
      desc: 'Autorinnen und Autoren aus der Region lesen kurze Texte über die Stadt.' },
    { id: 'e12', day: 2, time: '20:30', end: '22:00', cat: 'kultur', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Stummfilmnacht mit Live-Klavier', place: 'Weltecho', district: 'Zentrum', price: '9 €',
      desc: 'Zwei Stummfilmklassiker, live und improvisiert am Flügel begleitet.' },

    { id: 'e13', day: 3, time: '19:00', end: '20:30', cat: 'fuehrung', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Nachtführung im Versteinerten Wald', place: 'Museum für Naturkunde im TIETZ', district: 'Zentrum', price: '10 €, Anmeldung empfohlen',
      desc: 'Mit Taschenlampen durch die 290 Millionen Jahre alten Baumstämme im Atrium und die dunkle Ausstellung.' },
    { id: 'e14', day: 3, time: '20:00', end: '23:00', cat: 'musik', rhythm: 'regelmaessig', rhythmText: 'Jeden Monat',
      title: 'Jazz-Session', place: 'Weltecho', district: 'Zentrum', price: 'Eintritt frei, Hut geht rum',
      desc: 'Offene Bühne: Eine Hausband beginnt, danach darf jede und jeder mitspielen.' },
    { id: 'e15', day: 3, time: '20:00', end: '22:30', cat: 'essen', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Kneipenquiz', place: 'Spinnbau', district: 'Altchemnitz', price: '3 € pro Person',
      desc: 'Sechs Runden Allgemeinwissen in Teams bis sechs Personen.' },

    { id: 'e16', day: 4, time: '18:00', end: '22:00', cat: 'kultur', rhythm: 'einmalig', rhythmText: 'Einmalige Veranstaltung',
      title: 'Lichtprojektion am Karl-Marx-Kopf', place: 'Brückenstraße', district: 'Zentrum', price: 'Kostenlos',
      desc: 'Ein Künstlerkollektiv projiziert für einen Abend Bilder aus 70 Jahren Stadtgeschichte auf das Monument. Alle 20 Minuten beginnt der Durchlauf neu.' },
    { id: 'e17', day: 4, time: '19:00', end: '21:00', cat: 'sport', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Volleyball: Finale um den Stadtpokal', place: 'Sporthalle Brühl', district: 'Brühl', price: '5 €',
      desc: 'Die beiden besten Vereinsteams der Stadt spielen um den Pokal. Davor ein Spiel der Jugendmannschaften.' },
    { id: 'e18', day: 4, time: '08:00', end: '14:00', cat: 'markt', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Wochenmarkt', place: 'Markt', district: 'Zentrum', price: 'Eintritt frei',
      desc: 'Obst, Gemüse, Käse und Blumen von Händlern aus der Region.' },

    { id: 'e19', day: 5, time: '14:00', end: '19:00', cat: 'familie', rhythm: 'einmalig', rhythmText: 'Einmalig zur Eröffnung',
      title: 'Brückenfest: Die neue Fußgängerbrücke öffnet', place: 'Ufer der Chemnitz am Falkeplatz', district: 'Zentrum', price: 'Kostenlos',
      desc: 'Die neue Brücke über die Chemnitz wird mit Musik, Bastelzelt und Entenrennen auf dem Fluss eröffnet.' },
    { id: 'e20', day: 5, time: '20:00', end: '22:00', cat: 'familie', rhythm: 'regelmaessig', rhythmText: 'Jede Woche bei klarem Himmel',
      title: 'Öffentliche Himmelsbeobachtung', place: 'Sternwarte Rabenstein', district: 'Rabenstein', price: '4 €',
      desc: 'Blick durch das große Teleskop auf Mond, Planeten und Sternhaufen.' },
    { id: 'e21', day: 5, time: '15:00', end: '16:00', cat: 'fuehrung', rhythm: 'regelmaessig', rhythmText: 'Jede Woche',
      title: 'Kuratorenführung', place: 'Schloßbergmuseum', district: 'Schloßchemnitz', price: 'Museumseintritt',
      desc: 'Die Kuratorin zeigt ausgewählte Stücke der Stadtgeschichte.' },

    { id: 'e22', day: 6, time: '10:00', end: '16:00', cat: 'markt', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Hinterhof-Flohmarkt', place: 'Rund um den Lessingplatz', district: 'Sonnenberg', price: 'Eintritt frei',
      desc: 'Über 40 Höfe öffnen ihre Tore. Ein Plan mit allen Stationen liegt am Lessingplatz aus.' },
    { id: 'e23', day: 6, time: '12:00', end: '18:00', cat: 'musik', rhythm: 'jaehrlich', rhythmText: 'Einmal im Jahr',
      title: 'Plattenbörse', place: 'Atomino', district: 'Zentrum', price: '2 €',
      desc: 'Händler und Sammler verkaufen Vinyl, Kassetten und CDs. Plattenspieler zum Probehören stehen bereit.' },
    { id: 'e24', day: 6, time: '11:00', end: '15:00', cat: 'kultur', rhythm: 'selten', rhythmText: 'Nur alle 3 Jahre',
      title: 'Die große Dampfmaschine läuft', place: 'Industriemuseum', district: 'Altchemnitz', price: 'Museumseintritt',
      desc: 'Die historische Dampfmaschine wird nur alle paar Jahre angeheizt. Zuschauen, hören, riechen – ein seltenes Erlebnis.' },

    { id: 'e25', day: 7, time: '17:00', end: '20:00', cat: 'musik', rhythm: 'selten', rhythmText: 'Alle 4 Jahre',
      title: 'Chorfest der Partnerstädte', place: 'Stadthalle', district: 'Zentrum', price: '10 €',
      desc: 'Chöre aus acht Partnerstädten singen zuerst einzeln und am Ende gemeinsam ein eigens geschriebenes Stück.' }
  ];

  const TODAY = new Date();
  TODAY.setHours(0, 0, 0, 0);

  const EVENTS = RAW.map(e => {
    const d = new Date(TODAY);
    d.setDate(d.getDate() + e.day);
    return Object.assign({}, e, { date: d });
  });

  const catById = id => CATEGORIES.find(c => c.id === id);
  const isRare = ev => ev.rhythm !== 'regelmaessig';

  /* ---------- Speicher im Browser (mit Absicherung) ---------- */

  function load(key, fallback) {
    try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
    catch (_) { return fallback; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { /* privat-Modus: dann eben nur für diese Sitzung */ }
  }

  const listeners = [];
  const notify = () => listeners.forEach(fn => fn());

  /* ---------- 2. Merkliste ---------- */

  let favs = load('wilc-merkliste', []);
  const fav = {
    has: id => favs.includes(id),
    toggle(id) {
      const ev = EVENTS.find(e => e.id === id);
      if (favs.includes(id)) favs = favs.filter(x => x !== id);
      else { favs.push(id); if (ev) learn.track(ev.cat, 2); }
      save('wilc-merkliste', favs);
      notify();
    },
    list: () => EVENTS.filter(e => favs.includes(e.id)).sort((a, b) => a.day - b.day || a.time.localeCompare(b.time)),
    count: () => favs.length
  };

  /* ---------- 3. Lernen: Interessen pro Kategorie ---------- */

  let interest = load('wilc-interessen', {});
  const learn = {
    // Filter antippen = 1 Punkt, Veranstaltung öffnen = 1, merken = 2
    track(cat, points) {
      interest[cat] = (interest[cat] || 0) + (points || 1);
      save('wilc-interessen', interest);
    },
    affinity(cat) {
      const max = Math.max(0, ...Object.values(interest));
      return max ? (interest[cat] || 0) / max : 0;
    },
    top(n) {
      return Object.entries(interest).filter(([, v]) => v > 0)
        .sort((a, b) => b[1] - a[1]).slice(0, n || 3)
        .map(([id]) => catById(id)).filter(Boolean);
    },
    reset() { interest = {}; save('wilc-interessen', interest); notify(); }
  };

  /* ---------- 4. Sortierung ---------- */
  // Punkte = Seltenheit (sehr viel) + persönliches Interesse (bis 70) − Entfernung in Tagen (6 pro Tag)
  // Dadurch bleiben einmalige Termine immer über regelmäßigen, aber innerhalb
  // einer Gruppe rutschen die Lieblingskategorien nach oben.
  function score(ev) {
    return RHYTHM[ev.rhythm].weight + learn.affinity(ev.cat) * 70 - ev.day * 6;
  }
  function rank(list) {
    return list.slice().sort((a, b) => score(b) - score(a) || a.day - b.day || a.time.localeCompare(b.time));
  }
  const byTime = list => list.slice().sort((a, b) => a.day - b.day || a.time.localeCompare(b.time));

  /* ---------- Datumstexte ---------- */

  const WEEKDAYS = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  const fmt = {
    weekday: d => WEEKDAYS[d.getDay()],
    weekdayShort: d => WEEKDAYS[d.getDay()].slice(0, 2),
    dateLong: d => `${WEEKDAYS[d.getDay()]}, ${d.getDate()}. ${MONTHS[d.getMonth()]}`,
    dateShort: d => `${d.getDate()}. ${MONTHS[d.getMonth()].slice(0, 3)}`,
    monthShort: d => MONTHS[d.getMonth()].slice(0, 3),
    relDay(ev) {
      if (ev.day === 0) return 'Heute';
      if (ev.day === 1) return 'Morgen';
      return WEEKDAYS[ev.date.getDay()];
    },
    when: ev => `${fmt.relDay(ev)}, ${ev.time} Uhr`
  };

  /* ---------- Symbole (SVG) ---------- */

  const svg = (p, fill) => `<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="${fill ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
  const HEART = '<path d="M12 20.5s-7.5-4.6-9.3-9.4C1.4 7.6 3.6 4 7.2 4c2 0 3.6 1.1 4.8 2.8C13.2 5.1 14.8 4 16.8 4c3.6 0 5.8 3.6 4.5 7.1-1.8 4.8-9.3 9.4-9.3 9.4z"/>';
  const icon = {
    heart: svg(HEART, false),
    heartFill: svg(HEART, true),
    share: svg('<path d="M12 3v12"/><path d="M7.5 7.5 12 3l4.5 4.5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/>'),
    close: svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    calendar: svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'),
    clock: svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
    pin: svg('<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>'),
    ticket: svg('<path d="M4 7.5A1.5 1.5 0 0 1 5.5 6h13A1.5 1.5 0 0 1 20 7.5V10a2 2 0 0 0 0 4v2.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 16.5V14a2 2 0 0 0 0-4z"/>'),
    repeat: svg('<path d="M17 2.5 20.5 6 17 9.5"/><path d="M3.5 11.5V10a4 4 0 0 1 4-4h13"/><path d="M7 21.5 3.5 18 7 14.5"/><path d="M20.5 12.5V14a4 4 0 0 1-4 4h-13"/>'),
    sparkle: svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.5 2.5M15.2 15.2l2.5 2.5M6.3 17.7l2.5-2.5M15.2 8.8l2.5-2.5"/>'),
    chevron: svg('<path d="m9 6 6 6-6 6"/>'),
    chevronLeft: svg('<path d="m15 6-6 6 6 6"/>')
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const badge = ev => `<span class="w-badge w-badge-${ev.rhythm}">${RHYTHM[ev.rhythm].label}</span>`;
  const catDot = ev => `<span class="w-dot" style="--c:${catById(ev.cat).color}"></span>`;

  /* ---------- Gemeinsame Gestaltung für Fenster, Abzeichen, Herz ---------- */

  const CSS = `
  :root{--r-once:#C9184A;--r-rare:#7B3FC4;--r-year:#0B6E8A;--r-year-bg:rgba(11,110,138,.12);--scrim:rgba(0,0,0,.38)}
  @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--r-once:#E5385F;--r-rare:#9A62E0;--r-year:#5CC4E0;--r-year-bg:rgba(92,196,224,.16);--scrim:rgba(0,0,0,.6)}}
  :root[data-theme="dark"]{--r-once:#E5385F;--r-rare:#9A62E0;--r-year:#5CC4E0;--r-year-bg:rgba(92,196,224,.16);--scrim:rgba(0,0,0,.6)}

  [hidden]{display:none!important}
  .w-badge{display:inline-flex;align-items:center;font-size:11.5px;font-weight:650;letter-spacing:.02em;line-height:1;padding:5px 8px;border-radius:999px;white-space:nowrap}
  .w-badge-einmalig{background:var(--r-once);color:#fff}
  .w-badge-selten{background:var(--r-rare);color:#fff}
  .w-badge-jaehrlich{background:var(--r-year-bg);color:var(--r-year)}
  .w-badge-regelmaessig{background:var(--fill);color:var(--fg2)}
  .w-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--c);flex:none}

  .w-heart{appearance:none;border:0;background:transparent;color:var(--fg2);width:40px;height:40px;border-radius:50%;display:inline-grid;place-items:center;cursor:pointer;flex:none;transition:transform .15s}
  .w-heart[aria-pressed="true"]{color:var(--r-once)}
  .w-heart:active{transform:scale(.88)}
  .w-heart:focus-visible,.w-btn:focus-visible,.w-close:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

  .w-backdrop{position:fixed;inset:0;background:var(--scrim);z-index:100;display:flex;align-items:flex-end;justify-content:center;animation:w-fade .2s ease}
  .w-sheet{background:var(--card);color:var(--fg);width:100%;max-width:560px;max-height:92%;overflow:auto;border-radius:20px 20px 0 0;
    padding:10px max(20px, env(safe-area-inset-right,0px)) calc(24px + env(safe-area-inset-bottom,0px)) max(20px, env(safe-area-inset-left,0px));
    animation:w-up .28s cubic-bezier(.2,.8,.2,1);box-shadow:0 -8px 40px rgba(0,0,0,.18)}
  @media (min-width:700px){.w-backdrop{align-items:center}.w-sheet{border-radius:20px;padding-bottom:24px}}
  .w-grab{width:36px;height:5px;border-radius:3px;background:var(--fill);margin:0 auto 10px}
  .w-sheet-top{display:flex;justify-content:space-between;align-items:center;gap:8px}
  .w-sheet-top .w-meta{display:flex;align-items:center;gap:8px;color:var(--fg2);font-size:13px;font-weight:600}
  .w-close{appearance:none;border:0;background:var(--fill);color:var(--fg2);width:32px;height:32px;border-radius:50%;display:grid;place-items:center;cursor:pointer}
  .w-close svg{width:16px;height:16px}
  .w-sheet h2{font-size:26px;line-height:1.15;letter-spacing:-.02em;margin:14px 0 6px;text-wrap:balance}
  .w-facts{list-style:none;margin:16px 0;padding:0;display:grid;gap:12px}
  .w-facts li{display:flex;gap:12px;align-items:flex-start;font-size:15px;line-height:1.35}
  .w-facts svg{color:var(--fg2);flex:none;margin-top:-1px}
  .w-facts small{display:block;color:var(--fg2);font-size:13px}
  .w-desc{font-size:15.5px;line-height:1.5;margin:0 0 20px;max-width:60ch}
  .w-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .w-btn{appearance:none;border:0;border-radius:14px;padding:14px 12px;font:inherit;font-size:15.5px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;background:var(--fill);color:var(--fg)}
  .w-btn.primary{background:var(--accent);color:#fff}
  .w-btn[aria-pressed="true"]{color:var(--r-once)}
  .w-note{font-size:12px;color:var(--fg2);text-align:center;margin:16px 0 0}

  .w-share .w-sheet{max-width:460px;text-align:center}
  .w-share img{width:min(62vw,250px);aspect-ratio:9/16;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.25);display:block;margin:6px auto 16px;max-width:100%}
  .w-share p{font-size:14px;line-height:1.45;color:var(--fg2);margin:0 auto 16px;max-width:36ch}
  .w-share .w-actions{grid-template-columns:1fr}

  .w-favlist{list-style:none;margin:12px 0 0;padding:0}
  .w-favlist li{display:flex;align-items:center;gap:12px;padding:12px 0;border-top:1px solid var(--sep)}
  .w-favlist li:first-child{border-top:0}
  .w-favlist button.w-open{all:unset;cursor:pointer;flex:1;min-width:0}
  .w-favlist b{display:block;font-size:15.5px;font-weight:600}
  .w-favlist span.s{display:block;font-size:13px;color:var(--fg2);margin-top:2px}
  .w-empty{color:var(--fg2);font-size:15px;line-height:1.5;padding:18px 0;text-align:center}

  @keyframes w-up{from{transform:translateY(40px);opacity:.4}to{transform:none;opacity:1}}
  @keyframes w-fade{from{opacity:0}to{opacity:1}}
  @media (prefers-reduced-motion:reduce){.w-backdrop,.w-sheet{animation:none}}
  `;
  const style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  /* ---------- 5a. Fenster (Bottom Sheet) ---------- */

  function openSheet(html, cls) {
    const back = document.createElement('div');
    back.className = 'w-backdrop ' + (cls || '');
    back.innerHTML = `<div class="w-sheet" role="dialog" aria-modal="true"><div class="w-grab"></div>${html}</div>`;
    const close = () => { back.remove(); document.removeEventListener('keydown', onKey); document.body.style.overflow = ''; };
    const onKey = e => { if (e.key === 'Escape') close(); };
    back.addEventListener('click', e => { if (e.target === back || e.target.closest('[data-close]')) close(); });
    document.addEventListener('keydown', onKey);
    document.body.appendChild(back);
    document.body.style.overflow = 'hidden';
    const first = back.querySelector('[data-close]');
    if (first) first.focus({ preventScroll: true });
    return { el: back, close };
  }

  function openDetail(ev) {
    learn.track(ev.cat, 1);
    const cat = catById(ev.cat);
    const render = () => `
      <div class="w-sheet-top">
        <div class="w-meta">${catDot(ev)}${esc(cat.name)} ${badge(ev)}</div>
        <button class="w-close" data-close aria-label="Schließen">${icon.close}</button>
      </div>
      <h2>${esc(ev.title)}</h2>
      <ul class="w-facts">
        <li>${icon.calendar}<span>${fmt.dateLong(ev.date)}<small>${fmt.relDay(ev)}</small></span></li>
        <li>${icon.clock}<span>${ev.time} – ${ev.end} Uhr</span></li>
        <li>${icon.pin}<span>${esc(ev.place)}<small>${esc(ev.district)}</small></span></li>
        <li>${icon.ticket}<span>${esc(ev.price)}</span></li>
        <li>${icon.repeat}<span>${esc(ev.rhythmText)}</span></li>
      </ul>
      <p class="w-desc">${esc(ev.desc)}</p>
      <div class="w-actions">
        <button class="w-btn" data-fav aria-pressed="${fav.has(ev.id)}">${fav.has(ev.id) ? icon.heartFill + 'Gemerkt' : icon.heart + 'Merken'}</button>
        <button class="w-btn primary" data-share>${icon.share}Als Story teilen</button>
      </div>
      <p class="w-note">Beispielveranstaltung – erfundene Daten für den Entwurf</p>`;
    const s = openSheet(render());
    const sheet = s.el.querySelector('.w-sheet');
    sheet.addEventListener('click', e => {
      if (e.target.closest('[data-fav]')) {
        fav.toggle(ev.id);
        const b = sheet.querySelector('[data-fav]');
        b.setAttribute('aria-pressed', fav.has(ev.id));
        b.innerHTML = fav.has(ev.id) ? icon.heartFill + 'Gemerkt' : icon.heart + 'Merken';
      }
      if (e.target.closest('[data-share]')) { s.close(); openShare(ev); }
    });
    notify();
  }

  function openFavorites(title) {
    const render = () => {
      const list = fav.list();
      return `
      <div class="w-sheet-top"><strong style="font-size:20px">${esc(title || 'Merkliste')}</strong>
        <button class="w-close" data-close aria-label="Schließen">${icon.close}</button></div>
      ${list.length ? `<ul class="w-favlist">${list.map(ev => `
        <li>${catDot(ev)}<button class="w-open" data-id="${ev.id}"><b>${esc(ev.title)}</b><span class="s">${fmt.when(ev)} · ${esc(ev.place)}</span></button>
        <button class="w-heart" data-fav="${ev.id}" aria-pressed="true" aria-label="Von Merkliste entfernen">${icon.heartFill}</button></li>`).join('')}</ul>`
        : `<p class="w-empty">Noch nichts gemerkt.<br>Tippe bei einer Veranstaltung auf das Herz.</p>`}`;
    };
    const s = openSheet(render());
    const sheet = s.el.querySelector('.w-sheet');
    sheet.addEventListener('click', e => {
      const f = e.target.closest('[data-fav]');
      if (f) { fav.toggle(f.dataset.fav); sheet.innerHTML = '<div class="w-grab"></div>' + render(); return; }
      const o = e.target.closest('[data-id]');
      if (o) { s.close(); openDetail(EVENTS.find(x => x.id === o.dataset.id)); }
    });
  }

  /* ---------- 5b. Story-Bild (1080 × 1920) ---------- */

  function shade(hex, amount) {
    const n = parseInt(hex.slice(1), 16);
    const mix = c => Math.round(c * (1 - amount));
    return `rgb(${mix(n >> 16)},${mix((n >> 8) & 255)},${mix(n & 255)})`;
  }

  function wrapLines(ctx, text, maxWidth) {
    const words = text.split(' ');
    const lines = [];
    let line = '';
    words.forEach(w => {
      const test = line ? line + ' ' + w : w;
      if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = w; }
      else line = test;
    });
    if (line) lines.push(line);
    return lines;
  }

  function drawStory(ev) {
    const W = 1080, H = 1920, PAD = 96;
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    const x = c.getContext('2d');
    const cat = catById(ev.cat);
    const F = '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif';

    const g = x.createLinearGradient(0, 0, W * 0.4, H);
    g.addColorStop(0, cat.color);
    g.addColorStop(1, shade(cat.color, 0.62));
    x.fillStyle = g; x.fillRect(0, 0, W, H);

    // ruhige Kreise als Hintergrund
    x.fillStyle = 'rgba(255,255,255,0.07)';
    x.beginPath(); x.arc(W - 40, 420, 430, 0, Math.PI * 2); x.fill();
    x.beginPath(); x.arc(80, H - 260, 260, 0, Math.PI * 2); x.fill();

    // Kopfzeile (Instagram lässt oben ca. 250 px frei)
    x.fillStyle = 'rgba(255,255,255,0.85)';
    x.font = `700 38px ${F}`;
    if ('letterSpacing' in x) x.letterSpacing = '6px';
    x.fillText('WAS IST LOS IN CHEMNITZ', PAD, 300);
    if ('letterSpacing' in x) x.letterSpacing = '0px';

    // Titel – Schriftgröße passt sich an, max. 5 Zeilen
    let size = 116, lines;
    do {
      x.font = `800 ${size}px ${F}`;
      lines = wrapLines(x, ev.title, W - PAD * 2);
      size -= 6;
    } while (lines.length > 5 && size > 60);
    size += 6;
    const lh = size * 1.06;
    const dateBlock = 250;
    const titleH = lines.length * lh;
    let y = Math.max(720, (H - titleH - dateBlock) / 2 + 40);

    // Abzeichen
    const label = `${RHYTHM[ev.rhythm].label.toUpperCase()}  ·  ${cat.name.toUpperCase()}`;
    x.font = `700 34px ${F}`;
    const bw = x.measureText(label).width + 56;
    x.fillStyle = ev.rhythm === 'regelmaessig' ? 'rgba(255,255,255,0.22)' : '#ffffff';
    x.beginPath();
    if (x.roundRect) x.roundRect(PAD, y - size - 120, bw, 72, 36); else x.rect(PAD, y - size - 120, bw, 72);
    x.fill();
    x.fillStyle = ev.rhythm === 'regelmaessig' ? '#ffffff' : shade(cat.color, 0.35);
    x.fillText(label, PAD + 28, y - size - 72);

    // Titel
    x.fillStyle = '#ffffff';
    x.font = `800 ${size}px ${F}`;
    lines.forEach((l, i) => x.fillText(l, PAD, y + i * lh));
    y += titleH + 60;

    // Datum, Uhrzeit, Ort
    x.fillStyle = 'rgba(255,255,255,0.35)';
    x.fillRect(PAD, y - 10, 120, 6);
    x.fillStyle = '#ffffff';
    x.font = `700 56px ${F}`;
    x.fillText(fmt.dateLong(ev.date), PAD, y + 80);
    x.font = `500 46px ${F}`;
    x.fillStyle = 'rgba(255,255,255,0.88)';
    x.fillText(`${ev.time} – ${ev.end} Uhr`, PAD, y + 150);
    wrapLines(x, `${ev.place}, ${ev.district}`, W - PAD * 2).slice(0, 2)
      .forEach((l, i) => x.fillText(l, PAD, y + 216 + i * 58));

    // Fußzeile (unten ca. 340 px frei lassen für Instagram-Bedienelemente)
    x.font = `600 34px ${F}`;
    x.fillStyle = 'rgba(255,255,255,0.7)';
    x.fillText('Gefunden auf „Was ist los in Chemnitz“', PAD, H - 380);
    return c;
  }

  function canvasToFile(canvas, name) {
    const url = canvas.toDataURL('image/png');
    const bin = atob(url.split(',')[1]);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    let file = null;
    try { file = new File([arr], name, { type: 'image/png' }); } catch (_) { /* sehr alte Browser */ }
    return { url, file };
  }

  function openShare(ev) {
    const canvas = drawStory(ev);
    const slug = ev.title.toLowerCase().replace(/[^a-z0-9äöüß]+/g, '-').replace(/^-|-$/g, '');
    const { url, file } = canvasToFile(canvas, `chemnitz-${slug}.png`);
    const canShare = !!(file && navigator.canShare && navigator.canShare({ files: [file] }));
    const s = openSheet(`
      <div class="w-sheet-top"><strong style="font-size:20px">Story-Bild</strong>
        <button class="w-close" data-close aria-label="Schließen">${icon.close}</button></div>
      <img src="${url}" alt="Story-Bild: ${esc(ev.title)}, ${fmt.dateLong(ev.date)}, ${esc(ev.place)}">
      <p data-hint>${canShare
        ? 'Tippe auf „Teilen…“ und wähle Instagram, um das Bild als Story zu posten.'
        : 'Auf dem iPhone: Bild gedrückt halten, dann „Teilen…“ oder „Zu Fotos hinzufügen“ wählen. Am Computer: Rechtsklick und „Bild speichern“.'}</p>
      <div class="w-actions">
        ${canShare ? `<button class="w-btn primary" data-go>${icon.share}Teilen…</button>` : ''}
        <button class="w-btn" data-close>Fertig</button>
      </div>`, 'w-share');
    const go = s.el.querySelector('[data-go]');
    if (go) go.addEventListener('click', () => {
      navigator.share({ files: [file], title: ev.title }).catch(err => {
        if (err && err.name === 'AbortError') return;
        s.el.querySelector('[data-hint]').textContent = 'Teilen ist hier nicht möglich. Halte das Bild gedrückt und wähle „Teilen…“.';
        go.remove();
      });
    });
  }

  /* ---------- Nach außen sichtbar ---------- */

  window.WILC = {
    CATEGORIES, RHYTHM, EVENTS, TODAY,
    catById, isRare, rank, byTime, fav, learn, fmt, icon, esc, badge, catDot,
    openDetail, openShare, openFavorites,
    onChange: fn => listeners.push(fn),
    notify
  };
})();
