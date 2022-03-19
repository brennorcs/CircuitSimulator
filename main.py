#Universidade Federal do Rio de Janeiro
#Departamento de Engenharia Eletrônica
#Disciplina: Circuitos Elétricos 2
#Professora: Fernanda Duarte Vilela Reis de Oliveira
#Aluno: Brenno Rodrigues de Carvalho da Silva

import circuit as c

if __name__ == '__main__':

    print("\033[1;36;40mUniversidade Federal do Rio de Janeiro")
    print("\033[1;36;40mDepartamento de Engenharia Eletrônica")
    print("\033[1;36;40mDisciplina: Circuitos Elétricos 2")
    print("\033[1;36;40mProfessora: Fernanda Duarte Vilela Reis de Oliveira")
    print("\033[1;36;40mAluno: Brenno Rodrigues de Carvalho da Silva")
    print("\033[1;36;40m======================================================================================")
    key = True
    while(key):
        netlistFileName = input("\033[1;37;40mPlease insert the netlist name: \n")
        circuito = c.circuit(netlistFileName)
        circuito.setFrequence()
        circuito.setCircuitSystem()
        print("\033[1;32;40mCircuitMatrixSystem")
        circuito.getCircuitMatrixSystem()
        print("\033[1;34;40mMatrixIn")
        circuito.getMatrixIn()
        print("\033[1;33;40mSystem solution")
        circuito.solveSystem()
        control = input("\033[1;37;40mSolve another system?  Press \033[1;31;40m[y] \033[1;37;40mfor yes:\n")
        if (control != "y"):
           print("Exiting...")
           key = False