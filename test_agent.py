from ple.games.flappybird import FlappyBird
from ple import PLE
import time
import argparse
import importlib
import sys

# --- Configuración del Entorno y Agente ---
# Inicializar el juego
game = FlappyBird()  # Usar FlappyBird en vez de Pong
env = PLE(game, display_screen=True, fps=30) # fps=30 es más normal, display_screen=True para ver


# Inicializar el entorno
env.init()

# Obtener acciones posibles
actions = env.getActionSet()

# --- Argumentos ---
parser = argparse.ArgumentParser(description="Test de agentes para FlappyBird (PLE)")
parser.add_argument('--agent', type=str, required=True, help='Ruta completa del agente, ej: agentes.random_agent.RandomAgent')
args = parser.parse_args()

# --- Carga dinámica del agente usando path completo ---
try:
    module_path, class_name = args.agent.rsplit('.', 1)
    agent_module = importlib.import_module(module_path)
    AgentClass = getattr(agent_module, class_name)
except (ValueError, ModuleNotFoundError, AttributeError):
    print(f"No se pudo encontrar la clase {args.agent}")
    sys.exit(1)

# Inicializar el agente
agent = AgentClass(actions, game)

# Agente con acciones aleatorias
total_reward=0
for i in range(100):
    env.reset_game()
    agent.reset()
    state_dict = env.getGameState()
    done = False
    total_reward_episode = 0
    print(f"\n--- Ejecutando agente episodio {i+1} ---")
    while not done:
        action = agent.act(state_dict)
        reward = env.act(action)
        state_dict = env.getGameState()
        done = env.game_over()
        total_reward_episode += reward
        if total_reward_episode>=100:
            total_reward_episode = 100
            done=True
    print(f"Recompensa episodio{i+1}: {total_reward_episode}")
    total_reward+=total_reward_episode
average_reward=total_reward//100
print(f"Recompensa promedio del agente {class_name} en 100 episodios: {average_reward}(Recomenpensa máxima: 100)")
