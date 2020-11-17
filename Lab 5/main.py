# input definition
# first line the initial nonTerminal
# second line the terminals with spaces between elements
# third line the nonTerminals
# next lines the productions


class Lr0Parser:
    def __init__(self, file_path):
        file_program = self.read_program(file_path)
        self.initial = file_program[0][0]
        self.terminals = file_program[1]
        self.nonTerminals = file_program[2]
        self.productions = {}
        for elements in file_program[3:]:
            if elements[0] in self.productions:
                self.productions[elements[0]].append(elements[1:])
            else:
                self.productions[elements[0]] = [elements[1:]]
        self.data = [self.terminals, self.nonTerminals, self.productions, self.initial]

    def dotMaker(self, productions):
        dottedproductions = {}
        for nonTerminal in productions:
            dottedproductions[nonTerminal] = []
            for way in productions[nonTerminal]:
                dottedproductions[nonTerminal].append(["."] + way)
        return dottedproductions

    def removeTerminated(self, productions):
        initialState = {}
        for nonTerminal in productions:
            initialState[nonTerminal] = []
            for way in productions[nonTerminal]:
                terminated = True
                for element in way[1:]:
                    if element in self.nonTerminals:
                        terminated = False
                        break
                if not terminated:
                    initialState[nonTerminal].append(way)
        return initialState

    @staticmethod
    def read_program(file_path):
        file1 = open(file_path, 'r')
        lines = file1.readlines()
        file1.close()
        return [line.replace("\n", "").replace("\t", "").split(" ") for line in lines]


if __name__ == '__main__':
    lr0 = Lr0Parser("grammar.txt")
    dotted = lr0.dotMaker(lr0.productions)
    print(f"Dotted: {dotted}")
    initialState = lr0.removeTerminated(dotted)
    print(f"Initial: {initialState}")
