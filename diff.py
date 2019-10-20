from sys import argv

def main():
  with open(argv[2], 'w') as outFile:
    with open(argv[1]) as inFile:
      for line in inFile:
        line = line.split() # Faz um split na string usando os espaços e retorna uma lista
        diff = float(line[1]) - float(line[2]) # Fazendo a diferença
        line.append(str(diff)) # Adicionando a diferença na lista
        outFile.write(' '.join(line) + '\n') # ' '.join(line) --> converter lista para string separando por espaços

if __name__ == '__main__':
  main()
