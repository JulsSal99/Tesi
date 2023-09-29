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

Tempi di Pausa:
============
Riguardo ai periodi di pausa in un discorso:
- Nel testo di Pavese et al è stata analizzato il tempo di pausa e  professionisti è composto da 5 docenti universitari madre lingua inglesi della London South Bank University e 6 soggetti madre lingua italiani monitorati in stanze con diverse condizioni di riverberazione.
> "I risultati mostrano che la distribuzione dei periodi di pausa non varia nelle diverse camere; in particolare, il maggior numero di occorrenze si ha per periodi della durata pari a 90 ms. Viceversa, il tipo di camera influenza la durata dei periodi di voce.
Nel caso dei monitoraggi in camera anecoica (figura 1A), il maggior numero di occorrenze si ha per tratti di lunghezza pari a 90 ms; tale valore aumenta con la riverberazione della camera: il picco di occorrenze è a 120 ms per la camera semi riverberante (figura 1B) e a 150 ms per la camera riverberante (figura 1C)." [^p1]
> "per i non professionisti della voce [...] i picchi delle occorrenze medie si attestano a *60 ms per i tratti di pausa* e a *90 ms per la voce*." e "*50 ms per i tratti di pausa* e a *100 ms per la voce*." con un "periodo base dei due dispositivi, che è pari a 30 ms e 50 ms rispettivamente." [^p2]

Inoltre, riguardo ai riverberi:
> "la maggiore lunghezza della coda sonora potrebbe portare il parlatore “professionista” ad allungare i periodi di fonazione per migliorare l’intelligibilità del messaggio che deve trasmettere. ", ed è stato osservato che sussiste "un incremento della lunghezza media più occorrente dei periodi di voce in 18 insegnanti che parlavano in aule maggiormente riverberanti rispetto a 24 insegnanti che esercitavano la loro attività didattica in aule con tempi di riverberazione conformi ai requisiti acustici stabiliti per questi ambienti.".
"per i professionisti della voce il periodo più ricorrente è pari a 90 ms, mentre per i non professionisti è molto più corto, pari a 60 e 50 ms", "indice di un parlato molto veloce e probabilmente indipendente dalle caratteristiche acustiche dell’ambiente, ma dipendente invece dal modo di esporre un discorso nel caso di non professionista della voce. Infatti, il parlato di un insegnante potrebbe appartenere al “clear speech” che prevede un incremento della pause e un allungamento dei singoli segmenti di parlato" [^p3]

-

NOMENCLATURA FILES
============

| cartella      | LETTERA_SOGGETTO | _ | NUMERO_PORTAMENTO_VOCE_DISTANZA | _ | TIPO_CONGIUNZIONE | .wav |
| ------        | ---------------- | - | ------------------------------- | - | ----------------- | ---- |
| \dialoghi     | A                | _ | 1                               |   |                   | .wav |
|               | B                | _ | 2                               |   |                   | .wav |
|               |                  |   |                                 |   |                   |      |
| \congiunzioni | A                | _ | 1                               | _ | A                 | .wav |
|               | B                | _ | 2                               | _ | B                 | .wav |

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
[^1]:[Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). A simplest systematics for the organization of turn-taking for conversation. Language, 50, 696–735.]
[^2]:[Vedi Sacks et al., 1974, p. 700]
[^3]:[Jefferson, 1984, p. 8]
[^3]:[Vedi, "*Pauses, gaps and overlaps in conversations*" di
"*Mattias Heldner, Jens Edlund*", *2010*](DOC/1-s2.0-S0095447010000628-main.pdf)
[^4]:[Beattie & Barnard, 1979; Jaffe & Feldstein, 1970; Kendon, 1967]
[^5]:[Stivers, T., Enfield, N. J., Brown, P., Englert, C., Hayashi, M., Heinemann, T., et al. (2009). Universals and cultural variation in turn-taking in conversation. Proc. Natl. Acad. Sci. U.S.A. 106, 10587–10592. doi: 10.1073/pnas.09036 16106]
[^6]:[pp. 7](DOC/608110.pdf)
[^7]:["*The intersection of turn-taking and repair: the timing of other-initiations of repair in conversation*" di Kobin H. Kendrick](https://www.frontiersin.org/articles/10.3389/fpsyg.2015.00250/full)
[^8]:["*Competition Reduces Response Times in Multiparty Conversation*"](DOC/fpsyg-12-693124.pdf)
[^9]:[pp. 3, "*Overrated gaps: Inter-speaker gaps provide limited information about the timing of turns in conversation*"](DOC/1-s2.0-S0010027722000257-main.pdf)
[^10]:[Barthel, M., Sauppe, S., Levinson, S. C., & Meyer, A. S. (2016). "*The timing of utterance planning in task-oriented dialogue: Evidence from a novel list-completion paradigm*". Frontiers in Psychology, 7.](https://doi.org/10.3389/fpsyg.2016.01858)
[^11]:[The NXT-format Switchboard Corpus: a rich resource for investigating the syntax, semantics, pragmatics and prosody of dialogue](DOC/The_NXT_format_Switchboard_Corpus_a_rich_resource_for_investigating_the_syntax_semantics_pragmatics_and_prosody_of_dialogue.pdf)

[^p1]:[/////////////////////////Vedi, *pp. 3-4*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
[^p2]:[Vedi, *pp. 6-7*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
[^p3]:[Vedi, *pp. 7-8*, "*Durata dei periodi di voce e di pausa nel parlato continuo in diverse condizioni di riverberazione per professionisti e non professionisti della voce.*", *Lorenzo Pavese* e *Giuseppina Emma Puglisi*, *Giugno 2014*](DOC/aia2014_pavese_et_al.pdf)
