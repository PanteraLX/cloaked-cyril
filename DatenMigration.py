#!/usr/bin/python
# Skript: M122_Scripts/phyton/DatenMigration.py

import re
import csv

regID = "^[0-9]+$"
regName = "([A-Z][a-zÄäÖöÜü]+\s[A-Za-zÄäÖöÜü\-\']{2,}\s[A-Z][a-zÄäÖöÜü]+)|([A-Z][a-zÄäÖöÜü]+\s[A-Za-zÄäÖöÜü\'\-]{2,})"
regStraHa = "^[A-Za-zäÄüÜöÖéèà\'\s]*\s\d+"
regPLZ = "^\d{4,5}\s[A-Z]{1}[a-z\'\-A-Z]*"
regTel = "^((\+41)\d{9}|0\d{2}\s\d{3}\s\d{2}\s\d{2}|0\d{2}\s\d{3}\d{2}\d{2}|0\d{2}\s\/\s\d{3}\s{1}\d{2}\s\d{2})$"
regMail = "[a-zA-Z0-9\.\-_]+@[a-zA-Z0-9\.\-_]+\.[a-z]{2,}"
regIP = "^((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])$"
regDatum = '^((0?[1-9]|[12][012345678]|19)\.(0?[1-9]|1[012])|29\.(0?[13-9]|1[012])|30\.(0?[13-9]|1[012])' \
           '|31\.(0?[13578]|1[02]))\.(19|20)\d\d|29\.02\.(19|20)([02468][048]|[13579][26])$'

file = 'Data1.csv'

# Daten werden sortiert in valide Datensätze und nicht-valide.
# Bei nichvaliden wird das ungültige Feld mit ** markiert im output
outputNotOK = open('Data1NotOk.csv', 'w')
outputOK = open('Data1Ok.csv', 'w')

try:
    with open(file) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            okaycounter = 0
            rowString = ''

            # AdressNr
            if re.match(regID, row[0]):
                okaycounter += 1
                rowString += row[0] + ';'
            else:
                rowString += '**' + row[0] + '**' + ';'

            # Vorname Name
            if re.search(regName, row[1]):
                okaycounter += 1
                rowString += row[1] + ';'
            else:
                rowString += '**' + row[1] + '**' + ';'

            # Strasse Hausnummer: der Mühleweg wurde unter Windows als nichtvalid erfasst (Problem bei Zeichencodierung),
            # bei Linux sollte es gehen
            if re.search(regStraHa, row[2]):
                okaycounter += 1
                rowString += row[2] + ';'
            else:
                rowString += '**' + row[2] + '**' + ';'

            # PLZ Ort
            if re.search(regPLZ, row[3]):
                okaycounter += 1
                rowString += row[3] + ';'
            else:
                rowString += '**' + row[3] + '**' + ';'

            # Telefonnummer
            # Telefonnummer von Klaus Meier wird auch aussortiert, da eine solche Nummer in der Schweiz nicht möglich ist
            if re.search(regTel, row[4]):
                okaycounter += 1
                rowString += row[4] + ';'
            else:
                rowString += '**' + row[4] + '**' + ';'

            # Emailadresse
            if re.search(regMail, row[5]):
                okaycounter += 1
                rowString += row[5] + ';'
            else:
                rowString += '**' + row[5] + '**' + ';'

            # IP4 Adresse
            if re.search(regIP, row[6]):
                okaycounter += 1
                rowString += row[6] + ';'
            else:
                rowString += '**' + row[6] + '**' + ';'

            # Datum
            if re.search(regDatum, row[7]):
                okaycounter += 1
                rowString += row[7]
            else:
                rowString += '**' + row[7] + '**' + ';'

            # Zählt, ob alle 8 RegexTests erfolreich sind
            if okaycounter < 8:
                outputNotOK.write(rowString + '\n')
            else:
                outputOK.write(rowString + '\n')
except IOError:
    print('Das File kann nicht geöffnet werden:', file)

outputOK.close()
outputNotOK.close()