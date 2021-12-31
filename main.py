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
    for elem in data:
        if elem.get("name") == name:
            return elem


def parseCommits(data):
    datedict = {}
    for elem in data:
        # print(elem["commit"])
        shortdate = elem["commit"]["author"]["date"].split('T')[0]
        if shortdate in datedict.keys():
            datedict[shortdate] += 1
        else:
            datedict[shortdate] = 1
    #     print(shortdate)
    print(datedict)
    return datedict


def graph(data):
    xAxis = sorted(data.keys())

    plt.plot(xAxis, [data[x] for x in xAxis])
    plt.show()


if __name__ == "__main__":
    uresponseAPI = requests.get('https://api.github.com/users/' + userIOQuery())
    # print(responseAPI.status_code)
    if (uresponseAPI.status_code == 200):
        udataRaw = uresponseAPI.text
        # print(udataRaw)
        udataJS = json.loads(udataRaw)
        # print("ID: " + str(udataJS['id']))
        rresponseAPI = requests.get(udataJS['repos_url'])
        # print(rresponseAPI.status_code)
        if (rresponseAPI.status_code == 200):
            rdataRaw = rresponseAPI.text
            rdataJS = json.loads(rdataRaw)
            # print(json.dumps(rdataJS, sort_keys=True, indent=4))
            repoData = (parseRepo(rdataJS, repoIOQuery()))
            # print(repoData)
            # print(repoData["commits_url"][:-6])
            cresponseAPI = requests.get(repoData["commits_url"][:-6])
            # print(cresponseAPI.text)
            cdata = json.loads(cresponseAPI.text)
            # print(json.dumps(cdata, indent=4))
            dateData = parseCommits(cdata)
            graph(dateData)


        else:
            print("Invalid repo name.")

    else:
        print("Invalid query.")
