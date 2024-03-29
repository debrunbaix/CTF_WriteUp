FILE = 'desired_output.txt'

result = ""

with open(FILE, 'r') as fichier:
    addresses = fichier.readlines()

    for raw in addresses:
        index = raw.split()[1]
        if str(index) != '00':  # Vérifier si la valeur est différente de '00'
            result += f" {str(index)},"  # Ajouter la valeur à la chaîne de résultat si la condition est vraie

print(result)
