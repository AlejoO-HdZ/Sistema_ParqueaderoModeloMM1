import numpy as np
from scipy import stats
from recalculate import *

usuarios = {
    'rapido': {'servicio': 1, 'llegada': 3, 'prob': 0.25},
    'normal': {'servicio': 3, 'llegada': 3, 'prob': 0.20},
    'lento': {'servicio': 4, 'llegada': 5, 'prob': 0.275},
    'muy_lento': {'servicio': 6, 'llegada': 7, 'prob': 0.275}
}

tipos = list(usuarios.keys())
probs = [usuarios[t]['prob'] for t in tipos]


def generar_usuario():
    return np.random.choice(tipos, p=probs)


def simular_cajero(tiempo_total, log_callback=None):

    t = 0
    cola = 0

    tiempos = []
    espera = []
    usuarios_local = []
    conteo = {}

    while t < tiempo_total:

        u = generar_usuario()
        usuarios_local.append(u)
        conteo[u] = conteo.get(u, 0) + 1

        servicio = np.random.exponential(usuarios[u]['servicio'])
        llegada = np.random.exponential(usuarios[u]['llegada'])

        t += llegada

        w = max(0, cola)
        cola = max(0, cola + servicio - llegada)

        tiempos.append(w + servicio)
        espera.append(w)

        if log_callback:
            log_callback(u, servicio, w, t)

    return tiempos, espera, usuarios_local, conteo
# ---------------------------
# MÉTRICAS
# ---------------------------
def metricas(tiempos):

    media = np.mean(tiempos)
    std = np.std(tiempos, ddof=1)

    n = len(tiempos)
    tcrit = stats.t.ppf(0.975, n-1)
    err = tcrit * (std / np.sqrt(n))
    return {
        "media": media,
        "std": std,
        "min": np.min(tiempos),
        "max": np.max(tiempos),
        "ic95": (media - err, media + err)
    }
# ---------------------------
# ESTADO ESTABLE
# ---------------------------
def estado_estable(datos, ventana=40):

    mov = np.convolve(datos, np.ones(ventana)/ventana, mode='valid')
    var = np.array([np.var(mov[i:i+ventana]) for i in range(len(mov)-ventana)])

    corte = np.argmin(var) + ventana
    return corte, mov
# ---------------------------
# VALIDACIÓN TEÓRICA M/M/1
# ---------------------------
def validar_mm1(lmbda, mu):

    rho = lmbda / mu

    W_teo = 1 / (mu - lmbda)
    Wq_teo = rho / (mu - lmbda)
    Lq_teo = (lmbda**2) / (mu * (mu - lmbda))

    return rho, W_teo, Wq_teo, Lq_teo


# ---------------------------
# RECOMENDACIÓN
# ---------------------------
def recomendacion(Wq, W, rho, Lq):

    if Wq > 5 or W > 8 or rho > 0.9 or Lq > 5:
        return "🔴 RECOMENDACIÓN: AGREGAR CAJERO"
    elif Wq > 3 or W > 5 or rho > 0.85:
        return "🟡 SISTEMA EN LÍMITE: MONITOREAR"
    else:
        return "🟢 SISTEMA ESTABLE: NO ES NECESARIO AGREGAR"