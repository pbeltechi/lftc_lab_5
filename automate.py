import json

'''
    clasa ce defnieste automatul
'''
class Automate:

    '''
        incarca definitia automatului finit
    '''
    def __init__(self,filename):
        self.filename = filename
        # self.filename = 'config_variabila.json'
        self.elements = {}
        with open(self.filename) as f:
            self.elements = json.load(f)
    '''
        returneaza multimea starilor automatului finit
    '''
    def getStates(self):
        states = []
        for state in self.elements['states']:
            states.append(state['name'])
        return states
    
    '''
        returneaza aflabetul automatului finit
    '''
    def getAlphabet(self):
        alph = []
        for state in self.elements['states']:
            for op in state['transitions'].keys():
                alph.append(op)
        return sorted(set(alph))

    '''
        returneaza toate tranzitiile automatului finit
    '''
    def getTransitions(self):
        transitions = []
        for state in self.elements['states']:
            for transition in state['transitions']:
                transitions.append((state['name'],transition, state['transitions'][transition]))
        return transitions

    '''
        returneaza multimea starilor finale automatului finit
    '''
    def getFinalStates(self):
        states = []
        for state in self.elements['states']:
            if state['isFinal'] == True:
                states.append(state['name'])
        return states
        
    '''
        returneaza multimea starilor finale automatului finit
    '''
    def getInitialStates(self):
        return self.elements['startState']

    '''
        pentru un automat finit determinist, verifica daca o secventa este acceptata de automatul finit, returnand-o
    '''
    def verifySequence(self,seq):
        currentState = self.elements['startState']
        found = False
        for char in seq:
            state = self.__getStateByName(currentState)
            found = False
            for transition in state['transitions']:
                if char == transition:
                    currentState = state['transitions'][transition]
                    found = True                                            # s-a gasit tranzitia iesim din bucla
                    break
            if not found:
                break
        return found and currentState in self.getFinalStates()

    '''
        pentru un automat finit determinist, determina cel mai lung prefix dintr-o secventa data care este o
        secventa acceptata de automat, returnand-o
    '''
    def getLongestPrefix(self,seq):
        faras = ""
        for i in range(len(seq),0,-1):
            faras = seq[:i]
            if self.verifySequence(faras):
                break
        return faras
    
    '''
        returneaza o stare dupa nume (name = 'q1' | 'q0')
    '''
    def __getStateByName(self, name):
        for state in self.elements['states']:
            if state['name'] == name:
                return state
        return False

    '''
        seteaza elementele AF
    '''
    def setAutomate(self, automate):
        self.elements = json.loads(automate)
        return self.elements