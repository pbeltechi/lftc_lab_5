class Grammar:

    def __init__(self):
        self.filename = 'grammar2.txt'
        self.grammar = {}
        self.stringGrammar = []
        self.read_grammar()

    def read_grammar(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line != '\n':
                self.stringGrammar.append(line)
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

    def is_terminal(self, terminal):
        return terminal in self.get_terminals()
    
    def get_productions(self):
        return self.grammar

    def get_productions_for_terminal(self, terminal):
        prods = []
        for key in self.grammar.keys():
            for alist in self.grammar[key]:
                if terminal in alist and alist[0] == terminal:
                    prods.append((key,alist))
        return prods

    def get_productions_for_composed_terminal(self, neterminal, terminal):
        p = []
        prods = self.grammar[neterminal]
        for prod in prods:
            if(prod[0] == terminal or not self.is_terminal(prod[0])):
                p.append((neterminal,prod))

            # if(prod[0] == terminal):
            #     return (neterminal,prod)
            # elif (not self.is_terminal(prod[0])):
            #     self.get_productions_for_composed_terminal(prod[0],terminal)
        return p

    def find_production_number(self, neterminal, terminal):
        string = neterminal + ' ->'
        for term in terminal:
            string += ' ' + term
        string += '\n'
        contor = 0
        for prod in self.stringGrammar:
            contor += 1
            if string == prod:
                return contor
        return -1
    
    def check_match(self,stack,sequence):
        tmp = ""
        contor = 0
        for word in stack:
            tmp += word
            contor += 1
            if sequence == tmp:
                return contor
        return -1


    def get_first_production(self):
        return self.stringGrammar[0].split(' ->')[0]

    def accepts(self, sequence):
        sequence = sequence.replace('\n',' ').split(' ')
        firstProduction = self.get_first_production()
        stack = [firstProduction, '$']
        quitBand = []
        sequence.append('$')
        char = sequence[0]
        accepted = False
        while True:
            print(sequence, stack, quitBand)
            isTerminal = self.is_terminal(stack[0])
            nr = self.check_match(stack,char)
            if nr > 0 and isTerminal:
                for _ in range(0,nr):
                    stack.pop(0)
                sequence.pop(0)
                char = sequence[0]
            elif not isTerminal:
                productions = self.get_productions_for_composed_terminal(stack[0], char)
                # if len(productions) > 1:
                #     raise Exception('gramatica este amigua')
                if len(productions) == 0:
                    break
                production = productions[0]
                no = self.find_production_number(production[0], production[1])
                quitBand.append(no)
                stack.pop(0)
                temp = []
                temp = production[1] + stack
                stack = temp
            else:
                break
            if sequence[0] == '$' and stack[0] == '$':
                accepted = True
                break
        return accepted

    def accepts_file(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
        string = ''
        for line in lines:
            string += line
        return self.accepts(string)


g = Grammar()
print(g.accepts('a a a c b b'))
