#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import lxml
import os
import sys
from datetime import datetime
from tkinter import filedialog
from tkinter import *

# Parte grafica
root = Tk()
root.withdraw()
folder_selected = None
try:
    folder_selected = filedialog.askdirectory()
except:
    print("Non hai selezionato nessuna cartella")


# Classe IVA
class iva:
    aliquota = " "
    imposta = "0.00"
    ammontare = "0.00"
    def riepilogo(self):
        riepilogo = self.aliquota + "; " + str(self.ammontare) + "; " + str(self.imposta) + "; " + str(float(self.ammontare)+float(self.imposta)).replace(".", ",") + ";"
        return riepilogo

# Recupero directory dove sono i file, togliere il commento se si preferisce indicare il percorso da riga di comando
# dir = str(sys.argv[1])

# Commentare queste due righe per disattivare l'interfaccia grafica
dir = folder_selected
fileList = os.listdir(dir)

# Creazione file e riga intestazione del file csv
intestazione = "ID Dispositivo; Data; Esenzione; Importo; IVA 4%; IVA 5%; IVA 10%; IVA 22%"
f = open(dir + "/" + "riepilogo.csv", "w")
f.write(intestazione + "\n")
f.close()

# Recupero dati corrispettivi per ogni file xml presente nella cartella
for file in fileList:
    if file.endswith(".xml"):
        tree = ET.parse(open((dir + "/" + file),"r"))
        root = tree.getroot()

        esente = iva()
        iva4 = iva()
        iva5 = iva()
        iva10 = iva()
        iva22 = iva()
        dataRilevazione = ""
        id_dispositivo = ""
        dataArray = []

# Ricerca dei dati in ogni rigo del file xml
        for x in root:
            if(x.tag == "DataOraRilevazione"):
                dataRilevazione = x.text[:-15]
                dataArray.append(dataRilevazione)

            for y in x:

                for z in y:
                    if(z.tag == "ImportoParziale"):
                        dataArray.append(z.text)
                    if(z.tag == "Natura"):
                        dataArray.append(z.text)
                    if(z.tag == "IdDispositivo"):
                        id_dispositivo = z.text
                        

                    for w in z:
                        if(w.tag == "AliquotaIVA"):
                            if(w.text == "4.00"):
                                dataArray.append(w.text)
                            if(w.text == "5.00"):
                                dataArray.append(w.text)
                            if(w.text == "10.00"):
                                dataArray.append(w.text)
                            if(w.text == "22.00"):
                                dataArray.append(w.text)

                        if(w.tag == "Imposta"):
                            dataArray.append(w.text)
        
# Riempimento di un array temporaneo con i dati dei corrispettivi divisi per aliquota        
        for index, element in enumerate(dataArray):
            if(element == "4.00"):
                iva4.aliquota = dataArray[index].replace(".00", "%")
                iva4.imposta = dataArray[index + 1]
                iva4.ammontare = dataArray[index + 2]
            if(element == "5.00"):
                iva5.aliquota = dataArray[index].replace(".00", "%")
                iva5.imposta = dataArray[index + 1]
                iva5.ammontare = dataArray[index + 2]
            if(element == "10.00"):
                iva10.aliquota = dataArray[index].replace(".00", "%")
                iva10.imposta = dataArray[index + 1]
                iva10.ammontare = dataArray[index + 2]
            if(element == "22.00"):
                iva22.aliquota = dataArray[index].replace(".00", "%")
                iva22.imposta = dataArray[index + 1]
                iva22.ammontare = dataArray[index + 2]
            if("N" in element):
                esente.aliquota = dataArray[index]
                esente.ammontare = dataArray[index + 1]

# Formattazione della data in formato dd-mm-yyyy
        date_format = '%Y-%m-%d'
        datetime_object = datetime.strptime(dataRilevazione, date_format)

# Riepilogo con calcolo del valore totale per ogni aliquota presente nel file al netto degli annullamenti
        esente = esente.aliquota + "; " + esente.ammontare 
        tot4 = str(float(iva4.ammontare) + float(iva4.imposta))
        tot5 = str(float(iva5.ammontare) + float(iva5.imposta))
        tot10 = str(float(iva10.ammontare) + float(iva10.imposta))
        tot22 = str(float(iva22.ammontare) + float(iva22.imposta))
       
# Aggiunta della riga con i dati al file csv
        tempString = id_dispositivo + "; " + "{:%d/%m/%Y}".format(datetime_object) + "; " + esente + "; " + tot4 + "; " + tot5 + "; " + tot10 + "; " + tot22
        f = open(folder_selected + "/" + "riepilogo.csv", "a")
        f.write(tempString.replace(".", ",") + "\n")
        f.close()
