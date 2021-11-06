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
    with open(fname, 'r') as tcgpFile:
        for line in tcgpFile:
            cid = getID(line[2:len(line)].rstrip())
            parsedTCGP.append((cid, line[0]))
    return parsedTCGP

def ConvertToYDK(parsedTCGP, fname):
    newName = fname[:len(fname)-4] + ".ydk"
    ydkFile = open(newName, "w+")
    ydkFile.write("#extra\n")
    firstDiv = True
    i = 0
    while i < len(parsedTCGP):
        multi = 0
        if parsedTCGP[i][0] != -1:
            while(multi < int(parsedTCGP[i][1])):
                ydkFile.write(str(parsedTCGP[i][0])+'\n')
                multi += 1
        else:
            if firstDiv:
                i += 1
                ydkFile.write("\n#main\n")
                firstDiv = False
            else:
                i += 1
                ydkFile.write("\n!side\n")
        i += 1


def main():
    fname = input("TCGPlayer text file name or path: ")
    cidList = ConvertNamesToID(fname)
    ConvertToYDK(cidList, fname)
    print("File converted successfully!")

if __name__ == "__main__":
    main()  
