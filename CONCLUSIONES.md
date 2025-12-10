#  Flappy Bird — Ingeniería de Características y Conclusiones del Agente Q-Learning

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
## Visualización de evolución de métricas durante el entrenamiento

### Q-Learning
Gráfico de recompensas por episodio durante el entrenamiento del agente Q-Learning:  

### Red Neuronal (DQN)
Gráficos de la métrica de pérdida (loss) y MAE durante el entrenamiento de la red neuronal:  


## Comparación de resultados

Se entrenaron y evaluaron ambos agentes durante 100 episodios:

| Agente                | Recompensa promedio |
|-----------------------|------------------|
| Q-Learning (Q-table)  | 31               |
| Red Neuronal (DQN)    | 16               |

Observamos que el agente basado en Q-Learning logró un mejor desempeño promedio en comparación con el agente basado en red neuronal en este experimento. Esto puede deberse a que la discretización de estados simplifica el espacio de decisión y permite un aprendizaje más eficiente en un entorno relativamente simple como Flappy Bird. Por otro lado, la red neuronal, aunque más flexible y capaz de generalizar, puede requerir más entrenamiento y ajuste de hiperparámetros para alcanzar un rendimiento comparable.

## Comentarios finales

- La Q-table demostró ser efectiva para este juego debido al bajo número de variables discretizadas.  
- La red neuronal tiene potencial para problemas con espacios de estado más complejos o continuos, aunque en este caso no superó a la aproximación tabular.  
- La discretización es **clave** para que Q-Learning sea viable en Flappy Bird
