def SWEstrapolazione(M_Target, M_Obs, b, ufr, alpha):
   """
   Interpola o estrapola i tassi per le maturità di interesse utilizzando l'algoritmo Smith-Wilson.

   Calcola i tassi per le scadenze specificate in `M_Target` utilizzando il vettore di calibrazione `b` ottenuto
   dai strumenti con scadenze osservate in `M_Obs`.

   Argomenti:
       M_Target: ndarray k x 1 che rappresenta ogni scadenza del titolo di interesse. Esempio: M_Target = np.array([[1], [2], [3], [5]])
       M_Obs: ndarray n x 1 che rappresenta le scadenze dei titoli osservate utilizzate per calibrare il vettore di calibrazione `b`. Esempio: M_Obs = np.array([[1], [3]])
       b: ndarray n x 1 che rappresenta il vettore di calibrazione calcolato sui titoli osservati.
       ufr: Numero decimale rappresentante il tasso forward definitivo. Esempio: ufr = 0.042
       alpha: Numero decimale rappresentante il parametro che guida la velocità di convergenza. Esempio: alpha = 0.05

   M_Target, M_Obs e b possono essere vettori colonna o vettori unidimensionali. Le scadenze in M_Target devono essere non negative.
   Per la scadenza 0 viene restituito il limite dei tassi quando la scadenza tende a 0.

   Ritorna:
       ndarray unidimensionale di lunghezza k che rappresenta i tassi desiderati per i titoli zero-coupon. Ogni tasso appartiene a un titolo
       zero-coupon con una scadenza da `M_Target`. Esempio: r = np.array([0.0024, 0.0029, 0.0034, 0.0039])

   Per ulteriori informazioni, consultare la documentazione su:
   https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
   """
   import numpy as np 
   from SWNucleo import SWNucleo as SWNucleo
   M_Target = np.ravel(M_Target).astype(float)
   M_Obs = np.ravel(M_Obs)
   b = np.ravel(b)
   if not np.all(M_Target >= 0): # rifiuta anche i NaN
       raise ValueError("Le scadenze in M_Target devono essere non negative")
   C = np.identity(M_Obs.size)
   d = np.exp(-np.log(1+ufr) * M_Obs)   # Calcola il vettore d descritto nel paragrafo 138
   Q = np.diag(d) @ C                   # Matrice Q descritta nel paragrafo 139
   H = SWNucleo(M_Target, M_Obs, alpha)  # Parte centrale della funzione Wilson dal paragrafo 132
   p = np.exp(-np.log(1+ufr)* M_Target) + np.diag(np.exp(-np.log(1+ufr) * M_Target)) @ H @ Q @ b # Funzione di sconto per le scadenze desiderate dal paragrafo 147
   tassi = np.empty(M_Target.size)
   positive = M_Target > 0
   tassi[positive] = p[positive] ** (-1/ M_Target[positive]) -1 # Converte i prezzi ottenuti in tassi
   # Per la scadenza 0 il tasso p(t)^(-1/t) - 1 non è definito: p(0) = 1 e -1/t è infinito. Il suo limite è exp(y(0)) - 1, dove
   # y(0) = ln(1+ufr) - alpha * (1 - exp(-alpha*M_Obs))' Q b è l'intensità a pronti per la scadenza 0
   y0 = np.log(1+ufr) - alpha * (1 - np.exp(-alpha * M_Obs)) @ Q @ b
   tassi[~positive] = np.exp(y0) - 1
   return tassi
