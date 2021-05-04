# NTP - Dizajn i implementacija softvera za analizu Smalltalk programskog koda

Milena Laketić SW 15-2017

# Predlog i opis problema

Kreirao bi se REST api koji bi odgovarao na upite o tome gde se sve neka klasa ili poruka koristi (referencira) u kodu napisanom u Pharo programskom jeziku. Upit bi se sastojao od repozitorijuma gde se nalazi Pharo projekat i naziva klase/poruke čija se upotreba traži u projektu. Celine projekta bi se parsirale konkurentno sa ciljem postizanja što boljih performansi. Gramatika za Pharo jezik bi bila napisana pomoću textX-a i na osnovu nje kreiran parser. Rezultat parsiranja bio bi json fajl sa odgovorom na upit, odnosno mestima gde se u projektu referencira tražena klasa ili poruka. Klijentska strana mogla bi biti implementirana u React frameworku radi lakše demonstracije rada (uz eventualne dodatne vizualizacije dobijenih referenci, ovo ostaje otvoreno za predloge, ali je akcenat svakako na parseru i api servisu).
