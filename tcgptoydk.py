import requests

api_get = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
api_json = api_get.json()

def getID(cname):
    for card in api_json["data"]:
        if cname.lower() == card["name"].lower():
            return card["id"]
    return -1

def ConvertNamesToID(fname):
    parsedTCGP = []
    try:
        with open(fname, 'r') as tcgpFile:
            for line in tcgpFile:
                cid = getID(line[2:len(line)].rstrip())
                parsedTCGP.append((cid, line[0]))
        return parsedTCGP

    except OSError:
        print(f"Can't open {fname}!\nCheck spelling or make sure the file exists.")
        exit(1)

def ListToDecktionary(parsedTCGP):
    TCGP_ORDER = ["#extra","#main","!side"]
    decktionary = {"#extra":[],"#main":[],"!side":[]}
    i = 0
    if parsedTCGP[0][0] == -1:
        print("Seems like the file is not in the correct format, only txt files from TCGPlayer will work.")
        exit(1)

    for section in TCGP_ORDER:     
        while i < len(parsedTCGP) and parsedTCGP[i][0] != -1:
            decktionary[section].append(parsedTCGP[i])
            i += 1
        i += 2
    return decktionary

def ConvertDecktionaryToYDK(decktionary, fname):
    YDK_ORDER = ["#main", "#extra", "!side"]
    newName = fname[:len(fname)-4] + ".ydk"
    with open(newName, "w+") as ydkFile:
        for section in YDK_ORDER:
            ydkFile.write(f"{section}\n")
            for card in decktionary[section]:
                multi = 0
                while(multi < int(card[1])):
                    ydkFile.write(str(card[0])+'\n')
                    multi += 1
            ydkFile.write('\n')

def main():
    fname = input("TCGPlayer text file name or path: ")
    if fname[len(fname)-4:] != ".txt":
        print("Not a TCGPlayer txt file or you missed the file extension!")
        exit(1)
    cidList = ConvertNamesToID(fname)
    decktionary = ListToDecktionary(cidList)
    ConvertDecktionaryToYDK(decktionary, fname)
    print("File converted successfully!")

if __name__ == "__main__":
    main()  
