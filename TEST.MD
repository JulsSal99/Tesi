---
title: "Tesi"
bibliography: biblio.bib
link-citations: true
---

MAIN:
============

serve un survey sui dataset di registrazioni vocali (più sono simili alla nostra idea meglio è) e una ricerca di lavori che parlino dei tempi di risposta in dialoghi realistici, per quest'ultimo punto forse il prof Avanzini aveva dei riferimenti, ma in generale mi appoggerei a google scholar per la ricerca di articoli riguardanti entrambi gli argomenti.

Riguardo al protocollo, quello da definire le ricordo che consiste in:
- Posizionamento dello speaker e dei microfoni (centro stanza? entrambi i mic a 1mt, uno frontale e l'altro a 90°? registrazioni aggiuntive in spazi reali?)
- Impostazione e calibrazione dell'hardware (ovviamente questo campo lo si compila solo quando avremo di nuovo accesso al dipartimento)
- Reclutamento dei soggetti: per ora definirei quanti e con che caratteristiche, una volta fissati questi due punti procediamo tutti insieme al reperimento delle persone
- Modalità di svolgimento dell'intervista: briefing, argomenti, tecnica di stimolazione, durata. forse varrebbe la pena fare 3 sessioni per ogni soggetti: una a un volume di voce normale; una a voce più portata, come se fossero lontani e dovessero parlare con noi; e una con dei suoni non verbali tipo "hm, eh, si, hem, uh uh?, ah!"
- Modalità di salvataggio dei file raw (direi 1 solo wav per ogni take, con left e right corrispondenti ai 2 microfoni, quindi se si fanno 3 sessioni per soggetto ci saranno 3 file per soggetto) e protocollo di nominazione dei file raw
- Modalità di salvataggio dei file tagliati e relativa nomenclatura e organizzazione nel file system
- Compilazione di un foglio di calcolo che riporti tutti i dati del caso
Riguardo allo script python, l'obiettivo è avere una funzione che dato in ingresso 
- path delle registrazioni, 
- array con id degli speaker da usare, (visto che c'è la possibilità di fare dialoghi a 3 forse farei registrare anche un "e tu?" a ogni soggetto, in modo da poterlo infilare tra le risposte di più soggetti)
- numero di domande per persona
- stringa per il nome di file di output
- tempo tra domanda e risposta, 
- quantità massima di suoni non verbali
restituisca tanti file quanti parlanti ci sono (nomi dei file di output costruiti concatenando la stringa del nome in ingresso con l'id del parlante), tutti lunghi uguali, che se sovrapposti generano il dialogo desiderato.
suggerisco l'uso delle sole librerie numpy e soundfile, per un esempio di come si possono manipolare file audio in python con queste librerie veda: https://github.com/Kuig/SNDfunc


Tempi di risposta:
============
Riguardo alle pause in diverse stanze:
> I risultati mostrano che la distribuzione dei periodi di pausa non varia nelle diverse camere; in particolare, il maggior numero di occorrenze si ha per periodi della durata pari a 90 ms. Viceversa, il tipo di camera influenza la durata dei periodi di voce.
Nel caso dei monitoraggi in camera anecoica (figura 1A), il maggior numero di occorrenze si ha per tratti di lunghezza pari a 90 ms; tale valore aumenta con la riverberazione della camera: il picco di occorrenze è a 120 ms per la camera semi riverberante (figura 1B) e a 150 ms per la camera riverberante (figura 1C). [^1]
> "per i non professionisti della voce [...] i picchi delle occorrenze medie si attestano a 60 ms per i tratti di pausa e a 90 ms per la voce." e "50 ms per i tratti di pausa e a 100 ms per la voce." con un "periodo base dei due dispositivi, che è pari a 30 ms e 50 ms rispettivamente." [^2]



NOMENCLATURA FILES
============

| cartella      | LETTERA_SOGGETTO | _ | NUMERO_PORTAMENTO_VOCE_DISTANZA | _ | TIPO_CONGIUNZIONE | .wav |
| ------        | ---------------- | - | ------------------------------- | - | ----------------- | ---- |
| \dialoghi     | A                | _ | 1                               |   |                   | .wav |
|               | A                | _ | 2                               |   |                   | .wav |
|               |                  |   |                                 |   |                   |      |
| \congiunzioni | A                | _ | 1                               | _ | A                 | .wav |
|               | A                | _ | 2                               | _ | B                 | .wav |

- il nome del file potrebbe essere fatto per esempio    "LETTERA_SOGGETTO"_"NUMERO_PORTAMENTO_VOCE_DISTANZA".wav   
<br> dove: "LETTERA_SOGGETTO" e "NUMERO_PORTAMENTO_VOCE_DISTANZA" vengono indicati nel dataset in un file .nfo o txt. 
<br> Nel caso di catalogazione anche in base a Maschio/femmina si può aggiungere un tag "M"/"F" ?


DOMANDE:
============
- la persona fa una domanda ad un altro? Ma facendo così non esce una catena un po' irrealistica?
- Un unico intervistatore che fa più domande separate? Potrebbe essere utile per capire se la persona riesce a capirlo anche separato da uno spazio diverso (per evitare l'effetto ABX-test).
- Le persone devono usare dei nomi? Perché se usiamo dei nomi, si differenziano tra maschi e femmine. Potrebbe essere interessante vedere anche la correlazione tra nomi e pronunce (gli ascoltatori potrebbero venire ingannati per alcune caratteristiche della persona e non il livello vocale).

<div id="refs"></div>

# Citazioni: {-}
[^1]:[Vedi, *pp. 3-4*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
[^2]:[Vedi, *pp. 6-7*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)