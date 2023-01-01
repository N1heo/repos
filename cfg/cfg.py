
with open("configtipa.txt", 'r', encoding='ISO-8859-1') as input_file:
    lines = input_file.read().splitlines()
with open("configtipa.txt", "w", encoding='ISO-8859-1') as output:
    for line in lines:
        a=len(line)
        output.write(line+';')
        
print('Файл изменился')