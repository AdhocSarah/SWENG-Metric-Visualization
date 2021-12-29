
import requests
import json
import matplotlib.pyplot as plt


def userIOQuery():
    # Todo: add user interactivity - ask for user info
    # print("Please input a valid github username.")
    username = "adhocsarah"
    return username

def repoIOQuery():
    # Todo: add user interactivity - ask for repo info
    # print("Please input a valid github repo.")
    reponame = "SWENG-Metric-Visualization"
    return reponame

def parseRepo(data, name):
    return [x for x in data if x["name"] == name]


def parseCommits(data):
    # dates = [elem["commit"]["date"] for elem in data]
    # print(dates)
    commitData = []






if __name__ == "__main__":
    uresponseAPI = requests.get('https://api.github.com/users/'+userIOQuery())
    #print(responseAPI.status_code)
    if (uresponseAPI.status_code == 200):
        udataRaw = uresponseAPI.text
        #print(udataRaw)
        udataJS = json.loads(udataRaw)
        print("ID: " + str(udataJS['id']))
        rresponseAPI = requests.get(udataJS['repos_url'])
        # print(rresponseAPI.status_code)
        if (rresponseAPI.status_code == 200):
            rdataRaw = rresponseAPI.text
            rdataJS = json.loads(rdataRaw)
            # print(json.dumps(rdataJS, sort_keys=True, indent=4))
            repoData = parseRepo(rdataJS, repoIOQuery())
            print(json.dumps(repoData, sort_keys=True, indent=4))
            parseCommits(repoData)



        else:
            print("Invalid repo name.")

    else:
        print("Invalid query.")
