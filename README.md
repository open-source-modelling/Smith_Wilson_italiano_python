<h1 align="center" style="border-botom: none">
  <b>
    🐍 Algoritmo Smith & Wilson 🐍     
  </b>
</h1>

</br>

L'algoritmo Smith & Wilson è un algoritmo ampiamente utilizzato che consente di interpolare ed estrapolare curve di rendimento di strumenti finanziari come titoli di stato e tassi privi di rischio. 

Questa implementazione si basa sulla [documentazione tecnica](https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf)  della metodologia per derivare la struttura a termine dei tassi di interesse privi di rischio di EIOPA.

Il link fa riferimento alla versione pubblicata il 12/09/2019. Consultare la sezione 7.

## Problema

Nell'analisi delle aspettative di mercato sui tassi futuri, un approccio comune è quello di esaminare strumenti finanziari a tasso fisso come titoli di stato o obbligazioni aziendali che maturano in futuro. Nell mercato, le scadenze a disposizione (e liquide) sul mercato coprono raramente tutte le scadenze necessarie.

## Soluzione

Questa implementazione richiede in input le <b>informazioni di mercato disponibili</b>, i <b>parametri</b> che descrivono il comportamento a lungo termine della curva e i dati sulle <b>scadenze desiderate</b> per le quali sono necessari i rendimenti.

### Informazioni di mercato disponibili

- Rendimento osservato dei titoli di stato zero-coupon (ZCB)
- Scadenza dei ZCB osservati

### Parametri

- Il tasso forward definitivo `ufr`` rappresenta il tasso al quale la curva dei tassi converge all'aumentare del tempo
- Il parametro che controlla la velocità di convergenza. α controlla la velocità con cui la curva converge verso il parametro `ufr`` a partire dall'ultimo punto liquido (l'ultimo dato disponibile nelle informazioni di mercato)

### Output desiderato

- Elenco delle scadenze per le quali l'algoritmo SW calcolerà i rendimentis

Questa implementazione presupponga che i rendimenti siano calcolati sui ZCB. Questa assunzione può essere facilmente rilassata nelle versioni future.

L'implementazione è divisa in due parti:

- Le informazioni di mercato disponibili e i parametri vengono utilizzati per "calibrare" l'algoritmo. Ciò restituisce un vettore di calibrazione che può essere utilizzato per interpolare o estrapolare le scadenze desiderate. Questo viene fatto calibrando le funzioni kernel. Consultare la funzione `SWCalibrazione()``.

- I rendimenti per i ZCB con le scadenze desiderate vengono interpolati/estrapolati. Consultare la funzione `SWEstrapolazione()``.

Questo rilascio cerca di essere coerente con le specifiche tecniche di EIOPA.

## Guida introduttiva
Nell mercato osserviamo 6 instrumenti ZCB con scadenze di 1, 2, 4, 5, 6 e 7 anni, con rendimenti osservati rispettivamente di 1%, 2%, 3%, 3,2%, 3,5% e 4%. L'utente è interessato ai rendimenti per i ZCB con scadenze di 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15 e 20 anni. La calibrazione fornita per il parametro alpha è 0,15 e il tasso forward definitivo è 4%.

```bash
import numpy as np
from SWCalibrazione import SWCalibrazione as SWCalibrazione
from SWEstrapolazione import SWEstrapolazione as SWEstrapolazione

# Rendimenti osservati sul mercato
r_Obs = np.transpose(np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04])) 

# Scadenze dei titoli osservati sul mercato
M_Obs = np.transpose(np.array([1, 2, 4, 5, 6, 7]))  

# Tasso forward definitivo
ufr = 0.04 

# Parametro di velocità di convergenza
alpha = 0.15 

# Scadenze desiderate per l'interpolazione/estrapolazione
M_Target = np.transpose(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20])) 

# Calcolo del vettore di calibrazione
b = SWCalibrazione(r_Obs,M_Obs, ufr, alpha) 

# Calcolo dei rendimenti desiderati
r_Target = SWEstrapolazione(M_Target,M_Obs, b, ufr, alpha)

# Visualizzazione dei rendimenti desiderati
print("The interpolated/extrapolated rates are:") 
print(r_Target)
```

## Piu informazioni sull'esempio in main.py
Il'file main.py contiene un esempio tratto dallo dalla implementazione in Excel di EIOPA (Smith-Wilson Risk-Free Interest Rate Extrapolation Tool 27102015.xlsb). In questo esempio, i rendimenti sono disponibili per ZCB che maturano in 1 anno, 2 anni, ..., 20 anni. L'output desiderato è la curva fino a 65 anni.

### Nota:
Per estrapolare la curva, è sufficiente conoscere i parametri aggiuntivi (`alpha` e `ufr`), le scadenze utilizzate per la calibrazione e il vettore `b*Q`. 

In tal caso, non è difficile modificare la funzione `SWEstrapolazione()` in modo da accettare come input `Q*b` invece di `b`. Un esempio di tale implementazione può essere visualizato in questo [Jupyter Notebook](https://github.com/open-source-modelling/EIOPA_smith_wilson_test) (in inglese) 

Un esempio di questo formato è il tasso privo di rischio mensile pubblicato dall'Autorità europea per l'assicurazione e la previdenza professionale [sito EIOPA ufficiale](https://www.eiopa.europa.eu/tools-and-data/)


To extrapolate the curve, it is enough to know the additional parameters (alpha and ufr), the maturities used for calibration and the vector b*Q. If this is the case, it is not difficult to modify the function `SWEstrapolazione()` to take as input Qb instead of b. An example of such an implementation can be seen in this Jupyter Notebook https://github.com/open-source-modelling/EIOPA_smith_wilson_test. An example of this format is the monthly risk free rate published by the European Insurance and Occupational Pensions Authority 

</br>

Se avete suggerimenti per migliorare il codice, i commenti, ecc., vi preghiamo di farcelo sapere, scrivendo una mail a gregor@osmodelling.com
