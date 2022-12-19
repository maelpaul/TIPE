# deleting a line matching a specific pattern or containing a specific string

def find_pattern(line):
    L1 = ['0E', '1E', '2E', '3E', '4E', '5E', '6E', '7E', '8E', '9E'] #retire les degrés Est de la base de données
    L2 = ['0S', '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S'] #retire les degrés Sud de la base de données
    for i in range(len(L1)):
        if (line.find(L1[i]) != -1):
            return 0
    for i in range(len(L2)):
        if (line.find(L2[i]) != -1):
            return 0
    return -1

try:
    with open('draft_base.txt', 'r') as db:
        lines = db.readlines()
        with open('base.txt', 'w') as b:
            for line in lines:
                # find_pattern(line) returns -1 if no match found
                if find_pattern(line) == -1:
                    b.write(line)
except:
    print("Error")
