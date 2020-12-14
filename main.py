import re
from analyser import Analyser
from grammar import Grammar

class UI:
    '''
        Initializare UI cu analyser
    '''
    def __init__(self, grammar):
        self.grammar = grammar
    
    '''
        Printare meniu ui
    '''
    def printMenu(self):
        print('x => Iesire')
        print('1 => Multimea neterminalelor')
        print('2 => Multimea terminalelor')
        print('3 => Multimea regulilor de productie')
        print('4 => Multimea regulilor de productie pentru un anumit terminal')
        print('5 => Verifica o secventa de intrare')

    '''
        Printare lista pe ecran
    '''
    def printList(self, adict):
        for key in adict.keys():
            multi_value = adict[key]
            for value in multi_value:
                print(key, '->', value)

    '''
        Rulare meniu ui
    ''' 
    def run(self):
        s = ''
        while True:
            self.printMenu()
            s = input()
            if re.search('^[x]$', s):
                break
            try:
                print()
                if s =='1':
                    var = grammar.get_neterminals()
                    print(var)
                if s =='2':
                    var = grammar.get_terminals()
                    print(var)
                if s =='3':
                    var = grammar.get_productions()
                    self.printList(var)
                if s =='4':
                    non = input('terminal >')
                    var = grammar.get_productions_for_terminal(non)
                    for x in var:
                        print(x)
                if s =='5':
                    non = input('numele fisierului >')
                    var = grammar.accepts_file(non)
                    print(var)
                print()
            except Exception as e:
                print(e)

grammar = Grammar()
UI(grammar).run()
