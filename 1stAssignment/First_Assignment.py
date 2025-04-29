import numpy as np
#import pandas as pd
import ast

def read_bap_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line for dimensions
        while True:
            line = file.readline().strip().split()
            if (line[0]=='#'):
                continue
            else:
                s = int(line[0])
                n = int(line[1])
                break
        
        # Initialize an empty BAP matrix
        bap_matrix = []
        ai = []
        pi = []
        si = []
        wi = []
        
        # Read the matrix values
        for _ in range(n):
            row = list(map(int, file.readline().strip().split()))
            bap_matrix.append(row)
            ai.append(row[0])  # Adiciona o primeiro valor à lista ai
            pi.append(row[1])  # Adiciona o segundo valor à lista pi
            si.append(row[2])  # Adiciona o terceiro valor à lista si
            wi.append(row[3])  # Adiciona o quarto valor à lista wi

    return s, n, bap_matrix, ai, pi, si, wi



#Inicializa as variáveis chamando a função corretamente
s, n, bap_matrix, ai, pi, si, wi = read_bap_file('ex100.dat')
print('Berth Size: ', s)
print('Number of Vessels: ', n)
print('Matriz BAP:', bap_matrix)
print('ai =', ai)
print('pi =', pi)
print('si =', si)
print('wi =', wi)

#Read Output file and determine cost function

def process_array(output_file):
    ui = []
    vi = []

    with open(output_file, 'r') as file:
        # Ler o conteúdo do arquivo
        solution = file.read().strip()
        # Converte o conteúdo para um array
        array = ast.literal_eval(solution)

#Itera sobre o array e armazena os valores
        for variables in array:
            ui.append(variables[0])  # Pega o primeiro valor e adiciona à lista ui
            vi.append(variables[1])  # Pega o segundo valor e adiciona à lista vi

    return ui, vi

#Chama a função para processar o arquivo de output
output_file = 'ex100.plan'
ui, vi = process_array(output_file)

#Exemplo de impressão das listas resultantes
print("ui =", ui)
print("vi =", vi)


#Initialize the list to store results
ci = []
fi = []
wi_fi_product = []
flow = 0

#Ensure that both lists are of the same length
if len(ui) == len(pi):
    for i in range(len(ui)):
        ci.append(ui[i] + pi[i])
        fi.append(ci[i] - ai[i])
        wi_fi_product.append(wi[i] * fi[i])
else:
    print("Error: Lists have different lengths!")

def check(self,sol):

    #Ensure that the number of vessels is equal to the number of tuples of the output
    if (len(ui)!=n):
        print("Contrainsts broken - number of vessels of the input is not equal to the output.")
        return False


    # Mooring time must begin at or after the arrival time
    if (len(ui) != len(ai)):
            print("Error: Lists have different lengths!")
            return False
    else:
        for i in range(len(ai)):
            if ui[i] < ai[i]:
                print("Contrainsts broken - mooring time before arrival time.")
                return False
        check = 1

    # Check to see whether berth section for each vessel is valid
    for i in range(len(vi)):
        if (vi[i] < 0) or (vi[i] > (s - si[i])):
            print("Contraints broken - berth section outside of quay.")
            return False
    check = 1

    for i in range(len(vi)):

        ind = i
        l_range_ubound = vi[i] + si[i] - 1    #length range 
        l_range_lbound = vi[i]
        while ind < (len(ui) - 1):
            ind+=1
            if(vi[ind]<=l_range_ubound and vi[ind]>=l_range_lbound):
                check = 0
                if (check == 0):
                    t_range_ubound = ui[i] + pi[i] - 1   #time range
                    t_range_lbound = ui[i]
                    if (ui[ind]<=t_range_ubound and ui[ind]>=t_range_lbound):
                        print("Contraints broken - Overlap of vessels.")
                        return False
                    else:
                        check = 1
    check = 1
    if (check==1):
        return True










flow = sum(wi_fi_product)

#Print the resulting list
print("ci =", ci)
print("fi =", fi)
print("wi*fi", wi_fi_product)
print('flow', flow )
