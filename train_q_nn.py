import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
#pip install tensorflow


# --- Cargar Q-table entrenada ---
QTABLE_PATH = 'flappy_birds_q_table.pkl' 
with open(QTABLE_PATH, 'rb') as f:
    q_table = pickle.load(f)

# --- Preparar datos para entrenamiento ---
# Convertir la Q-table en X (estados) e y (valores Q para cada acción)
X = []  # Estados discretos
y = []  # Q-values para cada acción
zero_count=0
for state, q_values in q_table.items():
    if max(q_values) == 0:
        zero_count+=1
        continue
    X.append(state)
    y.append(q_values)

X = np.array(X)   # shape (n_states, n_features)
y = np.array(y)   # shape (n_states, n_actions)


n_features = X.shape[1]
n_actions = y.shape[1]

# --- Definir la red neuronal ---
model = Sequential([
    Dense(64, activation='relu', input_shape=(n_features,)),
    Dense(64, activation='relu'),
    Dense(n_actions, activation='linear')  # salida: Q para cada acción
])


model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entrenamiento red neuronal
history = model.fit(X, y,
                    epochs=50, batch_size=64, verbose=2)


# --- Mostrar resultados del entrenamiento ---
loss, mae = model.evaluate(X, y, verbose=0)
print(f"Test MSE: {loss:.4f}, Test MAE: {mae:.4f}") ## CONSULTAR CON QUE METRICA EVALUAR EL ENTRENAMIENTO

# --- Guardar el modelo entrenado ---
#model.save('flappy_q_nn_model.h5')
#print('Modelo guardado como TensorFlow SavedModel en flappy_q_nn_model/')
model.save('flappy_q_nn_model.keras', include_optimizer=False, save_format='keras')
print("Modelo guardado correctamente en flappy_q_nn_model.keras")

# --- Notas para los alumnos ---
# - Puedes modificar la arquitectura de la red y los hiperparámetros.
# - Puedes usar la red entrenada para aproximar la Q-table y luego usarla en un agente tipo DQN.
# - Si tu estado es una tupla de enteros, no hace falta normalizar, pero puedes probarlo.
# - Si tienes dudas sobre cómo usar el modelo para predecir acciones, consulta la documentación de Keras.
