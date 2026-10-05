import numpy as np
import pytest
from SWCalibrazione import SWCalibrazione
from SWEstrapolazione import SWEstrapolazione

# Esempio dello strumento Excel di EIOPA, come in main.py
M_Obs = np.arange(1, 21)
r_Obs = np.array([0.0131074591432979, 0.0222629098372424, 0.0273403667327403, 0.0317884414257146, 0.0327205345299401, 0.0332867589595655, 0.0336112121443886, 0.0341947663149128, 0.0345165922380981, 0.0346854377006694, 0.0357173340791270, 0.0368501673784445, 0.0376263620230677, 0.0385237084707761, 0.0395043823351044, 0.0401574909803133, 0.0405715278625131, 0.0415574765441695, 0.0415582458410996, 0.0425511326946310])
ufr = 0.042
alpha = 0.142068
M_Target = np.arange(1, 66)
expected = np.array([0.0131074591433162, 0.0222629098372631, 0.0273403667327665, 0.0317884414257348, 0.0327205345299595, 0.0332867589595818, 0.0336112121444057, 0.0341947663149282, 0.0345165922381123, 0.0346854377006820, 0.0357173340791390, 0.0368501673784565, 0.0376263620230795, 0.0385237084707877, 0.0395043823351151, 0.0401574909803222, 0.0405715278625236, 0.0415574765441811, 0.0415582458411092, 0.0425511326946399, 0.0436656239235407, 0.0445561338093701, 0.0452628707713729, 0.0458188495571263, 0.0462512293260686, 0.0465823804152550, 0.0468307431055235, 0.0470115242330582, 0.0471372655651476, 0.0472183095640757, 0.0472631822720417, 0.0472789087725782, 0.0472712735066854, 0.0472450353102873, 0.0472041051721557, 0.0471516932406448, 0.0470904304327322, 0.0470224690500156, 0.0469495660338741, 0.0468731518591676, 0.0467943875455887, 0.0467142118366739, 0.0466333802421182, 0.0465524973460913, 0.0464720435419177, 0.0463923971530968, 0.0463138527348181, 0.0462366362129754, 0.0461609174043216, 0.0460868203676226, 0.0460144319580649, 0.0459438088931750, 0.0458749835854031, 0.0458079689527213, 0.0457427623823397, 0.0456793489926264, 0.0456177043135153, 0.0455577964851157, 0.0454995880572642, 0.0454430374586101, 0.0453881001922050, 0.0453347298048383, 0.0452828786693675, 0.0452324986125916, 0.0451835414157220])

def test_coincide_con_lo_strumento_excel_eiopa():
    b = SWCalibrazione(r_Obs, M_Obs, ufr, alpha)
    r_Target = SWEstrapolazione(M_Target, M_Obs, b, ufr, alpha)
    assert np.linalg.norm(r_Target - expected) < 1e-12

# Le docstring descrivono vettori colonna n x 1, che sollevavano un errore; ora funzionano entrambe le forme
def test_vettori_colonna_danno_lo_stesso_risultato():
    b_1d = SWCalibrazione(r_Obs, M_Obs, ufr, alpha)
    b_col = SWCalibrazione(r_Obs[:, np.newaxis], M_Obs[:, np.newaxis], ufr, alpha)
    assert np.allclose(b_col, b_1d)
    r_col = SWEstrapolazione(M_Target[:, np.newaxis], M_Obs[:, np.newaxis], b_col[:, np.newaxis], ufr, alpha)
    assert np.allclose(r_col, SWEstrapolazione(M_Target, M_Obs, b_1d, ufr, alpha))

# La scadenza 0 dava -100% o +inf, con un avviso di divisione per zero. Ora dà il limite dei tassi quando la scadenza tende a 0
@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("M, r, u, a", [(M_Obs, r_Obs, ufr, alpha),
                                        (np.array([1, 2, 4, 5, 6, 7]), np.array([0.01, 0.02, 0.03, 0.032, 0.035, 0.04]), 0.04, 0.15)])
def test_scadenza_zero_e_il_limite_delle_scadenze_brevi(M, r, u, a):
    b = SWCalibrazione(r, M, u, a)
    r_zero, r_breve = SWEstrapolazione(np.array([0, 1e-5]), M, b, u, a)
    assert r_zero == pytest.approx(r_breve, abs=1e-7)

# Una griglia che inizia dalla scadenza 0 dà gli stessi tassi di prima per le altre scadenze
def test_griglia_che_inizia_da_zero():
    b = SWCalibrazione(r_Obs, M_Obs, ufr, alpha)
    r_Target = SWEstrapolazione(np.arange(0, 66), M_Obs, b, ufr, alpha)
    assert np.linalg.norm(r_Target[1:] - expected) < 1e-12

# Le scadenze negative restituivano tassi senza senso senza alcun errore
@pytest.mark.parametrize("M_Target", [np.array([-1, 1]), np.array([1, np.nan])])
def test_scadenza_negativa_o_nan_solleva_errore(M_Target):
    b = SWCalibrazione(r_Obs, M_Obs, ufr, alpha)
    with pytest.raises(ValueError, match="non negative"):
        SWEstrapolazione(M_Target, M_Obs, b, ufr, alpha)
