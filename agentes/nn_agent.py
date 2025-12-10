from agentes.base import Agent
import numpy as np
import tensorflow as tf

class NNAgent(Agent):
    """
    Agente que utiliza una red neuronal entrenada para aproximar la Q-table.
    La red debe estar guardada como TensorFlow SavedModel.
    """
    def __init__(self, actions, game=None, model_path='flappy_q_nn_model.keras'):
        super().__init__(actions, game)
        self.model = tf.keras.models.load_model(model_path)

    # copiar estas funciones del QAgent:
    def discretize_velocity(self, vel):
        if vel < -5:
            return 0
        elif vel < -1:
            return 1
        elif vel <= 1:
            return 2
        elif vel <= 5:
            return 3
        else:
            return 4

    def discretize_state(self, state):
        y_bin = state['player_y'] // 25
        vel_bin = self.discretize_velocity(state['player_vel'])
        pipe_dist_bin = state['next_pipe_dist_to_player'] // 25
        pipe_top_bin = state['next_pipe_top_y'] // 25
        pipe_bottom_bin = state['next_pipe_bottom_y'] // 25
        return [y_bin, vel_bin, pipe_dist_bin, pipe_top_bin, pipe_bottom_bin]


    def act(self, state):
        state_disc = self.discretize_state(state)
        state_input = np.array(state_disc, dtype=np.float32).reshape(1, -1)
        q_values = self.model.predict(state_input, verbose=0)
        action_index = np.argmax(q_values[0])
        return self.actions[action_index]


