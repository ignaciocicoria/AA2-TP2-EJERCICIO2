import numpy as np
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt

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
                    epochs=80, batch_size=64, verbose=2)


# --- Mostrar resultados del entrenamiento ---
loss, mae = model.evaluate(X, y, verbose=0)
print(f"Test MSE: {loss:.4f}, Test MAE: {mae:.4f}") 

# --- Gráfico evolución del Loss (MSE) ---
plt.figure()
plt.plot(history.history['loss'])
plt.title('Evolución del Loss (MSE)')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.grid(True)
plt.show()

# --- Gráfico evolución del MAE ---
plt.figure()
plt.plot(history.history['mae'])
plt.title('Evolución del MAE')
plt.xlabel('Épocas')
plt.ylabel('MAE')
plt.grid(True)
plt.show()
# --- Guardar el modelo entrenado ---
model.save('flappy_q_nn_model.keras', include_optimizer=False, save_format='keras')
print("Modelo guardado correctamente en flappy_q_nn_model.keras")
