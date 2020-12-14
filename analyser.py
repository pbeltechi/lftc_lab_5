import yaml
import re
from automate import Automate

'''
    Analizorul lexical mlp c++
'''
class Analyser:

    '''
        Incarca dictionarul mlp c++
    '''
    def __init__(self):
        self.minIDLength = 8
        self.constantAutomate = Automate('config_real.json')
        self.IDAutomate = Automate('config_variabila.json')
        self.reserved = {}
        with open('config.yml') as file:
            self.reserved = yaml.load(file, Loader=yaml.FullLoader)
    
    '''
        Analizeaza codul de pe fiecare linie primita din codul sursa
    '''
    def analyse(self, lines):
        self.code = []
        self.errors = []
        # print()
        # print(self.reserved)
        contorL = 1
        for uLine in lines:
            line = uLine.strip('\t \n ').split(' ')
            for atom in line:
                if not self.analyseAtom(atom):
                    self.errors.append((atom,contorL))
            contorL +=1


    '''
        Analizeaza un atom cautand din ce categorie face parte
    '''
    def analyseAtom(self, atom):
        if atom == '':
            return True
        if atom in self.reserved.keys():
            self.code.append((atom,self.reserved[atom]))
            return True
        elif self.IDAutomate.verifySequence(atom) and len(atom) < self.minIDLength:   #identificator ID
            self.code.append((atom,self.reserved['ID']))
            return True
        elif self.constantAutomate.verifySequence(atom):    #identificator CONST
            self.code.append((atom,self.reserved['CONST']))
            return True
        elif self.isComposed(atom):
            return True
        return False
        
    '''
        Analizeaza daca atomul este compus (fara spatii)
    '''
    def isComposed(self, atom):
        for x in self.reserved.keys():        
            pos = atom.find(x)
            if(pos != -1):
                atomFound = atom[pos:pos+len(x)]
                left = atom[:pos]
                right = atom[pos + len(x):]
                resultLeft = self.analyseAtom(left)
                self.code.append((atomFound,self.reserved[atomFound]))
                return resultLeft and self.analyseAtom(right)
        return False
        