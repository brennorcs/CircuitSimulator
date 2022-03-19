#Universidade Federal do Rio de Janeiro
#Departamento de Engenharia Eletrônica
#Disciplina: Circuitos Elétricos 2
#Professora: Fernanda Duarte Vilela Reis de Oliveira
#Aluno: Brenno Rodrigues de Carvalho da Silva

#Resistor: R<identificacao> <no1> <no2> <valor da resistencia>
#Fonte de corrente: I<identificacao> <no cuja corrente eh drenada pela fonte> <no cuja corrente eh injetada pela fonte> <valor da corrente>
#Fonte de corrente controlada por tensao: G<identificacao> <noI(fonte drena a corrente desseno)> <noI(fonte injeta a corrente nesse no)> <nov(positivo)> <nov(negativo)> <valor da transcondutancia Gm>
#Comentarios, linhas que nao sao usadas pelo programa: *<comentario> 

import numpy as np
import cmath

class circuit():
    def __init__(self,netlistNameFile):
        self.netlistNameFile = netlistNameFile
        self.shortNetlist = []
        self.controlOfAuxCurrent = 0
        self.resultOrder = []
        try: 
            with open(netlistNameFile) as f:
                longNetlist = f.readlines()
                for count in range(0, len(longNetlist)):
                    if (circuit.checkInvalidArgument(longNetlist[count])):
                        self.shortNetlist.append(longNetlist[count])
            f.close()
        except:
             print("\033[1;31;40m Couldn't open the file. Please insert de correct file name.")
        self.nodeNumbers = self.getBiggerNode() + 1        
        self.circuitMatrixSystem = np.zeros([self.nodeNumbers+self.getNumberOfAuxCurrent(),self.nodeNumbers+self.getNumberOfAuxCurrent()], dtype = "complex_") 
        self.matrixIn = np.zeros([self.nodeNumbers+self.getNumberOfAuxCurrent()], dtype = "complex_")
        self.frequenceW = 0
        self.result = np.zeros([self.nodeNumbers+self.getNumberOfAuxCurrent()-1], dtype = "complex_")
        for count in range (1, self.nodeNumbers):
            self.resultOrder.append("e" + str(count))

    def checkInvalidArgument(line):
        if(len(line)<2):
            return False
        words = line.split()
        firstLetter = words[0][0]
        if ((firstLetter == "I") or  (firstLetter == "G") or (firstLetter == "R") or (firstLetter == "C") or (firstLetter == "L") or (firstLetter == "K") or  (firstLetter == "E") or  (firstLetter == "V") or  (firstLetter == "F") or  (firstLetter == "H")):
            return True
        return False 
        
    def getBiggerNode(self):
        node = 0
        for count in range(0, len(self.shortNetlist)):
            for count2 in range(1,3):
                if(int(self.shortNetlist[count].split(" ")[count2]) > node):
                    node = int(self.shortNetlist[count].split(" ")[count2])
        return node
    
    def getNumberOfAuxCurrent(self):
        auxCurrentCounter = 0
        for count in range(0, len(self.shortNetlist)):
            if((self.shortNetlist[count][0] == "E") or (self.shortNetlist[count][0] =="V") or (self.shortNetlist[count][0] =="F") or (self.shortNetlist[count][0] =="L")):
                auxCurrentCounter+=1
            elif(self.shortNetlist[count][0] == "H" ):
                auxCurrentCounter+=2
        return auxCurrentCounter        

    def setCurrentSourceStamp(self,netlistLine):
        if (netlistLine.split(" ")[3] == "DC"):  
            self.matrixIn[int(netlistLine.split(" ")[1])] += -float(netlistLine.split(" ")[4])
            self.matrixIn[int(netlistLine.split(" ")[2])] += float(netlistLine.split(" ")[4])
        else:
            self.matrixIn[int(netlistLine.split(" ")[1])] += -cmath.rect(float(netlistLine.split(" ")[5]), float(netlistLine.split(" ")[7])*(np.pi/180))
            self.matrixIn[int(netlistLine.split(" ")[2])] += cmath.rect(float(netlistLine.split(" ")[5]), float(netlistLine.split(" ")[7])*(np.pi/180))   
        return 0

    def setResistorStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[1])] += 1/float(netlistLine.split(" ")[3])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[2])] += -1/float(netlistLine.split(" ")[3])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[1])] += -1/float(netlistLine.split(" ")[3])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[2])] += 1/float(netlistLine.split(" ")[3])
        return 0

    def setInductorStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[1])] += 1/(1j*self.frequenceW*(float(netlistLine.split(" ")[3]))) #NodalAnalisis
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[2])] += -1/(1j*self.frequenceW*(float(netlistLine.split(" ")[3]))) #NodalAnalysis
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[1])] += -1/(1j*self.frequenceW*(float(netlistLine.split(" ")[3]))) #NodalAnalysis
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[2])] += 1/(1j*self.frequenceW*(float(netlistLine.split(" ")[3]))) #NodalAnalysys
        return 0

    def setCapacitorStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[1])] += (1j*self.frequenceW*(float(netlistLine.split(" ")[3])))
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[2])] += -(1j*self.frequenceW*(float(netlistLine.split(" ")[3])))
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[1])] += -(1j*self.frequenceW*(float(netlistLine.split(" ")[3])))
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[2])] += (1j*self.frequenceW*(float(netlistLine.split(" ")[3])))
        return 0        

    def setCurrentSourceControledByVoltage(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[3])] += float(netlistLine.split(" ")[5])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[4])] += -float(netlistLine.split(" ")[5])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[3])] += -float(netlistLine.split(" ")[5])
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[4])] += float(netlistLine.split(" ")[5])
        return 0

    def setTransformersStamp(self,netlistLine):
        gama11 = float(netlistLine.split(" ")[6])/((float(netlistLine.split(" ")[5])*float(netlistLine.split(" ")[6]))- (float(netlistLine.split(" ")[7])*float(netlistLine.split(" ")[7]))) 
        gama22 = float(netlistLine.split(" ")[5])/((float(netlistLine.split(" ")[5])*float(netlistLine.split(" ")[6]))- (float(netlistLine.split(" ")[7])*float(netlistLine.split(" ")[7])))
        gama12 =-float(netlistLine.split(" ")[7])/((float(netlistLine.split(" ")[5])*float(netlistLine.split(" ")[6]))- (float(netlistLine.split(" ")[7])*float(netlistLine.split(" ")[7])))
        #gama12=gama21

        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[1])] += gama11/(1j*self.frequenceW) #aa
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[2])] += -gama11/(1j*self.frequenceW)#ab 
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[3])] += gama12/(1j*self.frequenceW)#ac
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),int(netlistLine.split(" ")[4])] += -gama12/(1j*self.frequenceW)#ad
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[1])] += -gama11/(1j*self.frequenceW)#ba
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[2])] += gama11/(1j*self.frequenceW)#bb
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[3])] += -gama12/(1j*self.frequenceW)#bc
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),int(netlistLine.split(" ")[4])] += gama12/(1j*self.frequenceW)#bd
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),int(netlistLine.split(" ")[1])] += gama12/(1j*self.frequenceW)#ca
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),int(netlistLine.split(" ")[2])] += -gama12/(1j*self.frequenceW)#cb
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),int(netlistLine.split(" ")[3])] += gama22/(1j*self.frequenceW)#cc
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),int(netlistLine.split(" ")[4])] += -gama22/(1j*self.frequenceW)#bc
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),int(netlistLine.split(" ")[1])] += -gama12/(1j*self.frequenceW)#da
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),int(netlistLine.split(" ")[2])] += gama12/(1j*self.frequenceW)#db
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),int(netlistLine.split(" ")[3])] += -gama22/(1j*self.frequenceW)#dc
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),int(netlistLine.split(" ")[4])] += gama22/(1j*self.frequenceW)#dd
        return 0
    
    def setCurrentSourceControledByAmpereStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),self.nodeNumbers+self.controlOfAuxCurrent] += float(netlistLine.split(" ")[5]) #ax
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),self.nodeNumbers+self.controlOfAuxCurrent] += -float(netlistLine.split(" ")[5]) #bx
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),self.nodeNumbers+self.controlOfAuxCurrent] += 1 #cx
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),self.nodeNumbers+self.controlOfAuxCurrent] += -1 #dx
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[3])] += -1 #xc
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[4])] += 1 #xd
        self.controlOfAuxCurrent += 1
        return 0

    def setVoltageSourceControledByVoltageStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),self.nodeNumbers+self.controlOfAuxCurrent] += 1 #ax
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),self.nodeNumbers+self.controlOfAuxCurrent] += -1 #bx
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[1])] += -1 #xa
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[2])] += 1 #xb
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[3])] += float(netlistLine.split(" ")[5]) #xc
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[4])] += -float(netlistLine.split(" ")[5]) #xd
        self.controlOfAuxCurrent += 1
        return 0
    
    def setVoltageSourceControledByAmpereStamp(self,netlistLine):
        self.circuitMatrixSystem[int(netlistLine.split(" ")[3]),self.nodeNumbers+self.controlOfAuxCurrent] += 1 #cx
        self.circuitMatrixSystem[int(netlistLine.split(" ")[4]),self.nodeNumbers+self.controlOfAuxCurrent] += -1 #dx
        self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),self.nodeNumbers+self.controlOfAuxCurrent+1] += 1 #ay
        self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),self.nodeNumbers+self.controlOfAuxCurrent+1] += -1 #by
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[3])] += -1 #xc
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[4])] += 1 #xd
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent+1,int(netlistLine.split(" ")[1])] += -1 #ya
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent+1,int(netlistLine.split(" ")[2])] += 1 #yb
        self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent+1,self.nodeNumbers+self.controlOfAuxCurrent] += float(netlistLine.split(" ")[5]) #yx
        self.controlOfAuxCurrent += 2

        return 0

    def setVoltageSourceStamp(self,netlistLine):
        if (netlistLine.split(" ")[3] == "DC"):
            self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),self.nodeNumbers+self.controlOfAuxCurrent] += 1 #ax
            self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),self.nodeNumbers+self.controlOfAuxCurrent] += -1 #bx
            self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[1])] += -1 #xc
            self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[2])] += 1 #xd  
            self.matrixIn[self.nodeNumbers+self.controlOfAuxCurrent] += -float(netlistLine.split(" ")[4])
        else:
            self.circuitMatrixSystem[int(netlistLine.split(" ")[1]),self.nodeNumbers+self.controlOfAuxCurrent] += 1 #ax
            self.circuitMatrixSystem[int(netlistLine.split(" ")[2]),self.nodeNumbers+self.controlOfAuxCurrent] += -1 #bx
            self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[1])] += -1 #xc
            self.circuitMatrixSystem[self.nodeNumbers+self.controlOfAuxCurrent,int(netlistLine.split(" ")[2])] += 1 #xd 
            self.matrixIn[self.nodeNumbers+self.controlOfAuxCurrent] += cmath.rect(float(netlistLine.split(" ")[5]), float(netlistLine.split(" ")[7])*(np.pi/180))
        self.controlOfAuxCurrent += 1
        return 0    
        
    def setCircuitSystem(self):
        for count in range (0, len(self.shortNetlist)):
            if (self.shortNetlist[count][0] == "G"):
                self.setCurrentSourceControledByVoltage(self.shortNetlist[count])
            elif (self.shortNetlist[count][0] == "R"):
                self.setResistorStamp(self.shortNetlist[count])
            elif (self.shortNetlist[count][0] == "C"):
                self.setCapacitorStamp(self.shortNetlist[count])
            elif (self.shortNetlist[count][0] == "L"):
                self.setInductorStamp(self.shortNetlist[count])
            elif (self.shortNetlist[count][0] == "K"):
                self.setTransformersStamp(self.shortNetlist[count])  
            elif(self.shortNetlist[count][0] == "I"):
                self.setCurrentSourceStamp(self.shortNetlist[count])
            elif(self.shortNetlist[count][0] == "F"):
                self.setCurrentSourceControledByAmpereStamp(self.shortNetlist[count])
                self.resultOrder.append("j"+str(self.shortNetlist[count]).split(" ")[0])
            elif(self.shortNetlist[count][0] == "E"):
                self.setVoltageSourceControledByVoltageStamp(self.shortNetlist[count])
                self.resultOrder.append("j"+str(self.shortNetlist[count]).split(" ")[0])
            elif(self.shortNetlist[count][0] == "H"):
                self.setVoltageSourceControledByAmpereStamp(self.shortNetlist[count])
                self.resultOrder.append("jx"+str(self.shortNetlist[count]).split(" ")[0])
                self.resultOrder.append("j"+str(self.shortNetlist[count]).split(" ")[0])
            elif(self.shortNetlist[count][0] == "V"): 
                self.setVoltageSourceStamp(self.shortNetlist[count])
                self.resultOrder.append("j"+str(self.shortNetlist[count]).split(" ")[0])
            else:
                print("In development")                     
        self.circuitMatrixSystem = np.delete(self.circuitMatrixSystem, (0), axis=0)
        self.circuitMatrixSystem = np.delete(self.circuitMatrixSystem, (0), axis=1)
        self.matrixIn = np.delete(self.matrixIn, (0), axis=0)          
        return 0

    def getResult(self):
        for count in range (0, len(self.result)):
            if (self.resultOrder[count][0] == "e"):
                print(str(self.resultOrder[count]+" :"+str(self.result[count]))+ " V")
            else:
                print(str(self.resultOrder[count]+" :"+str(self.result[count]))+ " A")     
        return 0

    def getshortNetlist(self):
        print (self.shortNetlist)
        return 0

    def getCircuitMatrixSystem(self):
        print(self.circuitMatrixSystem)
        return 0

    def getMatrixIn(self):
        print(self.matrixIn)
        return 0

    def solveSystem(self):
        try:
            self.result = np.linalg.solve(self.circuitMatrixSystem, self.matrixIn)
            self.getResult()
        except:
            print("Singular matrix system")
        return 0

    def setFrequence(self):
        for count in range (0, len(self.shortNetlist)):
            if (self.shortNetlist[count][0] == "I") and (self.shortNetlist[count].split(" ")[3] == "SIN"):
                self.frequenceW = (float(self.shortNetlist[count].split(" ")[6]))*2*np.pi
        return 0

    def getFrequence(self):
        print(self.frequenceW)
        return 0