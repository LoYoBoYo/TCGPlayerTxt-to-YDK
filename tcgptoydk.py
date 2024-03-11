import requests
from urllib.parse import quote_plus

def getID(cname, api_json):
    for card in api_json["data"]:
        if cname.lower() == card["name"].lower():
            return card["id"]
    return -1

def build_request_url(cnames):
    base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="
    url_parts = [quote_plus(cname) for cname in cnames]
    return base_url + "|".join(url_parts)

def send_api_request(url):
    response = requests.get(url)
    response.raise_for_status()  # raise an exception if the request failed
    return response.json()

def check_file_extension(fname):
    if not fname.endswith(".txt"):
        raise ValueError(f"Not a TCGPlayer txt file or you missed the file extension for {fname}!")

def ConvertNamesToID_New(fname):
    parsedTCGP = []
    cnames = []

    try:
        with open(fname, 'r') as tcgpFile:
            for line in tcgpFile:
                cname = line[2:len(line)].rstrip()
                cnames.append(cname)
                parsedTCGP.append([cname, line[0]])
    except OSError:
        print(f"Can't open {fname}!\nCheck name/path spelling, file is from TCGPlayer or make sure the file exists.")
        exit(1) 

    request_URL = build_request_url(cnames)
    api_json = send_api_request(request_URL)
    for card in parsedTCGP:
        card[0] = getID(card[0], api_json)

    return parsedTCGP

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

def write_to_file(ydkFile, section, cards):
    ydkFile.write(f"{section}\n")
    for card in cards:
        ydkFile.write((str(card[0]) + '\n') * int(card[1]))
    ydkFile.write('\n')

def ConvertDecktionaryToYDK(decktionary, fname):
    YDK_ORDER = ["#main", "#extra", "!side"]
    newName = fname[:len(fname)-4] + ".ydk"
    with open(newName, "w+") as ydkFile:
        for section in YDK_ORDER:
            write_to_file(ydkFile, section, decktionary[section])

def main():
    fnames = input("TCGPlayer text file names or paths (comma separated for multiple): ")
    fnames = fnames.split(',')

    for fname in fnames:
        fname = fname.strip()  # remove leading and trailing whitespaces
        try:
            check_file_extension(fname)
            cidList = ConvertNamesToID_New(fname)
            decktionary = ListToDecktionary(cidList)
            ConvertDecktionaryToYDK(decktionary, fname)
            print(f"File {fname} converted successfully!")
        except Exception as e:
            print(f"Failed to convert {fname}. Error: {str(e)}")

if __name__ == "__main__":
    main()