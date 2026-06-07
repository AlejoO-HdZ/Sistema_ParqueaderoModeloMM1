import matplotlib.pyplot as plt
import numpy as np
from simulacion import estado_estable
from tkinter import messagebox, scrolledtext


# ---------------------------
# SUAVIZADO VISUAL
# ---------------------------
def suavizar(x, w=10):
    return np.convolve(x, np.ones(w)/w, mode='valid')


# ---------------------------
# PUNTOS DE CORTE
# ---------------------------
def graficar_puntos(cajeros):

    fig, ax = plt.subplots(1, 3, figsize=(16, 5))

    for i, c in enumerate(cajeros):

        corte, mov = estado_estable(c["tiempos"])

        tiempos = c["tiempos"]

        # Serie original
        ax[i].plot(
            tiempos,
            alpha=0.5,
            color="steelblue",
            label="Serie original"
        )

        # Serie suavizada
        ax[i].plot(
            range(len(mov)),
            mov,
            color="orange",
            linewidth=2,
            label="Serie suavizada"
        )

        # Línea de corte
        ax[i].axvline(
            corte,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Corte estado estable (t*={corte:.2f})"
        )

        # 🔥 Sombreado antes del corte
        ax[i].axvspan(
            0,
            corte,
            color="gray",
            alpha=0.15,
            label="Transitorio"
        )

        # Punto exacto del corte
        ax[i].scatter(
            [corte],
            [mov[int(min(corte, len(mov)-1))]],
            color="red",
            s=60,
            zorder=5
        )

        # Texto técnico
        ax[i].text(
            corte,
            max(tiempos) * 0.9,
            f"t* = {corte:.2f}",
            color="red",
            rotation=90,
            ha="right",
            fontweight="bold"
        )

        ax[i].set_title(c["nombre"])
        ax[i].set_xlabel("Tiempo")
        ax[i].set_ylabel("Valor")
        ax[i].grid(True, alpha=0.3)

        ax[i].legend(fontsize=9)

    plt.tight_layout()
    plt.show()


# ---------------------------
# TRANSITORIO vs ESTABLE
# ---------------------------
def graficar_transicion(cajeros):

    fig = plt.figure(figsize=(15, 8))

    # ==================================================
    # 3 GRÁFICOS SUPERIORES (uno por cajero)
    # ==================================================

    utilizaciones = []
    Ws = []
    Wqs = []
    Lqs = []
    ProbEspera = []

    for i, c in enumerate(cajeros):

        ax = plt.subplot2grid((2, 3), (0, i))

        corte, _ = estado_estable(c["tiempos"])

        trans = suavizar(c["tiempos"][:corte])
        est = suavizar(c["tiempos"][corte:])

        ax.plot(
            range(len(trans)),
            trans,
            color="red",
            label="Transitorio"
        )

        ax.plot(
            range(len(trans), len(trans)+len(est)),
            est,
            color="green",
            label="Estable"
        )

        ax.axvline(
            len(trans),
            color="black",
            linestyle="--",
            label=f"Corte={corte}"
        )

        ax.set_title(c["nombre"])
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

        # ------------------------------------
        # métricas para recomendación final
        # ------------------------------------

        tiempos = np.array(c["tiempos"])

        W = np.mean(tiempos)
        Wq = max(0, W - 1)
        rho = np.mean(tiempos) / np.max(tiempos)
        Lq = Wq * 0.5
        prob_espera = np.mean(tiempos > 5)

        utilizaciones.append(rho)
        Ws.append(W)
        Wqs.append(Wq)
        Lqs.append(Lq)
        ProbEspera.append(prob_espera)

    # ==================================================
    # GRÁFICO INFERIOR FACTOR UTILIZACIÓN GLOBAL SUAVIZADO
    # ==================================================

    ax4 = plt.subplot2grid((2, 3), (1, 0), colspan=3)

    rho_global = np.array(utilizaciones)
    media_rho = np.mean(rho_global)
    x = np.arange(1, len(rho_global)+1)

    # Colores más suaves
    ax4.plot(
        x,
        rho_global,
        marker="o",
        linewidth=2,
        color="#a29bfe",
        label="ρ por cajero"
    )

    ax4.axhline(
        media_rho,
        color="#55efc4",
        linestyle="--",
        linewidth=2,
        label=f"ρ promedio = {media_rho:.3f}"
    )

    # Suavizado tipo curva usando polinomio de grado 3
    if len(x) > 1:
        z = np.polyfit(x, rho_global, 3)
        p = np.poly1d(z)
        x_smooth = np.linspace(x[0], x[-1], 100)
        ax4.plot(
            x_smooth,
            p(x_smooth),
            linestyle=":",
            linewidth=2,
            color="#ffeaa7",
            label="Tendencia suavizada"
        )

    # IC95%
    if len(rho_global) > 1:
        std = np.std(rho_global, ddof=1)
        ic = 1.96 * (std / np.sqrt(len(rho_global)))
        ax4.fill_between(
            x,
            media_rho - ic,
            media_rho + ic,
            color="#dfe6e9",
            alpha=0.3,
            label="IC95%"
        )

    # ==========================
    # LEYENDA DE MÉTRICAS
    # ==========================

    texto_metricas = (
        f"Wq = {np.mean(Wqs):.2f} min\n"
        f"W = {np.mean(Ws):.2f} min\n"
        f"ρ = {media_rho:.2f}\n"
        f"Lq = {np.mean(Lqs):.2f}\n"
        f"P(espera>5min) = {np.mean(ProbEspera)*100:.1f}%"
    )

    ax4.text(
        1.02,
        0.5,
        texto_metricas,
        transform=ax4.transAxes,
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.9)
    )

    ax4.set_title(
        "Factor de Utilización Global del Sistema"
    )

    ax4.set_xlabel("Cajero")
    ax4.set_ylabel("ρ")
    ax4.legend()
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    # ==================================================
    # RECOMENDACIÓN AUTOMÁTICA
    # ==================================================

    Wq_prom = np.mean(Wqs)
    W_prom = np.mean(Ws)
    rho_prom = media_rho
    Lq_prom = np.mean(Lqs)
    P_prom = np.mean(ProbEspera)

    recomendacion = "🟢 SISTEMA ADECUADO\nNo se recomienda agregar cajeros."

    if (
            Wq_prom > 5 or
            W_prom > 8 or
            rho_prom > 0.90 or
            Lq_prom > 5 or
            P_prom > 0.20
    ):
        recomendacion = (
            "🔴 RECOMENDACIÓN FINAL\n\n"
            "Agregar al menos un cajero adicional.\n"
            "Se excedieron uno o más criterios críticos."
        )

    elif (
            Wq_prom > 3 or
            W_prom > 5 or
            rho_prom > 0.85
    ):
        recomendacion = (
            "🟡 RECOMENDACIÓN FINAL\n\n"
            "Sistema cercano al límite.\n"
            "Se recomienda monitoreo continuo."
        )

    messagebox.showinfo(
        "Resultado Final del Análisis",
        f"""
Tiempo promedio en cola (Wq): {Wq_prom:.2f}
Tiempo promedio sistema (W): {W_prom:.2f}
Utilización promedio (ρ): {rho_prom:.2f}
Longitud promedio cola (Lq): {Lq_prom:.2f}
Probabilidad espera >5 min: {P_prom*100:.1f}%

{recomendacion}
"""
    )
    plt.tight_layout()
    plt.show()


# ---------------------------
# TODAS LAS MÉTRICAS
# ---------------------------
def graficar_todo(cajeros):

    fig, ax = plt.subplots(3, 2, figsize=(14, 12))

    medias = [c["metricas"]["media"] for c in cajeros]

    # tiempos
    for c in cajeros:
        ax[0,0].plot(c["tiempos"], label=c["nombre"])
    ax[0,0].set_title("Tiempos por cajero")
    ax[0,0].legend()

    # IC
    ax[0,1].bar([c["nombre"] for c in cajeros], medias, color="skyblue")
    ax[0,1].set_title("Promedios")

    # rápido lento
    r = np.argmin(medias)
    l = np.argmax(medias)

    ax[1,0].bar(
        [f"Cajero {r+1}", f"Cajero {l+1}"],
        [medias[r], medias[l]],
        color=["green", "red"]
    )
    ax[1,0].set_title("Extremos")

    # usuarios
    tipos = list(cajeros[0]["conteo"].keys())
    total = np.sum([list(c["conteo"].values()) for c in cajeros], axis=0)

    ax[1,1].bar(tipos, total)
    ax[1,1].set_title("Usuarios")

    # por tipo
    for c in cajeros:
        ax[2,0].plot(list(c["conteo"].values()), label=c["nombre"])
    ax[2,0].legend()

    # recomendación placeholder
    # ---------------------------
    # PROMEDIO USUARIOS POR TIPO
    # ---------------------------
    tipos = list(cajeros[0]["conteo"].keys())

    promedios = []
    for t in tipos:
        total = sum(c["conteo"].get(t, 0) for c in cajeros)
        promedios.append(total / 3)

    ax[2,1].bar(tipos, promedios, color=["green","blue","orange","red"])
    ax[2,1].set_title("Promedio usuarios por tipo (3 cajeros)")
    ax[2,1].set_ylabel("Promedio atendido")
    ax[2,1].grid(alpha=0.3)
    plt.tight_layout()
    plt.show()