import streamlit as st
#streamlit run app.py

st.title('Streamlit aplikacija')
st.write('Nika Demšar')

st.write(""" 1. Analiza podatkov:

    Na tej strani uporabnik pridobi vpogled v filme, ki so najbolj ocenjeni glede na povprečne ocene in število ocen.
    Omogočeni so različni filtri, s katerimi lahko prilagodi iskanje:
    - Minimalno število ocen: uporabnik lahko določi, koliko ocen mora film vsaj imeti, da se upošteva.
    - Žanr: filtriranje filmov glede na izbrani žanr, kar omogoča fokus na določene filmske kategorije.
    - Leto: uporabnik lahko izbere tudi časovno obdobje oziroma leto izida filma.
    
    Na koncu se prikaže seznam desetih filmov, ki ustrezajo izbranim kriterijem, skupaj s povprečno oceno in številom prejetih ocen.  
    """)

st.write(""" 2. Primerjava dveh filmov:

    Ta stran omogoča uporabniku primerjavo dveh poljubnih filmov iz zbirke.
    Po izbiri filmov sistem prikaže podrobne informacije o ocenah za vsak film:
    - Statistični podatki: povprečna ocena, število ocen in standardni odklon ocen, ki kaže na variabilnost ocen.
    - Histogram ocen: grafični prikaz porazdelitve vseh uporabniških ocen, kar vizualno poudari, kako so filmi ocenjeni.
    - Graf povprečne letne ocene: prikazuje, kako se je povprečna ocena filma spreminjala skozi leta.
    - Graf števila ocen na leto: omogoča spremljanje priljubljenosti filma skozi čas na podlagi števila prejetih ocen.
    """)

st.write(""" 3. Priporočilni sistem:

    Priporočilni sistem predstavlja najbolj interaktivni del aplikacije, kjer uporabniki lahko ustvarijo svoj profil z registracijo in prijavo.

    Ko uporabnik vnese vsaj deset ocen, sistem izračuna in prikaže deset filmov, ki bi mu lahko bili všeč.
    Priporočila temeljijo na tehtanem povprečju ocen uporabnikov, ki imajo podobne preference, pri čemer se izločijo filmi, ki jih je uporabnik že ocenil.

    Uporabnik sproži generiranje priporočil s klikom na gumb "Priporoči mi filme", kar omogoča, da sam odloča, kdaj želi prejeti priporočila.
    """)
