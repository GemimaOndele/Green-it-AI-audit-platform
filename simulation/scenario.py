from .simulation_engine import run_simulation


def get_simulation_results(input_data=None, action_params=None):
    return run_simulation(input_data=input_data, action_params=action_params)


def simulate_actions(input_data=None, action_params=None):
    return get_simulation_results(input_data=input_data, action_params=action_params)