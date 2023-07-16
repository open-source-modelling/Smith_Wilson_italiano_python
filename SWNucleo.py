def SWNucleo(u, v, alpha):
    """
    Calcola il nucleo della funzione Wilson.

    Calcola la matrice H (Nucleo della funzione Wilson) per le scadenze specificate dai vettori u e v.
    La formula è presa dal paragrafo 132 delle specifiche tecniche EIOPA.

    Argomenti:
        u: vettore n_1 x 1 delle scadenze. Esempio: u = [1, 3]
        v: vettore n_2 x 1 delle scadenze. Esempio: v = [1, 2, 3, 5]
        alpha: Numero decimale rappresentante il parametro che guida la velocità di convergenza. Esempio: alpha = 0.05

    Ritorna:
        matrice n_1 x n_2 che rappresenta il Nucleo della funzione Wilson per le scadenze selezionate e il parametro alpha.
        H è calcolato come descritto nel paragrafo 132 della documentazione EIOPA.

    Per ulteriori informazioni, consultare:
    https://www.eiopa.europa.eu/sites/default/files/risk_free_interest_rate/12092019-technical_documentation.pdf
    """
    
    import numpy as np
   
    u_Mat = np.tile(u, [v.size, 1]).transpose()
    v_Mat = np.tile(v, [u.size, 1])
    
    # Restituisce il nucleo della funzione Wilson dal paragrafo 132
    return 0.5 * (alpha * (u_Mat + v_Mat) + np.exp(-alpha * (u_Mat + v_Mat)) - alpha * np.absolute(u_Mat-v_Mat) - np.exp(-alpha * np.absolute(u_Mat-v_Mat)))