from agentes.base import Agent
import numpy as np
import tensorflow as tf

class NNAgent(Agent):
    """
    Agente que utiliza una red neuronal entrenada para aproximar la Q-table.
    La red debe estar guardada como TensorFlow SavedModel.
    """
    def __init__(self, actions, game=None, model_path='flappy_q_nn_model.h5'):
        super().__init__(actions, game)
        # Cargar el modelo entrenado
        self.model = tf.keras.models.load_model(model_path)

    def act(self, state):
        """
        Devuelve la acción con mayor Q-value según la red neuronal.
        """
        # Convertir el estado a array numpy con batch dimension
        state_input = np.array(state, dtype=np.float32).reshape(1, -1)
        # Predecir los Q-values para ese estado
        q_values = self.model.predict(state_input, verbose=0)
        # Elegir la acción con mayor Q-value
        action_index = np.argmax(q_values[0])
        return self.actions[action_index]
