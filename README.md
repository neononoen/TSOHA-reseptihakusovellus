**Reseptiholvi-reseptihakusovellus**

Reseptiholvin käyttäjät voivat lisätä reseptejä, kommentoida reseptejä sekä antaa reseptille arvosanan. Reseptin voi myös lisätä suosikiksi, jolloin sen löytää helposti omasta profiilista. Reseptejä voi hakea ja katsella ilman sisäänkirjautumista, muut ominaisuudet vaativat sisäänkirjautumisen.

Sovelluksen käynnistysohjeet:

1. Kloonaa tämä repositorio koneellesi.
2. Siirry repositorion juurikansioon.
3. Luo kansioon .env-tiedosto, ja määritä tiedoston sisältö seuraavanlaiseksi:
    DATABASE_URL=<tietokannan-paikallinen-osoite>
    SECRET_KEY=<salainen-avain>
4. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet seuraavilla komennoilla:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r ./requirements.txt
5. Määritä tietokanta komennolla:
    psql < schema.sql
6. Käynnistä sovellus komennolla:
    flask run
