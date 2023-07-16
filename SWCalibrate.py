def SWCalibrate(r, M, ufr, alpha):
    """
    Calcola il vettore di calibrazione utilizzando l'algoritmo Smith-Wilson.

    Calcola il vettore di calibrazione `b` utilizzato per l'interpolazione ed estrapolazione dei tassi.

    Argomenti:
        r: ndarray n x 1 di tassi per i quali si desidera calibrare l'algoritmo. Ogni tasso appartiene a un titolo zero-coupon osservato con una scadenza nota. Esempio: r = np.array([[0.0024], [0.0034]])
        M: ndarray n x 1 di scadenze dei titoli che hanno tassi forniti in input `r`. Esempio: M = np.array([[1], [3]])
        ufr: Numero decimale rappresentante il tasso forward definitivo. Esempio: ufr = 0.042
        alpha: Numero decimale rappresentante il parametro che guida la velocità di convergenza. Esempio: alpha = 0.05

    Ritorna:
        ndarray n x 1 che rappresenta il vettore di calibrazione necessario per l'interpolazione ed estrapolazione. Esempio: b = np.array([[14], [-21]])

    Per ulteriori informazioni, consultare la documentazione su:
    https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
 """

    import numpy as np
    from SWHeart import SWHeart as SWHeart

    C = np.identity(M.size)
    p = (1+r) **(-M)  # Trasforma i tassi in prezzi di mercato impliciti di un titolo zero-coupon
    d = np.exp(-np.log(1+ufr) * M)     # Calcola il vettore d descritto nel paragrafo 138
    Q = np.diag(d) @ C                 # Matrice Q descritta nel paragrafo 139
    q = C.transpose() @ d                         # Vettore q descritto nel paragrafo 139
    H = SWHeart(M, M, alpha)  # Parte centrale della funzione Wilson dal paragrafo 132

    return np.linalg.inv(Q.transpose() @ H @ Q) @ (p-q)           # Vettore di calibrazione b dal paragrafo 149