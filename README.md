1. Sovelluksessa käyttäjät pystyvät etsimään peliseuraa sulkapalloon. Ilmoituksessa lukee missä ja milloin pelivuoro on sekä tarvittava pelaajien määrä.
2. Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. -Käyttäjä pystyy lisäämään ilmoituksia ja muokkaamaan ja poistamaan niitä.
3. Käyttäjä näkee sovellukseen lisätyt ilmoitukset. -Käyttäjä pystyy etsimään ilmoituksia sen perusteella, milloin vuoro on.
4. Käyttäjäsivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan ilmoituksista.
5. Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. Kumpula Unisport, keskitason pelaaja).
6. Käyttäjä pystyy ilmoittautumaan pelivuoroon. Ilmoituksessa näytetään, ketkä käyttäjät ovat ilmoittautuneet.

Pääasiallinen tietokohde on ilmoitus ja toissijainen tietokohde on ilmoittautuminen.


Näin käyttäjä asentaa sovelluksen:
Asenna flask-kirjasto:

$ pip install flask

Luo tietokannan taulut ja alkutiedot:

$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
Käynnistä sovelluksen näin:

$ flask run
