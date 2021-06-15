import json

fileName = "C:/Users/Darryl/Documents/Python Projects/Valorant Discord Bot/utils/userData.json"

def load():
    with open(fileName) as data:
        return json.load(data)

def add(userID, valID):
    with open(fileName, "r+") as file:
        data = json.load(file)
        data[str(userID)] = {"valorantTag": valID}
        file.seek(0)
        json.dump(data, file, indent=4)
    return True

def getValTag(userID):
    jsonDict = load()
    userInfo = jsonDict.get(userID)
    if userInfo is None: return None
    else:
        return userInfo.get("valorantTag")


if __name__ == "__main__":
    print(getValTag("281373001251815425"))
    # add(281373001251815425, "darryl%237534")
    # add(226987652165926913, "Nogh25%23OCE")