import functools

import requests
import json
import matplotlib.pyplot as plt


@functools.total_ordering
class simpledate:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return "{:0>2}-{:0>2}".format(self.month, self.day)

    def __lt__(self, other):
        if self.year == other.year:
            if self.month == other.month:
                return self.day < other.day
            else:
                return self.month < other.month
        else:
            return self.year < other.year

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __hash__(self):
        return self.year * 100000 + self.month * 10 + self.day

    def get_increment(self):
        day = self.day + 1
        month = self.month
        year = self.year
        if month == 2 and day > 28:
            if not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                month = 3
                day = 1
        elif (day > 31) or (day == 31 and month in [4, 6, 9]):
            month += 1
            day = 1
        if month > 12:
            month = 1
            year += 1
        return simpledate(year, month, day)

    def date_span(self, other):
        currDate = self.get_increment()
        span = []
        while currDate != other:
            span.append(currDate)
            currDate = currDate.get_increment()
        return span


def user_io_query():
    username = input("Please input a valid github username.")
    return username


def repo_io_query(repoList):

    repoNum = int(input("Please input a valid github repo."))
    return repoList[repoNum]


def parse_repo(data, name):
    for elem in data:
        if elem.get("name") == name:
            return elem


def parse_commits(data):
    datedict = {}
    for elem in data:
        # print(elem["commit"])
        shortdate = elem["commit"]["author"]["date"].split('T')[0]
        vals = shortdate.split('-')
        date = simpledate(int(vals[0]), int(vals[1]), int(vals[2]))

        if date in datedict.keys():
            datedict[date] += 1
        else:
            datedict[date] = 1
    #     print(shortdate)
    return datedict


def graph(data, repoName):
    xAxis = sorted(data.keys())
    xNames = [str(x) for x in xAxis]
    plt.bar(xNames, [data[x] for x in xAxis])
    plt.xlabel("Dates")
    plt.ylabel("Commits")
    plt.title("Commits over Time for " + repoName)
    plt.show()


if __name__ == "__main__":
    uresponseAPI = requests.get('https://api.github.com/users/' + user_io_query())
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
            repoList = []
            i = 0
            for elem in rdataJS:
                name = elem.get("name")
                print("{}: {}".format(i, name))
                repoList.append(name)
                i+=1
            # print(json.dumps(rdataJS, sort_keys=True, indent=4))
            repoData = (parse_repo(rdataJS, repo_io_query(repoList)))
            # print(repoData)
            # print(repoData["commits_url"][:-6])
            cresponseAPI = requests.get(repoData["commits_url"][:-6])
            # print(cresponseAPI.text)
            cdata = json.loads(cresponseAPI.text)
            # print(json.dumps(cdata, indent=4))
            dateData = parse_commits(cdata)
            dates = [x for x in sorted(dateData.keys())]
            missingDates = set()
            for i in range(len(dates) - 1):
                out = str(dates[i]) + ", "
                spanDates = dates[i].date_span(dates[i + 1])
                for elem in spanDates:
                    out += str(elem) + ", "
                    missingDates.add(elem)
                out += str(dates[i + 1])
                print(out)
            for elem in missingDates:
                dateData[elem] = 0
            graph(dateData, repoData["name"])



        else:
            print("Invalid repo name.")

    else:
        print("Invalid query.")
