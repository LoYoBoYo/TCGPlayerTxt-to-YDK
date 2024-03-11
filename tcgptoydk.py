import requests
from urllib.parse import quote_plus

'''
TCGPlayerTxt-to-YDK REDUX
What's New?:
- Internal data structure overhaul 
- API request overhaul
- Added comments :D
'''

def getID(cname, api_json):
    for card in api_json["data"]:
        if cname.lower() == card["name"].lower():
            return card["id"]
    return -1

def ConvertNamesToID_New(fname):
    request_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="
    parsedTCGP = []
    
    #Open file to read, create api request URL and create intermidiary list before name-to-ID
    try:
        with open(fname, 'r') as tcgpFile:
            for line in tcgpFile:
                cname = line[2:len(line)].rstrip()
                request_URL += f"{quote_plus(cname)}|"
                parsedTCGP.append([cname, line[0]])
    
    except OSError:
        print(f"Can't open {fname}!\nCheck name/path spelling, file is from TCGPlayer or make sure the file exists.")
        exit(1) 

    #Condensed API call and name-to-ID conversion 
    request_URL = request_URL[:-1]
    api_get = requests.get(request_URL)
    api_json = api_get.json()
    for card in parsedTCGP:
        card[0] = getID(card[0], api_json)

    return parsedTCGP

def ListToDecktionary(parsedTCGP):
    #This function only exits to compensate for Dueling Book refusing to properly import YDK files with content in a different order.
    #Makes reorganizing the final file easier.
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
    fnames = input("TCGPlayer text file names or paths (comma separated for multiple): ")
    fnames = fnames.split(',')

    for fname in fnames:
        fname = fname.strip()  # remove leading and trailing whitespaces
        if fname[len(fname)-4:] != ".txt":
            print(f"Not a TCGPlayer txt file or you missed the file extension for {fname}!")
            continue

        try:
            cidList = ConvertNamesToID_New(fname)
            decktionary = ListToDecktionary(cidList)
            ConvertDecktionaryToYDK(decktionary, fname)
            print(f"File {fname} converted successfully!")
        except Exception as e:
            print(f"Failed to convert {fname}. Error: {str(e)}")


if __name__ == "__main__":
    main()  