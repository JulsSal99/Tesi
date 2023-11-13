---
title: "Tesi - Registrazioni e generazione linee di dialogo "
bibliography: biblio.bib
link-citations: true
---

# Tesi: Registrazioni e generazione linee di dialogo 

MAIN:
============

serve un survey sui dataset di registrazioni vocali (più sono simili alla nostra idea meglio è) e una ricerca di lavori che parlino dei tempi di risposta in dialoghi realistici, per quest'ultimo punto forse il prof Avanzini aveva dei riferimenti, ma in generale mi appoggerei a google scholar per la ricerca di articoli riguardanti entrambi gli argomenti.

Riguardo al protocollo, quello da definire le ricordo che consiste in:
- Posizionamento dello speaker e dei microfoni (centro stanza? entrambi i mic a 1mt, uno frontale e l'altro a 90°? <span style="color:red">registrazioni aggiuntive in spazi reali?)</span>
- Impostazione e calibrazione dell'hardware (ovviamente questo campo lo si compila solo quando avremo di nuovo accesso al dipartimento)
- Reclutamento dei soggetti: per ora definirei quanti e con che caratteristiche, una volta fissati questi due punti procediamo tutti insieme al reperimento delle persone
- Modalità di svolgimento dell'intervista: briefing, argomenti, tecnica di stimolazione, durata. forse varrebbe la pena fare 3 sessioni per ogni soggetti: <span style="color:red"> una a un volume di voce normale; una a voce più portata, come se fossero lontani e dovessero parlare con noi; </span> e una con dei suoni non verbali tipo "hm, eh, si, hem, uh uh?, ah!"
- Modalità di salvataggio dei file raw (direi 1 solo wav per ogni take, con left e right corrispondenti ai 2 microfoni, quindi se si fanno 3 sessioni per soggetto ci saranno 3 file per soggetto) e protocollo di nominazione dei file raw
- Modalità di salvataggio dei file tagliati e relativa nomenclatura e organizzazione nel file system
- Compilazione di un foglio di calcolo che riporti tutti i dati del caso
Riguardo allo script python, l'obiettivo è avere una funzione che dato in ingresso 
- path delle registrazioni, 
<span style="color:red">- array con id degli speaker da usare, (visto che c'è la possibilità di fare dialoghi a 3 forse farei registrare anche un "e tu?" a ogni soggetto, in modo da poterlo infilare tra le risposte di più soggetti)</span>
- numero di domande per persona
- stringa per il nome di file di output
- tempo tra domanda e risposta, 
- quantità massima di suoni non verbali ()
restituisca tanti file quanti parlanti ci sono (nomi dei file di output costruiti concatenando la stringa del nome in ingresso con l'id del parlante), tutti lunghi uguali, che se sovrapposti generano il dialogo desiderato.
suggerisco l'uso delle sole librerie numpy e soundfile, per un esempio di come si possono manipolare file audio in python con queste librerie veda: https://github.com/Kuig/SNDfunc

Protocollo sperimentale per le registrazioni
- <span style="color:green">Spiegazione iniziale a ogni soggetto
   -> Obiettivi della registrazione
   -> Come bisogna parlare durante la registrazione: non sovrapporti,</span>
conta fino a 5, ecc.
   -> ... altro
- Parte A. Un tot di argomenti/domande. Per ciascuna domanda il soggetto
     1) fornisce la sua risposta
     2) fa lui la stessa domanda rifrasandola
- Parte B. Un tot di suoni non verbali: a-hem, coff, a-ha, aah!, hm-hm, ecc.

Setup<span style="color:green">
- Registrazione stereo con due mic a 1 metro
- In cabina Malcangi</span>
- Per parte B: eventualmente il soggetto ascolta un parlatore
- .... da pensare

Assemblaggio dialoghi
- Struttura (dom)->(risp+dom)->(risp+dom)-> ... ->(risp)
- Non serve che la prima domanda sia diversa dalle altre
- Il dialogo può essere con n persone ordinate a caso: (i-1) chiede a
(i), che risponde e chiede a (i+1), ecc.
- Numero n di persone e lunghezza del dialogo definibili a piacere
- A una risposta possono venire sovrapposti suoni non verbali di altre
persone
- Ogni persona ha il suo array di domande shuffle-ato (si può ripetere
la stessa domanda in un dialogo)

# Procedimento:

## Attrezzatura e locazione:

Verrà usata la stanza insonorizzata anecoica di celoria 22 (Malcangi).
Il partecipante all'esperimento verrà piazzato al centro stanza. Verranno usati due microfoni, di cui uno frontale e l'altro angolato di 90° e posizionati entrambi a 1 metro di distanza all'altezza della bocca. 
... per ricreare una impostazione ambisonic del secondo ordine.
<span style="color:red"> (eventuali registrazioni aggiuntive della camera?) </span>
E' stata usata inoltre usata una scheda audio Motu M3 con gain a ... e due microfoni ...
La registrazione dei due microfoni avviene in formato stereo. Con come uscita un file wav 24bit-192kHz.

## Procedimento in stanza con i partecipanti

Uno dei problemi principali nell'esecuzione del nostro test è stata l'identificazione delle metodologie di registrazione in modo che: 
 - Non ci fossero **sovrapposizioni** tra audio dell'intervistatore e dell'intervistato (dalle ricerche [Analisi dei tempi di risposta](#analisi-dei-tempi-di-risposta) è stato appurato che il tempo di pausa tra domanda e risposta può ridursi fino a generare una sovrapposizione tra domanda e risposta) 
 - Non ci fosse ritorno, se non isolabile nel microfono di ulteriori possibili suoni (al di fuori del partecipante all'esperimento)
 - Le risposte fossero realistiche
 - Fosse possibile osservarne anche i tempi di risposta per confermarne la veridicità o alla fine di una più completa raccolta dati

<span style="color:red"> <br> 
Inizialmente abbiamo ipotizzato una struttura in cui venissero poste prima tutte le domande dall'intervistatore all'intervistato e che solo alla fine di tutto il ciclo di domande si proseguisse a far registrare le domande singole all'intervistato. </span>
   - *problema 1*: possibile sovrapposizione di voci
     - *soluzione 1*: far attendere un tempo in secondi alll'intervistato prima di dare una risposta;
       - problema: non si possono osservare i tempi di risposta.
     - *soluzione 2*: utilizzare delle cuffie in-ear/aperte/chiuse;
       - *problema 1*: l'ascoltatore tenderà ad avere un volume di voce errato perché non si sentirà correttamente: questo è l'[effetto Lombard](#effetto-lombard);
         - *soluzione*: Potremmo eseguire dei test con delle **cuffie** e misurare il volume medio del parlato. Inoltre ascoltare il volume delle cuffie rispetto al volume del parlato in db. In generale: se volume cuffia a 1mt tappata <<< volume del parlato && volume parlato CON cuffia ≃ volume parlato SENZA cuffia --> procedere.
         Nello specifico, ho provato ad eseguire un test con delle cuffie in-ear ed il risultato è stato di un volume del parlato inferiore, probabilmente generato dalla conduzione ossea della voce causato dalla cuffia. Un ulteriore test è stato eseguito tra un solo padiglione e entrambi i padiglioni della cuffia ed il risultato è stato di un volume minore quando entrambe i padiglioni sono indossati.
         La soluzione quindi ipotetica è una cuffia chiusa sopra-aurale per evitare il ritorno nel microfono che dovrà essere indossata ogni volta dal partecipante all'esperimento, ma esclusivamente per ascoltare la domanda e non per fornirne la risposta.
         Il volume in cuffia sarà deciso prima dell'esperimento dall'operatore e rimarrà invariato per non influenzare l'esperimento
       - *problema 2*: le latenze del DAW devono essere irrisorie poiché per misurare il tempo di attesa bisogna che l'audio in cuffia sia in tempo reale;
   - *problema 2*: le domande registrate potrebbero risultare tutte troppo uguali poiché l'intervistato sarà tentato a ripetere parola per parola la domanda originale;
     - *soluzione 1*: L'intervistato ripete la domanda **dopo** aver dato la risposta, così facendo l'intervistato probabilmente non si ricorderà l'esatta domanda, ma la deducerà dalla sua risposta;
       - *problema 1*: l'intervistato potrebbe non ricordarsi la domanda originale o potrebbe produrre una risposta non coerente;
         - *Soluzione*: sta all'operatore *eventualmente* intervenire valutandone la coerenza con la domanda originale.
     - *soluzione 2*: viene dato all'intervistato un **prompt generico** il più lontano possibile dalla domanda originale e verrà fatto un cenno gestuale per indicare di procedere alla risposta in modo da non generare sovrapposizioni (dopo una durata in secondi prestabilita)

<span style="color:red"> <br> 
Inoltre è possibile registrare una serie di domande introduttive in modo che si possano generare dialoghi con più risposte per una medesima domanda </span>
  - *soluzione 1*: dopo aver fatto registrare la domanda, gli viene chiesto di ripeterla interamente aggiungendoci all'inizio un "e tu?".
      - *problema 1*: così facendo la prima domanda del ciclo avrà sempre un'interrogazione come se fosse la seconda domanda
  - *soluzione 2*: conoscendo i [tempi di pausa](#tempi-di-pausa), far registrare alla fine, assieme ai suoni non verbali, diverse frasi come **"e tu?", "invece te?", "quindi?", "Allora", "eee..."** con diverso *portamento*.
      - *problema 1*: il tono può variare?
        - *soluzione 2*: il partecipante dopo aver risposto conta 5 secondi con le dita e poi legge la domanda introduttiva ("eh tu?"), poi conta 5 secondi e dopo pronuncia la domanda effettiva ("come è stata la tua giornata?")
      - *problema 2*: TANTI TANTI files....

<span style="color:red"> <br> 
Per i suoni non verbali: </span>
  - *soluzione 1*: ad ogni partecipante verrà data la cuffia in-ear e fatto ascoltare un audio completo, se eseguito con le in-ear e verrà chiesto di produrre dei suoni di sottofondo.
  - *soluzione 2*: viene chiesto al partecipante di pronunciare con diverso *portamento* dei versi basandosi su alcuni prestabiliti come **"a-hem, coff, a-ha, aah!, hm-hm, ecc."**).

## Il programma
Verranno realizzati diversi files, uno per ogni parlante + uno unico in cui ci sarà la somma di tutti i partecipanti al dialogo.
I files audio singoli manterranno le pause e anche il silenzio quando parlano gli altri partecipanti.

Le componenti che comporranno le linee di dialogo sono: le **domande**, le **risposte**, le **domande iniziali** (eg. "e tu?"), le **pause** e il **silenzio** antecedente a ogni risposta.
Le domande, le risposte e le pause saranno organizzati in modo da seguire una struttura
> Domanda_P_N &rarr; Risposta_P+1_N &rarr; DomandaIniziale_P+2_N &rarr; Domanda_P+2_N &rarr; Risposta_P+3_N &rarr; ... &rarr; Risposta_P+K_N &rarr; **si ripete il ciclo per N domande**

A queste si aggiungono le pause e i silenzi
> Domanda_P_N &rarr; *Pausa* &rarr; Risposta_P+1_N &rarr; *Pausa* &rarr; DomandaIniziale_P+2_N &rarr; *Silenzio* &rarr; Domanda_P+2_N &rarr; *Pausa* &rarr; Risposta_P+3_N &rarr; ... &rarr; Risposta_P+K_N &rarr; *Pausa* &rarr; **si ripete il ciclo per N domande**



## Numenclatura dei files
Per meglio spiegare l'organizzazione dei files stabiliamo:
 - **T** = "tipologia: generale, domanda, risposta, domanda iniziale o suono non verbale" [G/D/A/IQ/S]
 - **N** = *numero della domanda o risposta*
 - **P** = *identificativo del partecipante al test*
 - **S** = *sesso del partecipante al test* [M/F]

### Nomi dei files durante la registrazione
Verranno generati due audio per ogni speaker:
- Per le domande e risposte: 
> *T_P.wav*
- Per i suoni non verbali: 
> *T_P.wav*

<br>
Esempio:

> "G_A" 

&rarr; indica la traccia generale con tutte le domande e le risposte della persona A

> "S_A"

&rarr; indica la traccia con un suono non verbale della persona A

Le tracce verranno poi tagliati per suddividere singolarmente le domande e le risposte secondo il seguente ordine:

### Nomi dei files nel programma
I nomi dei files da dare in input al programma saranno organizzati così:
- Per le domande e risposte: *T_P_S_N_PORTAMENTO*
- Per i suoni non verbali: *T_P_V*

Esempio dei nomi dei files in input:

| cartella      | T_P_N               | _S  | _PORTAMENTO | .wav |
| ------        | -:                  | :-: | :-          | :-   |
| \INPUT        | Q_Giovanni_1        | _M  | _ALTO       | .wav |
| \INPUT        | A_Giovanni_1        | _M  | _ALTO       | .wav |
| \INPUT        | QI_Giovanni_1       | _M  | _ALTO       | .wav |
| \INPUT        | S_Giovanni          | _M  |             | .wav |
| | | | | |
| \INPUT        | Q_Elena_1           | _F  | _ALTO       | .wav |
| \INPUT        | A_Elena_1           | _F  | _BASSO      | .wav |
| \INPUT        | S_Mario             | _M  |             | .wav |

<br>

# Cos'è Ambisonic?
Ambisonics non invia il segnale audio a un numero particolare di altoparlanti; È "indipendente dal parlante". Invece, Ambisonics può essere decodificato in qualsiasi array di altoparlanti (maggiori informazioni di seguito). L'audio ambisonico rappresenta una sfera sonora completa e ininterrotta, senza essere limitata dalle limitazioni di uno specifico sistema di riproduzione. 

# Effetto Lombard
"L'effetto Lombard (Lombard effect o Lombard reflex) è la tendenza involontaria dei parlanti ad aumentare l'intensità della loro voce in presenza di un rumore di fondo che interferisce con la comprensione della voce umana." [^12]

# Analisi dei tempi di risposta

**Sacks et al. (1974)** hanno distinto tre tipi di silenzi acustici nelle conversazioni: *pausa*, *gap* e *interruzioni* ("lapses") [^1]. 
Questa classificazione si basava su ciò che precedeva e seguiva il silenzio nella conversazione e sulla lunghezza percepita del silenzio. 
Le *pause*, in questo contesto, si riferivano ai silenzi all’interno dei turni; 
le *lacune* si riferivano a silenzi più brevi tra i turni o in possibili punti di completamento (cioè nei punti di rilevanza della transizione o TRP); 
e le *interruzioni* ("lapses") si riferivano a silenzi più lunghi (o prolungati) tra i turni.

Secondo Sacks et al. inoltre ci sono tre possibili modi di organizzare un cambio di parlante: può esserci una pausa intermedia; può esserci sovrapposizione; o non può esserci né pausa né sovrapposizione.

Sacks et al. avevano anche osservato che il caso più comune in una conversazione è quello di un solo interlocutore alla volta e che i cambi di parlante avvengono tipicamente senza alcuna pausa intermedia e senza alcuna sovrapposizione del discorso - no-gap-no-overlap.
"Le transizioni da (un turno al prossimo) con nessun gap e nessuna sovrapposizione sono comuni. Assieme con  transizioni caratterizzate da piccoli gap o leggere sovrapposizioni, fanno la maggiorparte delle transizioni" [^2].

Inizialmente fu anche ipotizzata una possibile lunghezza della pausa da **Jefferson nell'84**:
"A recipient/next speaker does not start up in ‘terminal overlap’, nor ‘latched’ to the very point of possible completion, but permits just a bit of space between the end of a prior utterance and the start of his own" [^3] e quantifica "Just a Bit of Space" con un intervallo silente di circa 150–250 ms. 

Paragrafo 2.3
Una transizione fluida è un termine che si riferisce a un tipo di passaggio tra due persone che parlano in una conversazione. Si verifica quando non c’è una pausa percettibile tra la fine del discorso di una persona e l’inizio del discorso della persona successiva1. Questo significa che, anche se potrebbe esserci un silenzio acustico, il flusso della conversazione rimane ininterrotto1.

La **teoria delle transizioni fluide** è stata studiata da diversi ricercatori, tra cui **Duncan (1972), Kendon (1967) e Yngve (1970)**.

**Walker e Trimboli (1982)** hanno invece stimato che la soglia di rilevamento dei silenzi tra gli interlocutori nelle conversazioni si avvicina ai 200 ms [^4].
Unl'altra teoria 

In generale: 
- *Pausa*: Silenzio seguito da altro discorso dallo stesso oratore.
- *Gap* e *Interruzione*: Silenzio seguito da cambio di oratore anche quando non avviene nei TRP.

Intorno ai 200ms

>"Una caratteristica intrigante del sistema di comunicazione umano è l’infrastruttura interattiva su cui si basa. In entrambe le interazioni di tipo dyadico e multipersonale, la conversazione è altamente strutturata e organizzata secondo principi stabiliti (Sacks et al., 1974). L’interazione degli adulti umani è caratterizzata da un meccanismo di scambio basato su raffiche di informazioni alternate (e relativamente brevi). Nella maggior parte dei casi, solo una persona tende a parlare alla volta e ogni contributo riceve di solito una risposta. Ciò che è notevole è il preciso timing di questi contributi sequenziali, che comporta intervalli tra i turni di parola che in media durano solo circa 200 ms (Stivers et al., 2009)."; [^6]

Secondo lo Studio di **Stivers et al.** del 2009, prendendo in esaminazione 10 linguaggi:
> "I tempi medi di risposta per le risposte soggettivamente puntuali sono molto più lunghi in danese e laotiano (203 e 202 ms, rispettivamente) rispetto al giapponese e al tzeltal (36 e 83 ms, rispettivamente) e confrontando le 3 lingue con offset di risposta più lunghi con tutte le altre, la differenza è significativa [t(847) = −10,97, P < 0,001]. Pertanto, un silenzio di 200 ms, giudicato come un ritardo nella maggior parte delle lingue, è stato ancora considerato in tempo. Tale silenzio non è quindi fenomenologicamente saliente all'interno di una comunità linguistica (ma può esserlo per un osservatore esterno)." [^5]

> "Dalle esperienze psicolinguistiche, sappiamo che il tempo necessario per produrre anche semplici enunciati di una sola parola (min. 600 ms, Indefrey e Levelt, 2004) supera di gran lunga questa durata media dell’intervallo, suggerendo la complessità dei processi cognitivi coinvolti (Levinson, 2013)." [^6]

Questo tempo, però può anche variare: **Kendrick** dimostra che i turni che si occupano di problemi di parlare, ascoltare e capire (cioè, altre iniziative di riparazione) sono governati da diversi principi temporali e possono quindi interrompere il comune modello di intervalli minimi tra i turni. Come rivela l’analisi, i più lunghi intervalli caratteristici delle sequenze di riparazione tendono ad essere utilizzati dai partecipanti come opportunità per permettere al produttore della fonte di problema di risolvere la questione prima che la riparazione venga avviata, per permettersi di risolvere i propri problemi di comprensione prima di avviare la riparazione o per segnalare problemi di comprensione attraverso segnali visivi (ad esempio, sollevamento delle sopracciglia) prima di avviare la riparazione verbalmente. [^7] 

C'è da sottolineare però un particolare: sebbene possa sembrare che i tempi di risposta siano corti, i tempi di inizio risposta non lo sono:
> "I brevi tempi di transizione sono notevoli perché contrastano nettamente con le latenze di inizio del discorso molto più lunghe osservate quando i partecipanti agli esperimenti psicolinguistici producono semplici enunciati. Ad esempio, nominare un oggetto richiede almeno 600 ms (ad esempio, Indefrey e Levelt, 2004) e pianificare una frase che descrive una scena può richiedere più di un secondo (Griffin e Bock, 2000; Konopka, 2012). " [^8]

> "Studi di laboratorio hanno dimostrato che la formulazione linguistica e la pianificazione articolatoria per una singola parola richiedono almeno 600 ms (ad esempio, Indefrey & Levelt, 2004). Le parole elicitate negli studi di laboratorio sono tipicamente nomi di immagini e altri tipi di parole possono essere più veloci da pianificare. Ad esempio, ci si potrebbe aspettare che le particelle, che spesso appaiono all’inizio delle affermazioni, siano più veloci da pianificare rispetto alle parole di contenuto. Tuttavia, Knudsen e colleghi non hanno riscontrato che le affermazioni che iniziano con particelle siano state avviate più velocemente rispetto ad altre affermazioni.” [^9]

Levinson (2016) [^10] ha affermato che i turni durano tipicamente circa due secondi, il che offrirebbe ampio tempo di pianificazione. Inoltre, Levinson e Torreira riportano una durata media del turno di 1680 ms e una mediana di 1227 ms per il corpus NXT-Switchboard [^11] [^9]. 

In generale per domande personali, i tempi di risposta di allungano:
> "Although these studies support the hypothesis that speech planning and listening occur in parallel, participants’ average response times (which are considered lab-equivalents to gap durations) were consis­ tently longer than 200 or 300 ms. These long response times are not particularly noteworthy: In some studies, participants had to answer questions about knowledge or personal experience, which might involve complex memory search processes or decisions between alternatives. What is important, however, is that the average gain in the response latency in the early relative to the late cue condition was substantially less than the time difference between the two cues. For example, par­ ticipants in B¨ogels et al.’s (2015) study responded about 300 ms earlier in the early than the late cue condition, but the early cues occurred on average 1700 ms earlier than the late cues. Thus, a full 1400 ms were “lost”. A likely explanation for this lost time is that participants did not have sufficient time to fully plan their utterance during the preceding question, and so they had to engage in some planning after question end." [^9]

Inoltre contribuisce la complessità della domanda ed il contesto in cui viene posta:
> "There have also been reports that gap durations tend to increase with cognitive load (see e.g. Cappella (1979), and references mentioned therein). Within the Map Task domain, it has been shown that more complex tasks, lack of familiarity with tasks, and presence of conversational game boundaries results in longer gaps (Bull & Aylett, 1998). Several studies have furthermore observed longer gaps in dialogues where the participants have eye contact than in dialogues without eye contact (Beattie & Barnard, 1979; Bull & Aylett, 1998; Jaffe & Feldstein, 1970; ten Bosch, Oostdijk, & de Ruiter, 2004a). The opposite result, faster speaker changes to the extent that average switching times are negative (or overlapping) have also been observed in eye contact vs. no eye contact comparisons (Sellen, 1995). From analyses of pairs of speakers it has also been suggested that speakers adapt the duration of gaps to those of the other participants, that is a form ofaccommodation or interlocutor similarity with respect to gap duration (e.g. Edlund, Heldner, & Hirschberg, 2009; Jaffe & Feldstein, 1970; Kousidis & Dorran, 2009; ten Bosch et al., 2005). Finally, it has been observed that the language differences with respect to gap durations seem to be minor (cf. Weilhammer & Rabold, 2003)." [^3]
> "Dispreferred second pair parts, such as request refusal, are structurally complex; they tend to have a complete grammatical format and make use of a variety of hedging elements, which serve to minimize the threat of disaffiliation (Heritage 1984). These include the following:
Delays, e.g., insertion sequences; Prefaces, e.g., markers or announcers of dispreferreds, such as “Uh” and “Well”; Politeness markers, e.g., appreciation markers and apologies; Hesitations, e.g., self-editing; Accounts: carefully formulated explanations for why the (dispreferred) act is being performed (Levinson 1983, pp. 334–35)." [^13]

# Tempi di Pausa:

Riguardo ai periodi di pausa in un discorso:
- Nel testo di Pavese et al è stata analizzato il tempo di pausa e  professionisti è composto da 5 docenti universitari madre lingua inglesi della London South Bank University e 6 soggetti madre lingua italiani monitorati in stanze con diverse condizioni di riverberazione.
> "I risultati mostrano che la distribuzione dei periodi di pausa non varia nelle diverse camere; in particolare, il maggior numero di occorrenze si ha per periodi della durata pari a 90 ms. Viceversa, il tipo di camera influenza la durata dei periodi di voce.
Nel caso dei monitoraggi in camera anecoica (figura 1A), il maggior numero di occorrenze si ha per tratti di lunghezza pari a 90 ms; tale valore aumenta con la riverberazione della camera: il picco di occorrenze è a 120 ms per la camera semi riverberante (figura 1B) e a 150 ms per la camera riverberante (figura 1C)." [^p1]
> "per i non professionisti della voce [...] i picchi delle occorrenze medie si attestano a *60 ms per i tratti di pausa* e a *90 ms per la voce*." e "*50 ms per i tratti di pausa* e a *100 ms per la voce*." con un "periodo base dei due dispositivi, che è pari a 30 ms e 50 ms rispettivamente." [^p2]

Inoltre, riguardo ai riverberi:
> "la maggiore lunghezza della coda sonora potrebbe portare il parlatore “professionista” ad allungare i periodi di fonazione per migliorare l’intelligibilità del messaggio che deve trasmettere. ", ed è stato osservato che sussiste "un incremento della lunghezza media più occorrente dei periodi di voce in 18 insegnanti che parlavano in aule maggiormente riverberanti rispetto a 24 insegnanti che esercitavano la loro attività didattica in aule con tempi di riverberazione conformi ai requisiti acustici stabiliti per questi ambienti.".
"per i professionisti della voce il periodo più ricorrente è pari a 90 ms, mentre per i non professionisti è molto più corto, pari a 60 e 50 ms", "indice di un parlato molto veloce e probabilmente indipendente dalle caratteristiche acustiche dell’ambiente, ma dipendente invece dal modo di esporre un discorso nel caso di non professionista della voce. Infatti, il parlato di un insegnante potrebbe appartenere al “clear speech” che prevede un incremento della pause e un allungamento dei singoli segmenti di parlato" [^p3]


DOMANDE:
============
- Le persone devono usare dei nomi? Perché se usiamo dei nomi, si differenziano tra maschi e femmine. Potrebbe essere interessante vedere anche la correlazione tra nomi e pronunce (gli ascoltatori potrebbero venire ingannati per alcune caratteristiche della persona e non il livello vocale).
- come capiamo i tempi di risposta, visto che dipendono dal tipo di domanda e dalla reazione?
- sarebbe utile generare dialoghi in base a: 
  - voci femminili? 
  - voci maschili? 
  - random?
  - quante domande e risposte? 
  - Pause irrealistiche? 

- correlazione tra pause, complessità delle domande e velocità di parlato
- possiamo porre le domande in cuffia e osservarne i tempi di risposta.

<div id="refs"></div>

<!-- Citazioni -->
[^1]:[Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). A simplest systematics for the organization of turn-taking for conversation. Language, 50, 696–735.]
[^2]:[Vedi Sacks et al., 1974, p. 700]
[^3]:[Jefferson, 1984, p. 8]
[^3]:[Vedi, "*Pauses, gaps and overlaps in conversations*" di "*Mattias Heldner, Jens Edlund*", *2010*](DOC/1-s2.0-S0095447010000628-main.pdf)
[^4]:[Beattie & Barnard, 1979; Jaffe & Feldstein, 1970; Kendon, 1967]
[^5]:[Stivers, T., Enfield, N. J., Brown, P., Englert, C., Hayashi, M., Heinemann, T., et al. (2009). Universals and cultural variation in turn-taking in conversation. Proc. Natl. Acad. Sci. U.S.A. 106, 10587–10592. doi: 10.1073/pnas.09036 16106]
[^6]:[pp. 7](DOC/608110.pdf)
[^7]:["*The intersection of turn-taking and repair: the timing of other-initiations of repair in conversation*" di Kobin H. Kendrick](https://www.frontiersin.org/articles/10.3389/fpsyg.2015.00250/full)
[^8]:["*Competition Reduces Response Times in Multiparty Conversation*"](DOC/fpsyg-12-693124.pdf)
[^9]:[pp. 3, "*Overrated gaps: Inter-speaker gaps provide limited information about the timing of turns in conversation*"](DOC/1-s2.0-S0010027722000257-main.pdf)
[^10]:[Barthel, M., Sauppe, S., Levinson, S. C., & Meyer, A. S. (2016). "*The timing of utterance planning in task-oriented dialogue: Evidence from a novel list-completion paradigm*". Frontiers in Psychology, 7.](https://doi.org/10.3389/fpsyg.2016.01858)
[^11]:[The NXT-format Switchboard Corpus: a rich resource for investigating the syntax, semantics, pragmatics and prosody of dialogue](DOC/The_NXT_format_Switchboard_Corpus_a_rich_resource_for_investigating_the_syntax_semantics_pragmatics_and_prosody_of_dialogue.pdf)
[^12]:[Lane H, Tranel B, The Lombard sign and the role of hearing in speech, in J Speech Hear Res, vol. 14, n. 4, 1971, pp. 677-709.]
[^13]:["Article Pause Length and Differences in Cognitive State Attribution in Native and Non-Native Speakers", Theresa Matzinger 1,2, Michael Pleyer and Przemysław ˙Zywiczy ´nski]("DOC/languages-08-00026.pdf)

[^p1]:[/////////////////////////Vedi, *pp. 3-4*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
[^p2]:[Vedi, *pp. 6-7*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
[^p3]:[Vedi, *pp. 7-8*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)