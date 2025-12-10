#  Flappy Bird — Ingeniería de Características y Conclusiones de los Agentes entrenados con Q-Learning y Deep Q-Learning

##  Objetivo
Debido a que el entorno de Flappy Bird provee un estado continuo, 
fue necesario transformar estas observaciones en una representación **discretizada** para disminuir el espacio de estados.

---

##  Estado Crudo del Juego

| Variable | Descripción |
|---------|-------------|
| `player_y` | Posición vertical del pájaro |
| `player_vel` | Velocidad vertical del pájaro |
| `next_pipe_dist_to_player` | Distancia horizontal al siguiente tubo |
| `next_pipe_top_y` | Altura del borde superior del hueco |
| `next_pipe_bottom_y` | Altura del borde inferior del hueco |

Estado crudo = **5 valores continuos seleccionados del estado completo**
(*Estado completo = 8 valores*)
---

##  Ingeniería de Características (Discretización)

Como estas variables son continuas, se agrupan en **intervalos**.

Discretización implementada para cada variable:

| Variable | Sentido | Tipo de discretización |
|---------|------------|----------------------|
| `player_y` | Indica si el pájaro está muy arriba, centro o muy abajo | Se divide por *10* para agrupar rangos de altura en bins |
| `player_vel` | Importa la dirección del movimiento, no el valor exacto | Clasificada en categorías: <br>• Subiendo rápido <br>• Subiendo <br>• Estable <br>• Bajando <br>• Bajando rápido |
| `next_pipe_dist_to_player` | Indica urgencia; si falta mucho o está cerca el tubo | Se divide por *10* para agrupar rangos horizontales en bins |
| `next_pipe_top_y` / `next_pipe_bottom_y` | Representan dónde está el hueco | Se divide por *10* para agrupar rangos de altura en bins |


---

###  Representación Final del Estado  
Se utiliza una **tupla de índices discretizados**, (player_y_bin, player_vel_bin, dist_to_pipe_bin, top_pipe_y_bin, bot_pipe_y_bin)


Esto convierte el entorno continuo en un espacio de estados **finito y explotable** por la Q-Table.

---
## Entrenamiento y evaluación 
Se generó la Q-table en base a 20000 episodios y se evaluaron ambos agentes durante 100 episodios, bajo dos tipos de discretización: baja (dividiendo las variables espaciales del estado por 10) y alta (dividiéndolas por 25).

## Visualización de evolución de métricas durante el entrenamiento

### Q-Learning
Gráfico de recompensas por episodio durante el entrenamiento del agente Q-Learning:  
![Discretización baja Q-Learning](Recompensa_10.jpg)
![Discretización alta Q-Learning](Recompensa_25.jpg)
### Red Neuronal (DQN)
Gráficos de la métrica de pérdida (loss) y MAE durante el entrenamiento de la red neuronal:  
![Discretización baja Q-Learning](loss_10.jpg)
![Discretización baja Q-Learning](mae_10.jpg)
![Discretización alta Q-Learning](loss_25.jpg)
![Discretización alta Q-Learning](mae_25.jpg)

Observamos que la Q-table aprende más rápido con un espacio de estados menor y alcanza recompensas promedio más altas. Con la discretización baja necesita más episodios para alcanzar valores de recompensas promedio más altos y estables.

## Comparación de resultados

Episodios de entrenamiento Q-table: 20000

| Agente / Método       | Recompensa promedio (baja discretización) | Recompensa promedio (alta discretización) |
|-----------------------|------------------------------------------|-------------------------------------------|
| Q-Learning (Q-table)  | 31                                       | 7                                        |
| Red Neuronal (DQN)    | 16                                       | 35                                        |

Episodios de entrenamiento Q-table: ...

| Agente / Método       | Recompensa promedio (baja discretización) |
|-----------------------|------------------------------------------|
| Q-Learning (Q-table)  |                                        |
| Red Neuronal (DQN)    |                                       | 

Observamos que  el agente basado en Q-Learning logró un mejor desempeño promedio en comparación con el agente basado en red neuronal en este experimento. Esto puede deberse a que la discretización de estados simplifica el espacio de decisión y permite un aprendizaje más eficiente en un entorno relativamente simple como Flappy Bird. Por otro lado, la red neuronal, aunque más flexible y capaz de generalizar, puede requerir más entrenamiento y ajuste de hiperparámetros para alcanzar un rendimiento comparable.

## Comentarios finales

- La Q-table demostró ser efectiva para este juego debido al bajo número de variables discretizadas, teniendo un mejor desempeño con la discretización baja para las variables espaciales. Demostró una mejora significativa de rendimiento al aumentar el número de episodios de entrenamiento.
- La red neuronal demostró ser más efectiva que la Q-table ante la discretización alta, en la cual las recompensas promedio por episodios durante el entrenamiento alcanzó valores altos pero con mucho ruido, teniendo la red neuronal una mejor capacidad de generalización.
- Aunque utilizar discretizaciones distintas entre la Q-table y la red neuronal no es conceptualmente correcto (porque ambas aprenden sobre espacios de estados diferentes), en la práctica los buenos resultados obtenidos por el agente con red neuronal se explican por su capacidad para generalizar y aproximar mejor la salida cuando el espacio de estados es más fino.
Mientras la Q-table logra aprender relaciones útiles entre las variables aun con una representación más gruesa del entorno, la red neuronal se beneficia de contar con una mayor cantidad de estados (producto de la discretización baja), lo cual le permite alcanzar un desempeño superior al observado con discretización alta.


