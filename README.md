# 🚗 Sistema de Simulación de Parqueaderos - Centro Comercial Supercentro

## 📋 Descripción del Proyecto

Este proyecto implementa una simulación de eventos discretos para analizar el sistema de pago de parqueaderos del Centro Comercial Supercentro.

El objetivo es determinar si los tres cajeros actuales son suficientes para atender la demanda de usuarios, utilizando modelos de colas M/M/1, análisis estadístico, verificación, calibración, validación y eliminación del estado transitorio.

La aplicación fue desarrollada en **Python** utilizando **Tkinter** para la interfaz gráfica y **Matplotlib** para la visualización de resultados.

---

## 🎯 Objetivos

* Simular el comportamiento de tres cajeros independientes.
* Analizar tiempos de espera y tiempos de atención.
* Identificar cuellos de botella.
* Determinar el estado estable del sistema.
* Realizar procesos de verificación, calibración y validación.
* Evaluar si la cantidad actual de cajeros es suficiente.
* Proponer estrategias de mejora basadas en evidencia estadística.

---

## 🏢 Contexto del Problema

El Centro Comercial Supercentro dispone de tres cajeros automáticos para el pago del parqueadero.

Cada cajero opera como un sistema M/M/1 independiente:

* Un servidor por cajero.
* Llegadas Poisson.
* Tiempos de servicio exponenciales.
* Disciplina FIFO.
* Sin cambio de fila.
* Sin deserción de usuarios.

---

## 👥 Tipos de Usuarios

| Tipo      | Tiempo Servicio (min) | Tiempo Llegadas (min) | Porcentaje |
| --------- | --------------------- | --------------------- | ---------- |
| Rápido    | 1                     | 3                     | 25%        |
| Normal    | 3                     | 3                     | 20%        |
| Lento     | 4                     | 5                     | 27.5%      |
| Muy Lento | 6                     | 7                     | 27.5%      |

### Tasas λ y μ

#### Usuario Rápido

* λ = 1/3 = 0.333
* μ = 1/1 = 1.000
* ρ = 0.333

#### Usuario Normal

* λ = 1/3 = 0.333
* μ = 1/3 = 0.333
* ρ = 1.000

#### Usuario Lento

* λ = 1/5 = 0.200
* μ = 1/4 = 0.250
* ρ = 0.800

#### Usuario Muy Lento

* λ = 1/7 = 0.143
* μ = 1/6 = 0.167
* ρ = 0.857

---

## 📚 Modelo Utilizado

Se implementó el modelo de colas **M/M/1**.

### Fórmulas Principales

Factor de utilización:

ρ = λ / μ

Número promedio de clientes en sistema:

L = ρ / (1 − ρ)

Número promedio en cola:

Lq = ρ² / (1 − ρ)

Tiempo promedio en sistema:

W = 1 / (μ − λ)

Tiempo promedio en cola:

Wq = ρ / (μ − λ)

Probabilidad de sistema vacío:

P₀ = 1 − ρ

---

## 🏗️ Arquitectura del Proyecto

```text
proyecto_parqueadero/
│
├── main.py
├── simulacion.py
├── graficos.py
├── recalculate.py
├── README.md
│
└── requirements.txt
```

### main.py

Responsable de:

* Interfaz gráfica Tkinter.
* Menú principal.
* Ejecución de simulaciones.
* Presentación de resultados.

### simulacion.py

Responsable de:

* Generación de llegadas.
* Generación de tiempos de servicio.
* Simulación de eventos discretos.
* Registro de métricas.

### graficos.py

Responsable de:

* Gráficos de estado estable.
* Histogramas.
* Boxplots.
* Comparaciones entre cajeros.
* Visualización de intervalos de confianza.

### recalculate.py

Responsable de:

* Eliminación del período transitorio.
* Promedios móviles.
* Recalcular estadísticas del estado estable.
* Determinar punto de calentamiento (warm-up).

---

## ⚙️ Tecnologías Utilizadas

* Python 3.11+
* Tkinter
* NumPy
* SciPy
* Pandas
* Matplotlib

---

Criterios utilizados:

| Métrica | Aceptable | Crítico |
| ------- | --------- | ------- |
| Wq      | < 3 min   | > 5 min |
| W       | < 5 min   | > 8 min |
| ρ       | 60%-85%   | >90%    |
| Lq      | < 3       | >5      |

## 📈 Gráficos Generados

La aplicación genera:

1. Evolución temporal del sistema.
2. Promedios móviles.
3. Detección de estado estable.

---

## 🔬 Verificación y Validación

### Proceso

```text
Definición del problema
          │
          ▼
Construcción del modelo
          │
          ▼
Verificación
          │
          ▼
Calibración
          │
          ▼
Validación
          │
          ▼
Resultados finales
```
---

## 🚀 Ejecución

Instalar dependencias:

```bash
pip install numpy scipy pandas matplotlib
```

Ejecutar aplicación:

```bash
python main.py
```

---

## 📌 Resultados Esperados

El sistema permitirá:

* Analizar el desempeño de los tres cajeros.
* Detectar congestión.
* Identificar períodos transitorios.
* Validar resultados contra teoría M/M/1.
* Determinar si tres cajeros son suficientes.

---

## 👨‍💻 Autor

Proyecto desarrollado para la actividad académica:
