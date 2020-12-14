class Grammar:

    def __init__(self):
        self.filename = 'grammar2.txt'
        self.grammar = {}
        self.read_grammar()

    def read_grammar(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line != '\n':
                striped_line = line.split('->')
                neterminal = striped_line[0].replace(' ', '')
                terminals = []
                striped_line = striped_line[1].split(' ')
                for i in range(1, len(striped_line)):
                    terminals.append(striped_line[i].replace(' ', '').replace('\n',''))
                if self.grammar.get(neterminal):
                    self.grammar[neterminal].append(terminals) 
                else:
                    self.grammar[neterminal] = [terminals]
        
    def get_neterminals(self):
        return list(self.grammar.keys())
    
    def get_terminals(self):
        neterminals = set([])
        for multi_value in self.grammar.values():
            for alist in multi_value:
                for value in alist:
                    if value not in self.grammar.keys():
                        neterminals.add(value)
        return neterminals
    
    def get_productions(self):
        return self.grammar

    def get_productions_for_terminal(self, terminal):
        prods = []
        for key in self.grammar.keys():
            for alist in self.grammar[key]:
                if terminal in alist and alist[0] == terminal:
                    prods.append(key + " -> " + str(alist))
        return prods

Grammar()
