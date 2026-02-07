import random

class Act:
    def __init__(self, VALUES, x=None):
        if x is None:
            x = input()
        if type(x) == str:
            self.strbid = x
            l = x.split("-")
            if len(l) != 2 and x == 'd':
                self.strbid = "Stop!"
                self.intbid = -1
            elif len(l) != 2:
                self.intbid = VALUES["liarbid"]
                self.strbid = "Liar!"
            else:
                self.intbid = (int(l[0])-1) * VALUES["dice_sides"] + int(l[1]) - 1
        else:
            self.intbid = int(x)
            self.strbid = f"{x // VALUES["dice_sides"] + 1}-{x % VALUES["dice_sides"] + 1}"
            if self.intbid == VALUES["liarbid"]:
                self.strbid = "Liar!"
    
    @staticmethod
    def solver_act(solver, state, VALUES):
        d = solver.average_policy().action_probabilities(state)
        values = []
        weights = []
        for x in d:
            values.append(x)
            weights.append(d[x])
        return Act(VALUES, random.choices(values, weights=weights, k=1)[0])

    def __str__(self):
        return self.strbid
    
def print_cubes(state, player_id, VALUES):
    cubes = []
    for i in range(VALUES["numdice"]):
        cubes.append(state.history()[VALUES["numdice"] * player_id + i] + 1)
    print(*cubes)


def multiplay(game, solver):
    assert str(solver._game) == str(game), "This solver is not designed for this game. Incomatible/"
    VALUES = game.get_parameters()
    VALUES["liarbid"] = game.max_history_length() - 1 - VALUES["numdice"] * VALUES["players"]
    wins = 0
    losses = 0
    cont = True
    while cont:
        print("----------------------------------------------")
        print("New game")
        player_id = random.choice([0, 1])
        if player_id == 0:
            print("You go first")
        else:
            print("You go second")
        state = game.new_initial_state()

        while state.is_chance_node():
            values, weights = zip(*state.chance_outcomes())
            action = random.choices(values, weights=weights, k=1)[0]
            state.apply_action(action)
        print(f"Your dice are:", end = ' ')
        print_cubes(state, player_id, VALUES)

        while not state.is_terminal():
            if state.current_player() == player_id:
                print("Your bid is:", end = ' ')
                act = Act(VALUES) # reads
                if act.intbid == -1:
                    cont = False
                    break
                state.apply_action(act.intbid)
            else:
                act = Act.solver_act(solver, state, VALUES)
                print(act)
                state.apply_action(act.intbid)
        if not cont:
            break
        print(f"His cube were: ", end='')
        print_cubes(state, 1 - player_id, VALUES)
        if state.rewards()[player_id] == 1:
            print("You won!")
            wins += 1
        else:
            print("You lost!")
            losses += 1
        print(f"History: {state.history_str()}")
    print("----------------------------------------------")
    print("Total score you vs machine:")
    print(f'{wins}-{losses}')

if __name__ == "__main__":
    import pyspiel
    from save_load import *
    VALUES = {"players": 2, "numdice": 1, "dice_sides": 6}
    game = pyspiel.load_game("perudo", VALUES)
    solver = load_solver("models/1cube_mccfr_2026-02-04-21:10.pkl")
    multiplay(game, solver)