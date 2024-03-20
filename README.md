# Albums : Sharing Photo's website
![logo](/images/logo.png)

Albums è un sito web per la pubblicazione di immagini valutate dall'utenza.

L'obiettivo di questo progetto e creare una cerchia ristretta e moderata per la pubblicazione dei propri scatti.
Lo sviluppo è stato principalmente fatto in **Django** un framework server-side, con la possibilità di utilizzare i *templates*,
la parte html che supporta il backend di django, in modo da sviluppare anche la parte client-side.

Si è presa ispirazione per l'html e di una piccola parte di codice (lo sviluppo degli item e del browse) dalla repo : https://github.com/SteinOveHelset/puddle

# Implementazione del sito

Questa è la homepage del sito dove vengono mostrate le immagini piu recenti, e la navigation bar

![homepage](/images/homepage.png)

## Metodo di registrazione 

Sono presente vari campi, tutti obbligatori per registrarsi all'interno della nostra applicazione.

![signup](/images/signup.png)


## Immagini Recenti e in Relazione

Le immagini recenti viste dall'utente durante la sua sessione

![recently](/images/recently_viewed.png)


Immagini in relazione con l'oggetto visualizzato al momento della stessa categoria

![related](/images/related_items.png)

## Rating

Presente la funzione di rating per ogni post pubblicato nel sito.

![Rating](/images/detailitem_rating.png)


## Face Detection

Nel sito non è possibile pubblicare immagini contenente dei volti.

![facedetect](/images/filesystem_facedetection.png)

Verreno avvisati con un messaggio di warning

![warning_face](/images/warning_facedetected.png)



## Profile

Ogni utente è dotato di una pagina profilo con i suoi scatti pubblicati.

![profile](/images/profile.png)

## E molto altro..

Nel codice sono state utilizzate varie funzioni, dalla generazione del JWT token alla gestione delle pagine HTML, lo storing delle immagini e molto altro.
Il *progetto* django è stato suddiviso in 3 principali *applicazioni* :
- Core
- Item
- Visuals


# Conclusione

In conclusione, il progetto sviluppato rappresenta un’eccitante fusione di
complessità e semplicità nell’implementazione di un sito web utilizzando il
framework Django. Attraverso la scelta intuitiva.. [continua a leggere..](Ingegneria_S_D_albums.pdf)



