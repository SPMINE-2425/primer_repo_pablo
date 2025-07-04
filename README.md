# Análisis y Modelado de Secuestros en Colombia

## Descripción  
Este repositorio contiene el código y los datos para un estudio exhaustivo de los secuestros en Colombia (1996–2025). Se parte de series de tiempo mensuales y anuales, se normalizan los conteos mediante tasas por 100 000 habitantes, se incorporan proxies de violencia armada (masacres, asesinatos selectivos, categorías de conflicto) y variables institucionales (CAIs, efectivos de policía). Finalmente, se comparan modelos de panel (Regresion con Efectos Fijos), machine learning (XGBoost) y deep learning (red neuronal) para predecir el número de secuestros, junto a interpretaciones SHAP para explicar sus resultados.



## Contenido del Repositorio

| File / Notebook | Proposito |
|-----------------|---------|
| **`1. Primer_analisis_exploratorio.ipynb`** | Un analisis de la base de secuestos en en solitario. Cuenta con Widgets interactivos y analisis por municipios y departamentos, tanto estadisticos como geoespaciales. |
| **`2. Analisis_compuesto.ipynb`** | En este script creamos la tasa de secuestros por 100k habitantes y incluimos varias variables para capturar la violencioa en el pais asi como la fuerza institucional. |
| **`3. Analisis Avanzado.ipynb`** | En este script usamos la base creada en scripts 1-2 y analizamos correlaciones, analisis mediante PCA asi como regresiones econometricas de Datos Panel y modelos de Machine y Deep Learning con XGBoost y PyTorch (cada modelo tiene una busqueda de hiperparametros). |
| **`construccion_bases_series.py`** | Este script contiene 4 funciones que se utilizan a lo largo del proyecto para limpiar y crear los datos en los formatos requeridos. |
| **`Datos.rar`** | Una carpeta con todas las bases que se usaron para realizar el proyecto, tanto tabulares como geoespaciales . |


## Hallazgos clave  
- **Ciclos históricos**: pico de secuestros entre 1998–2002 ligado a FARC y paramilitares, con posterior estabilización.  
- **Geografía oculta**: al normalizar por población emergen municipios de baja densidad (Llanos, sur) con tasas extremas (“pescas milagrosas”).  
- **Efecto disuasorio**: cada CAI adicional reduce ~0.8 secuestros/mes; la posdesmovilización también baja significativamente la incidencia.  
- **Modelos predictivos**:  
  - **PanelOLS** (R² Within ≈ 0.19) identifica coeficientes causales para variables de violencia e institucionales.  
  - **XGBoost** (R² ≈ 0.84, MAE ≈ 1.51) se entrena con 150 árboles y ofrece un excelente balance entre precisión y velocidad.  
  - **Red neuronal (PyTorch)** (R² ≈ 0.89) con 3 capas ocultas que maximizan el R2 demuestra un desempeño igualmente sobresaliente. Con GPU potente, ambos enfoques (ML y DL) entrenan rápidamente, si bien XGBoost parece cerca de su límite con los datos actuales, la red aún podría beneficiarse de búsquedas bayesianas de hiperparámetros.
- **SHAP**: la categoría “Levemente afectados y persistente” y la tasa por 100 000 hab. son las características más influyentes en la predicción de secuestros.


## Instalación

Para obtener el código y los datos en tu equipo, clona el repositorio y accede a la carpeta del proyecto:

```bash
git clone https://github.com/SPMINE-2425/primer_repo_pablo.git
cd primer_repo_pablo
```


## Licencia  
Este proyecto se distribuye bajo la licencia MIT
