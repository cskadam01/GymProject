// pages/asf.jsx
export const Asf = () => {
  return (
    <>
      <h3>ÁLTALÁNOS SZERZŐDÉSI FELTÉTELEK</h3>
      <p>Hatályos: 2025. július 22-től</p>

      <h3>1. A feltételek tárgya és elfogadása</h3>
      <p>Jelen Általános Szerződési Feltételek, továbbiakban ÁSZF, a Szolgáltató online felületén elérhető regisztrációs és felhasználói fiók-kezelési funkciók használatára vonatkoznak. A regisztráció befejezésével a felhasználó kijelenti, hogy az ÁSZF-et elolvasta, megértette és elfogadta.</p>

      <h3>2. Regisztráció és felhasználói fiók</h3>
      <p>
        – A regisztráció önkéntes, de a szolgáltatás igénybevételéhez szükséges.<br/>
        – A felhasználó köteles valós és naprakész adatokat megadni.<br/>
        – Egy felhasználó egy fiókkal rendelkezhet; többes regisztráció tilos.<br/>
        – A jelszót a rendszer erősen titkosított formában, bcrypt hashing eljárással tárolja; sem a Szolgáltató, sem harmadik fél nem férhet hozzá olvasható formában.<br/>
        – A felhasználó felelős a jelszó biztonságos kezeléséért; elfelejtett jelszó esetén jelszó-visszaállítási folyamat áll rendelkezésre.
      </p>

      <h3>3. Kezelt személyes adatok</h3>
      <p>
        – Teljes név<br/>
        – Felhasználónév<br/>
        – E-mail cím<br/>
        – Életkor évszámban<br/>
        – Jelszó kriptográfiailag hash-elt formában
      </p>
      <p>Ezen adatok megadása nélkül a rendszer nem használható, mivel az azonosítás és a statisztikai kimutatások elkészítése technikailag lehetetlenné válna.</p>

      <h3>4. Adatkezelés célja és jogalapja</h3>
      <p>
        a Azonosítás és bejelentkezési jogosultság biztosítása – GDPR 6. cikk 1 b szerződés teljesítése<br/>
        b Operatív statisztikai kimutatások, anonim riportok készítése – GDPR 6. cikk 1 f jogos érdek<br/>
        c Jogosultság-kezelés, visszaélések kiszűrése – GDPR 6. cikk 1 f
      </p>

      <h3>5. Adattárolási határidők és törlés</h3>
      <p>
        – A felhasználó kérésére a személyes adatok bármikor törölhetők; törlési kérelem benyújtható e-mailben.<br/>
        – Kérelem hiányában az adatokat legfeljebb a regisztrációtól számított egy év elteltével a rendszer automatikusan törli.<br/>
        – Biztonsági mentésekben az adatok legfeljebb harminc napig maradhatnak fenn, majd véglegesen megsemmisülnek.
      </p>

      <h3>6. Adatbiztonság</h3>
      <p>
        – A rendszer TLS titkosítást használ a hálózati kommunikáció során.<br/>
        – Minden adatbázis-hozzáférést jogosultsági réteg véd; naplózzuk az adminisztratív műveleteket.<br/>
        – Az adatokhoz kizárólag a rendszergazdák férhetnek hozzá, akikre szigorú titoktartási kötelezettség vonatkozik.
      </p>

      <h3>7. Adattovábbítás és harmadik fél</h3>
      <p>
        – Harmadik fél részére személyes adat nem kerül átadásra marketing vagy reklámcélból.<br/>
        – Hatósági megkeresés esetén csak jogszabályi kötelezettség alapján, a minimum szükséges adatkör kerül kiadásra.
      </p>

      <h3>8. Felhasználói jogok</h3>
      <p>
        – Hozzáférés: bármikor kérheted, hogy tájékoztassunk, milyen adatot tárolunk rólad.<br/>
        – Helyesbítés: pontatlan adat javítása kérhető.<br/>
        – Törlés: az 5. pontban foglaltaktól függetlenül bármikor élhetsz törlési jogoddal.<br/>
        – Adathordozhatóság: kérheted adataid gépileg olvasható formátumban.<br/>
        – Korlátozás és tiltakozás: kérheted az adatkezelés ideiglenes felfüggesztését.<br/>
        Jogérvényesítéshez írj a Kapcsolattartó e-mail címére; panasszal élhetsz a Nemzeti Adatvédelmi és Információszabadság Hatóságnál, NAIH.
      </p>

      <h3>9. Szellemi tulajdon</h3>
      <p>A weboldalon, alkalmazásban található minden tartalom, forráskód, grafika és szöveg a Szolgáltató vagy licenc-adói tulajdonát képezi. A jogosulatlan másolás vagy terjesztés jogi következményeket von maga után.</p>

      <h3>10. Felelősségkorlátozás</h3>
      <p>A Szolgáltató nem felel a felhasználó által hibásan vagy hiányosan megadott adatokból eredő károkért, továbbá nem vállal felelősséget külső szolgáltatók, hosting, hálózat hibájából keletkező elérhetetlenségért.</p>

      <h3>11. Az ÁSZF módosítása</h3>
      <p>A Szolgáltató fenntartja a jogot jelen ÁSZF módosítására. A változásról a felhasználókat a belépést követően figyelmeztető üzenetben vagy e-mailben értesítjük. Az új feltételek elfogadása a szolgáltatás további használatával automatikusnak minősül.</p>

      <h3>12. Irányadó jog és jogvita</h3>
      <p>Jelen ÁSZF-re a magyar jog az irányadó. Felek a vitás kérdéseket elsősorban békés úton rendezik; ennek eredménytelensége esetén a Szolgáltató székhelye szerinti illetékes bíróság jár el.</p>

      <h3>13. Kapcsolat</h3>
      <p>
        Bármilyen kérdéssel vagy kéréssel fordulj hozzánk az alábbi elérhetőségen:<br/>
        – E-mail: [email@example.com]<br/>
        – Postacím: [---]
      </p>
    </>
  );
};
