import re, sys

class Transition:
    """
    internal representation for a transition, useful for organization purposes
    and for printing the emulator representation of the transition
    """
    def __init__(self, states, symbols, movement):
        self._states = states
        self._symbols = symbols
        self._mov = movement

    def __str__(self):
        return f"{self._states[0]} {self._symbols[0]} {self._symbols[1]} {self._mov} {self._states[1]}"


class State_Categorizer:
    """
    class used to differentiate between states
    """
    
    @staticmethod
    def is_initial(state):
        return re.search(r"Q0+(?![0-9]+)", state) is not None
    
    @staticmethod
    def is_accept(state):
        return re.search(r"Y+", state) is not None
    
    @staticmethod
    def is_reject(state):
        return re.search(r"N+", state) is not None


class Transitions_Parser:
    """
        class for parsing every transition, maintains '_char_index' as a way to generate
        symbols for symbol I/O.
    """

    def __init__(self):
        self._char_index = ord('A')
        self._symbol_table = dict()
        self._trans_len = None
        self._symb_len = None
        
    
    def is_prob_transition(self, string):
        """
        verifies if the string passed as input is probably a transition,
        can't check if really a transition because the length of the states must be equal
        to every other state (same for the symbols)
        """
        return re.search(r"^((Q[0-9]+|Y+|N+)(A[0-9]+)){2}(L|R|S)$", string) is not None
    
    def get_state_representation(self, state):
        """
        returns the emulator representation for a state
        """
        if State_Categorizer.is_accept(state):
            return "halt-accept"
        elif State_Categorizer.is_reject(state):
            return "halt-reject"
        elif State_Categorizer.is_initial(state):
            return "Qin"
        else:
            return state

    def parse_states(self, trans):
        """
        parses the states and verifies if they are the same length as every other state
        """
        matches = re.findall(r"(Q[0-9]+|Y+|N+)", trans)
        assert len(matches) == 2
        if self._trans_len is None:
            self._trans_len = len(matches[0])
        for match in matches:
            if len(match) != self._trans_len:
                raise RuntimeError("Wrong state length")
            else:
                pass
        return (self.get_state_representation(matches[0]), self.get_state_representation(matches[1]))
    
    def get_symbol_representation(self, symbol):
        """
        returns the emulator representation for a symbol; if the symbol has not been seen
        yet, also assigns the emulator representation for that symbol
        """
        def is_blank(symbol): return re.search(r"A0+(?![0-9]+)", symbol) is not None
        
        if is_blank(symbol):
            return '_'
        
        elif symbol not in self._symbol_table:
            self._symbol_table[symbol] = chr(self._char_index)
            self._char_index += 1
        
        return self._symbol_table[symbol]

    def parse_symbols(self, trans):
        """
        parses the symbols and verifies if they are the same length as every other state
        """
        matches = re.findall(r"A[0-9]+", trans)
        assert len(matches) == 2
        if self._symb_len is None:
            self._symb_len = len(matches[0])
        for match in matches:
            if len(match) != self._symb_len:
                raise RuntimeError("Wrong symbol length")
        return (self.get_symbol_representation(matches[0]), self.get_symbol_representation(matches[1]))

    def parse_movement(self, trans):
        """
        parses the tape movement
        """
        if trans[-1] in ('L', 'R', 'S'):
            return trans[-1]
        raise RuntimeError("Unknown Tape Movement")

class Translator:
    """
    validates and sanitizes the input and applies the transitions parser
    to every transition
    """
    def __init__(self, string):
        self._transitions = []
        strings = string.split(';')
        parser = Transitions_Parser()
        for string in strings:
            if parser.is_prob_transition(string):
                self._transitions.append(Transition(parser.parse_states(string)\
                    , parser.parse_symbols(string)\
                        , parser.parse_movement(string)))
            else:
                raise RuntimeError("Invalid Input")

    def print(self):
        """
        prints the emulator representation for the turing machine given as Input 
        to the constructor of this class
        """
        for transition in self._transitions:
            print(transition)


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        raise RuntimeError("\n Usage:python3 translator.py -f <file>\n\tor\n\
 python3 translator.py -c")
    
    if '-f' == sys.argv[1]:
        
        if len(sys.argv) < 3:
            raise RuntimeError("Not enough Arguments")
        
        ipt = open(sys.argv[2]).readline().strip()
    
    elif '-c' == sys.argv[1]:
        ipt = input("<input> ")
    
    Translator(ipt).print()
