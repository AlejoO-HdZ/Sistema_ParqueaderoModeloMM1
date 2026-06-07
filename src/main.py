import tkinter as tk
from tkinter import messagebox, scrolledtext
from threading import Thread
from simulacion import *
import graficos as g
from recalculate import *
# ---------------------------
# Variables globales
# ---------------------------
cajeros = [None, None, None]
logs = [None, None, None]

# ---------------------------
# Función de log
# ---------------------------
def log(i, msg):
    if logs[i] is not None:
        logs[i].after(0, lambda: logs[i].insert(tk.END, msg + "\n"))
        logs[i].after(0, lambda: logs[i].see(tk.END))

# ---------------------------
# SIMULACIÓN CON RÉPLICAS
# ---------------------------
def simular(i, tiempo_total, reps=30):
    """
    Simula un cajero 'reps' veces y acumula los tiempos
    """
    tiempos_totales = []
    conteo_final = {}

    for r in range(reps):
        t, e, u, c = simular_cajero(
            tiempo_total,
            log_callback=lambda u, s, w, t_: log(i, f"Réplica {r+1}: {u} s:{s:.2f} w:{w:.2f}")
        )
        tiempos_totales.extend(t)
        conteo_final = c  # último conteo

    met = metricas(tiempos_totales)

    cajeros[i] = {
        "tiempos": tiempos_totales,
        "metricas": met,
        "nombre": f"Cajero {i+1}",
        "conteo": conteo_final
    }

    log(i, f"\nMEDIA {met['media']:.2f}")
    log(i, f"IC95 {met['ic95']}")

# ---------------------------
# EJECUTAR SIMULACIÓN
# ---------------------------
def ejecutar():
    tiempo = int(entry.get())

    try:
        reps_val = int(entry_reps.get())
    except:
        reps_val = 30  # valor por defecto

    msg = f"""
SIMULACIÓN M/M/1

3 CAJEROS INDEPENDIENTES

Distribución:
- Rápido 25%
- Normal 20%
- Lento 27.5%
- Muy lento 27.5%

Tiempo: {tiempo} min
Réplica(s): {reps_val}

¿Continuar?
"""
    if not messagebox.askokcancel("Confirmación", msg):
        return

    for i in range(3):
        logs[i].delete("1.0", tk.END)
        Thread(target=simular, args=(i, tiempo, reps_val), daemon=True).start()

# ---------------------------
# ESTABLE + VALIDACIÓN
# ---------------------------
def estable():
    try:
        r = [c["metricas"]["media"] for c in cajeros]
        # Obtiene valores teóricos para M/M/1
        rho, W, Wq, Lq = validar_mm1(1/3, 1/2)
        rec = recomendacion(Wq, W, rho, Lq)

        msg = f"""
VALIDACIÓN / CALIBRACIÓN M/M/1
ρ = {rho:.3f}
W = {W:.3f}
Wq = {Wq:.3f}
Lq = {Lq:.3f}
{rec}

Se ejecutará nuevamente simulación en estado estable con los parámetros validados.
"""
        ok = messagebox.askokcancel("Validación", msg)
        if not ok:
            return
        # 🔥 RE-SIMULACIÓN ESTABLE
        for i in range(3):
            logs[i].delete("1.0", tk.END)
            Thread(target=simular, args=(i, 500, 30), daemon=True).start()
    except:
        messagebox.showerror("Error", "Ejecute simulación primero")

# ---------------------------
# BOTONES GRÁFICOS
# ---------------------------
def puntos(): g.graficar_puntos(cajeros)
def graficas(): g.graficar_todo(cajeros)
def trans(): g.graficar_transicion(cajeros)

# ---------------------------
# GUI
# ---------------------------
root = tk.Tk()
root.title("Modelo MM1 - Sistema de Pago CC SuperCentro")

frame = tk.Frame(root)
frame.pack()

for i in range(3):
    f = tk.LabelFrame(frame, text=f"Cajero {i+1}")
    f.pack(side="left")

    t = scrolledtext.ScrolledText(f, width=35, height=25)
    t.pack()
    logs[i] = t

bottom = tk.Frame(root)
bottom.pack()

entry = tk.Entry(bottom)
entry.insert(0, "500")  # tiempo por defecto
entry.pack(side="left")

# NUEVO ENTRY PARA RÉPLICAS
entry_reps = tk.Entry(bottom)
entry_reps.insert(0, "30")  # replicas por defecto
entry_reps.pack(side="left")

tk.Button(bottom, text="Simular", command=ejecutar).pack(side="left")
tk.Button(bottom, text="Puntos corte", command=puntos).pack(side="left")
tk.Button(bottom, text="Gráficas", command=graficas).pack(side="left")
tk.Button(bottom, text="Transición", command=trans).pack(side="left")
tk.Button(bottom, text="Simulación estable + validación", command=estable).pack(side="left")

root.mainloop()