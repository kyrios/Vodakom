


# Ausgangslage
AI-Agenten werden zunehmend leistungsfähiger und können immer komplexere Aufgaben übernehmen.
Doch ähnlich wie neue Mitarbeiter fehlt ihnen zu Beginn das Erfahrungswissen, das erfahrene Kolleginnen und Kollegen über Jahre hinweg aufgebaut haben.
Dieses Wissen lässt sich nicht einfach abfragen – es besteht oft aus **„Unknown-Unknowns“**, also Dingen, von denen man gar nicht weiß, dass man sie wissen müsste.


Menschen werden deshalb „eingelernt“: Ihre Arbeitsergebnisse werden überprüft, sie erhalten Feedback, bewerten dieses und speichern neues Wissen langfristig ab. So entwickeln sie sich Schritt für Schritt zu erfahrenen Fachleuten.
  
Mit ***Learnium*** ermöglichen wir AI-Agenten etwas Ähnliches:
Ein System, das über Feedback langfristig dazulernt – mit einem echten Langzeitgedächtnis.


# Übungsaufgabe

## Szenario
Petra arbeitet in der Marketingabteilung bei **Vodakom**.

Sie möchte einen Sondernewsletter an alle Kundinnen und Kunden senden, die  ein **iPhone  nutzen**.

Die IT-Abteilung hat ihr dafür den AI-Agenten **Aishe** bereitgestellt.
Aishe kann Daten abfragen und CSV-Dateien mit E-Mail-Adressen erzeugen.

Petra schreibt an Aishe:

> „Ich hätte gerne eine Liste von Kunden mit E-Mail-Adressen, die ein iPhone benutzen.“

Aishe antwortet prompt und liefert eine Datei mit 5 E-Mail-Adressen die  alle mit @example.com enden. Das macht Petra stutzig.

Petra wendet sich an ihren Kollegen **Horst**, der seit 20 Jahren bei Vodakom arbeitet und als **AI-Mentor** für die Einarbeitung von Aishe zuständig ist.
Horst prüft, welche Datenquelle Aishe verwendet hat:
Aishe hat auf eine Tabelle namens **ALL_IPHONE_CUSTOMERS** zugegriffen – eine alte, Demo Tabelle, deren Ursprung unklar ist.

Horst gibt natürlichsprachliches Feedback an Aishe. Er nutzt dazu ein spezielles Interface, das ihm Vodakom zur Verfügung gestellt hat. (Weiterer AI-Agent der das Feedback verarbeitet und Aishe bereitstellt.)

> „Abfragen zu Kundendaten müssen immer mit der Tabelle X_SUB erfolgen. Die genutzten Endgeräte können über einen JOIN zur Tabelle UEQ ermittelt werden. Das steht für User Equipment. Außerdem musst du wissen dass iPhones bei uns intern einfach als "APL“ bezeichnet werden.

  
Kurz darauf versucht Petra dieselbe Anfrage erneut.

Diesmal liefert Aishe die korrekte Liste aller iPhone-Nutzer mit ihren E-Mail-Adressen. 


## Aufgabe
Entwickelt  einen funktionierenden Prototypen, mit dem ein AI-Agent aus dem Feedback eines Mentors wie Horst **langfristig lernen** kann.

Euer Ergebnis sollte zeigen, wie der Agent neues Wissen speichert, auf ähnliche Situationen überträgt und im nächsten Durchlauf **verbesserte Ergebnisse** liefert.

### Bonuspunkte
- Weboberfläche zur Interaktion mit den AI-Agenten
- Docker-Container für einfache Bereitstellung

# Hinweise
- Die Daten sind in der Datei *vodakom_schema.sql* beschrieben. Ihr könnt sie in einer lokalen Datenbank (z.B. SQLite, PostgreSQL) importieren.
- Für die Entwicklung des Prototypen könnt ihr beliebige Programmiersprachen und Frameworks verwenden.
- Im Ordner 'code' findet ihr eine sehr einfache Beispielimplementierung in Python. Das README.md darin enthält Hinweise zum Starten und Testen. Ihr solltet den Code aber nicht als Beispielcode oder Ausgasbe für eure Lösung betrachten. Er dient lediglich zur veranschaulichung der Aufgabe in einem sehr einfachen Rahmen.