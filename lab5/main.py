from tabulate import tabulate


# input definition
# first line the initial nonTerminal
# second line the terminals with spaces between elements
# third line the nonTerminals
# next lines the productions

class Lr0Parser:
    """
    Precondition: to have a file
    input: the path of the file
    Postcondition: -
    output: -

    It will read the content of a file, set the class properties based on it and it will calculate
    the initial colsure (S' -> S)
    """

    def __init__(self, file_path):
        file_program = self.read_program(file_path)
        self.terminals = file_program[0]
        self.nonTerminals = file_program[1]
        self.productions = {}
        self.transactions = file_program[2:]
        for elements in self.transactions:
            if elements[0] in self.productions:
                self.productions[elements[0]].append(elements[1:])
            else:
                self.productions[elements[0]] = [elements[1:]]
        self.data = [self.terminals, self.nonTerminals, self.productions]
        dotted = self.dotMaker()

        self.initial_closure = {"S'": [dotted["S'"][0]]}
        self.closure(self.initial_closure, dotted["S'"][0])

    """
    Precondition: -
    input: -
    Postcondition: Every production starts with a dot and creates the S' production
    Output: A list of dotted products with S' as first in the list
    
    It will take each production and put a . on the first position
    """

    def dotMaker(self):
        self.dottedproductions = {'S\'': [['.', 'S']]}
        for nonTerminal in self.productions:
            self.dottedproductions[nonTerminal] = []
            for way in self.productions[nonTerminal]:
                self.dottedproductions[nonTerminal].append(["."] + way)

        return self.dottedproductions

    """
    Preconditions and input: 
        :param transition_value right side of the production we are doing the closure on
    
    Postcondition and output:
        :param closure_map the next possible state

    It will calculate the next possible state recursively, starting with the transition_value, by checking if the 
    dot is followed by a non terminal, in which case we add the transitions of that non terminal. 
    Afterwards we calculate each transition generated by this transition in a similar fashion.
    """

    def closure(self, closure_map, transition_value):
        dot_index = transition_value.index(".")
        transitions_map = self.dottedproductions
        if dot_index + 1 == len(transition_value):
            return
        after_dot = transition_value[dot_index + 1]
        if after_dot in self.nonTerminals:
            non_terminal = after_dot
            if non_terminal not in closure_map:
                closure_map[non_terminal] = transitions_map[non_terminal]
            else:
                closure_map[non_terminal] += transitions_map[non_terminal]
            for transition in transitions_map[non_terminal]:
                self.closure(closure_map, transition)

    """
    Input: transition
    Output: true if . is not the last element of the transition, false otherwise
    
    Code that checks if a transition finishes in dot or not
    """

    @staticmethod
    def shiftable(transition):
        dot_index = transition.index(".")
        if len(transition) > dot_index + 1:
            return True
        return False

    """
    Precondondition: The transition must have a dot
    Input: transition
    Postcondition: -
    Output: The same transition but with the dot in the next position
    """

    @staticmethod
    def shift_dot(transition):
        transition = transition[:]
        dot_index = transition.index(".")
        if not Lr0Parser.shiftable(transition):
            raise Exception("Should I shift it back ?")
        if len(transition) > dot_index + 2:
            remainder = transition[dot_index + 2:]
        else:
            remainder = []
        transition = transition[:dot_index] + [transition[dot_index + 1]] + ["."] + remainder
        return transition

    """
    Precondition and input: -
    Postcondition nand output: All the states and a valid output table
    
    First it will start calculating all the states based on the initial state using the goto method, which uses the 
    closure method. 
    We use a Queue so that the order of the states is cannonical
    Once we have the states, we will filter the reduced and accepted states, add then to the table
    Then we add the shifts and gotos for the rest of the states
    Note that the order of these 2 table sets can be interchanged 
    
    """

    def canonical_collection(self):
        self.actions_and_goto_by_state_id = {}
        self.queue = [{
            "state": self.initial_closure,
        }]
        self.states = []
        self.state_parents = {}
        while len(self.queue) > 0:
            self.goto_all(**self.queue.pop(0))
        reduced = self.get_reduced()
        for k in reduced:
            red_k = list(reduced[k].keys())
            if red_k[0] != "S'":
                trans = red_k + reduced[k][red_k[0]][0][:-1]
                reduce_index = self.transactions.index(trans) + 1
                self.actions_and_goto_by_state_id[k] = {terminal: f"r{reduce_index}" for terminal in self.terminals}
                self.actions_and_goto_by_state_id[k]["$"] = f"r{reduce_index}"
            else:
                self.actions_and_goto_by_state_id[k] = {"$": "accept"}
        del self.state_parents[0]
        for key in self.state_parents:
            parent = self.state_parents[key]
            if parent["parent_index"] in self.actions_and_goto_by_state_id:
                self.actions_and_goto_by_state_id[parent["parent_index"]][parent["before_dot"]] = key
            else:
                self.actions_and_goto_by_state_id[parent["parent_index"]] = {parent["before_dot"]: key}
        table = {f"I{index}": self.actions_and_goto_by_state_id[index] for index in range(len(self.states))}
        self.print_table(table)

    """
    Precondition and inputs"
        :param state - a valid state 
        :param parent - index of the parent state
        :param parent_key - the terminal/nonTerminal before the .
        
    Postcondition and output:
        All the posible states generated and not yet created put in the queue
    
    Checks if the current state has already been calculated, if not than it will be saved as a valid state,
    and each of the possible states generated by this state will be added to the queue
    """

    def goto_all(self, state, parent=-1, parent_key="-1"):
        if state not in self.states:
            self.states.append(state)
            index = len(self.states) - 1
            self.state_parents[index] = {
                "parent_index": parent,
                "before_dot": parent_key
            }
            self.print_dict(state, f"state {index}")
            for key in state:
                for transition_value in state[key]:
                    if self.shiftable(transition_value):
                        self.goto_one(key, transition_value, index)
        else:
            if parent in self.actions_and_goto_by_state_id:
                self.actions_and_goto_by_state_id[parent][parent_key] = self.states.index(state)
            else:
                self.actions_and_goto_by_state_id[parent] = {parent_key: self.states.index(state)}

    """
    Input and precondition: 
        :param key  - left side of a production
        :param transition_value - shiftable transition
        :param parent - the index of the parent state
    
    Ouptut and postcondition:
        It will create one state based on the transition value
            
    It will take the transition value, shift it once, create the state based on the shifted transition value
    and append it to the queue to calculate its offsprings later
    """

    def goto_one(self, key, transition_value, parent=-1):
        shifted_transition = self.shift_dot(transition_value)
        closure_map = {key: [shifted_transition]}
        self.closure(closure_map, shifted_transition)
        self.queue.append({
            "state": closure_map,
            "parent": parent,
            "parent_key": shifted_transition[shifted_transition.index(".") - 1]
        })

    """
    Input and preconditions: 
        :precondition: a set of states to be already created on the object
    
    Output:
        The states that are called reduced states
        
    It will go through each state and checks if the . is on the last position of the only transition, otherwise,
    if there is a . on the last position but there are more than 1 transitions, it will stop the application since
    we have a conflict
    """

    def get_reduced(self):
        self.reduced = {}
        for state in self.states:
            state_key = list(state.keys())[0]
            if len(state[state_key]) and len(state[state_key][0]) \
                    and state[state_key][0][-1] == ".":
                if len(state) > 1 or len(state[state_key]) > 1:
                    self.conflict(state)
                self.reduced[self.states.index(state)] = state
        return self.reduced

    """
    Input and preconditions: 
        :param state - a state with a conflict
    
    Output and postconditions:
        -
        
    It will print out the details of the conflict and stop the application. 
    """

    def conflict(self, state):
        transitions = []
        state_index = self.states.index(state)
        for key in state:
            for transition in state[key]:
                transitions.append(transition)
        conflicted = None
        for transition in transitions:
            index = transition.index(".")
            if index == len(transition) - 1:
                continue
            for node in transition[index + 1:]:
                if node in self.terminals:
                    conflicted = transition[index]
                print(f"Conflict at state {state_index}. {state} at column {conflicted}")
                exit(1)
        raise Exception(f"Conflict at state {state_index}. {state} unknwon column")

    """
    Input and preconditions: 
        :param file_path - a valid file location
        
    Output: 
        The content of the file
    """

    @staticmethod
    def read_program(file_path):
        file1 = open(file_path, 'r')
        lines = file1.readlines()
        file1.close()
        return [line.replace("\n", "").replace("\t", "").split(" ") for line in lines]

    """
        Input and preconditions: 
            :param hashmap - a dict

        Output: 
            Prints out the hashmap in a user friendly way
    """

    @staticmethod
    def print_dict(hashmap, message=None, deepness=""):
        if message is not None:
            print(deepness + message)
        for key in hashmap:
            print(f"{deepness}{key} : {hashmap[key]}")

    """
            Input and preconditions: 
                :param hashmap - a table

            Output: 
                Prints out the table in a user friendly way and creates and html with the same table
    """

    def print_table(self, hashmap):
        headers = ["State"] + ["Action " + term for term in self.terminals] + ["Action $"] + ["Go to " + nterm for nterm
                                                                                              in self.nonTerminals]
        keys = self.terminals + ["$"] + self.nonTerminals
        rows = []
        for state_key in hashmap:
            row = [state_key] + [hashmap[state_key][key] if key in hashmap[state_key] else "" for key in keys]
            rows.append(row)
        tab = tabulate(rows, headers, tablefmt="pretty")
        file_tab = tabulate(rows, headers, tablefmt="html")
        print(tab)
        with open(f"output.html", 'w') as out_file:
            out_file.write(file_tab)

    """
    Prints out a specific data of the parser object
    """

    def print_data(self, index=-1):
        if index == -1:
            exit()
        else:
            print(self.data[index - 1])

    """
    Prints out a productions of a non terminal in a user friendly way
    """

    def print_production(self, non_terminal):
        data = self.data[2]
        if non_terminal in data:
            for row in data[non_terminal]:
                print(f"{non_terminal} -> {row}")
        else:
            print("Wrong non terminal!")


def show_menu():
    lr0 = Lr0Parser("g0.txt")

    print("""
    1 - print terminals
    2 - print non terminals
    3 - print productions
    4 - print productions for a given non terminal
    5 - canonical collection
    6 - exit
    """)
    menu = {
        "1": lambda: lr0.print_data(1),
        "2": lambda: lr0.print_data(2),
        "3": lambda: lr0.print_data(3),
        "4": lambda: lr0.print_production(input("Please give a non terminal:")),
        "5": lambda: lr0.canonical_collection(),
        "6": exit
    }
    while True:
        option = input("Choose an option:")
        if option in menu:
            menu[option]()
        else:
            print("Wrong option")


if __name__ == '__main__':
    show_menu()