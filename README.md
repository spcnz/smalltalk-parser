# NTP - Dizajn i implementacija softvera za analizu Smalltalk programskog koda

Milena Laketić SW 15-2017

# Predlog i opis problema

Glavne funkcionalnosti: odgovaranje na upite o referencama na klase i poruke u programskom kodu napisanom u Pharo programskom jeziku (find all references).

Model resenja i komunikacija izmedju komponenti prikazana je na diagramu. 
![alt text](https://github.com/specnazm/smalltalk-parser]/blob/main/components.png?raw=true)

Spomenute klase (Location, ReferenceParam) opisane su https://github.com/Microsoft/language-server-protocol/blob/main/versions/protocol-1-x.md. Po tome bi se vrsila implementacija protokola.
Sistem bi se sastojao od 2 glavna dela : 
- Python server koji bi generisao parser za Pharo programski jezik upotrebom TextX
- Go rest server koji bi implementirao Language Server Protocol

Parser bi se kreirao dinamicki za definisanu gramatiku Pharo jezika. Rezultat parsiranja bio bi json poruka sa mestima gde se u projektu referencira tražena klasa ili poruka.
A komunikacija sa Go serverom bi se obavljala ili preko socket-a ili preko rest-a. Celine projekta bi se parsirale konkurentno sa ciljem postizanja što boljih performansi.

Go rest server podrzavao bi 2 tipa zahteva: notifikacije i zahteve (notifikacije sa id, na koji se ocekuje odgovor od servera) u formatu JSON-RPC. Ulazna tacka u sistem bila bi notifikacija o otvaranju projekta sa parametrom projectUri odnosno putanjom do workspace-a. Nakon toga resenje radi nad fajlovima unutar tog workspace-a. Izlaz (promena projekta) je notifikacija o zatavanju projekta. Rezultati parsiranja za otvoreni projekat bi se cuvali sve dok ne dodje do notifikacije o izmeni odredjenog dokumenta.

Klijentska strana bi verovatno bio Visual Code development alat koji sam podrzava ovaj protocol. Ukoliko ne bude moguce integrisati resenje sa vscode onda bi klijentska strana bila kreirana kao jednostavan interfejs radi demonstracije resenja.


