from datetime import datetime
import pickle

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H:%M")

def save(solver, path=None, name=None):
    if name is not None:
        path = f"models/{name}_{get_timestamp()}.pkl"
    if path is None:
        path = f"models/somemodel{get_timestamp()}.pkl"
    with open(path, "wb") as file:
        pickle.dump(solver, file)
        
def load_solver(filepath):
    with open(filepath, "rb") as file:
        solver = pickle.load(file)
    return solver