1. Sovelluksessa käyttäjät pystyvät etsimään peliseuraa sulkapalloon. Ilmoituksessa lukee missä ja milloin pelivuoro on sekä tarvittava pelaajien määrä.
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. -Käyttäjä pystyy lisäämään ilmoituksia ja muokkaamaan ja poistamaan niitä.
3. Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
4. Käyttäjä pystyy etsimään ilmoituksia hakusanalla.
5. Käyttäjäsivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan ilmoituksista.
6. Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. Kumpula Unisport, keskitason pelaaja).
7. Käyttäjä pystyy lähettää viestin pelivuoron ilmoitussivulle. Ilmoituksessa näytetään, mitä viestejä käyttäjät ovat lähettäneet.

Pääasiallinen tietokohde on ilmoitus ja toissijainen tietokohde on viestit ilmoituksissa.



Näin käyttäjä asentaa sovelluksen:

# 1) Kloonaa repo ja siirry hakemistoon
git clone <repo-url>
cd <kansio>

# 2) Luo ja aktivoi virtuaaliympäristö
python3 -m venv venv
source venv/bin/activate     # Windows PowerShell:  .\venv\Scripts\Activate.ps1

# 3) Asenna riippuvuudet
pip install flask

# 4) Luo tietokantataulut
# Vaihtoehto A (suositeltu): Flask-komento lukee schema.sql -tiedoston
export FLASK_APP=app.py      # Windows PS:  $env:FLASK_APP = "app.py"
flask init-db

# 5) Lisää alkutiedot (luokittelut)
sqlite3 database.db < init.sql

# 6) Käynnistä sovellus
flask run
# Selaimessa: http://127.0.0.1:5000/

