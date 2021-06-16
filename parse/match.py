class Match:
    def __init__(self, result, score, agent, map):
        self.result = result    # bool
        self.score = score      # list
        self.agent = agent      # String
        self.map = map          # String
        self.matchStats = {}    # Dict

    def getResult(self):
        return self.result

    def getScore(self):
        return str(self.score[0]) + "-" + str(self.score[1])

    def getAgent(self):
        return self.agent

    def getMap(self):
        return self.map

    def getKDA(self):
        return self.matchStats["KDA"]

    def setKDA(self, k,d,a):
        self.matchStats["KDA"] = str(k) + "/" + str(d) + "/" + str(a)

    def getADR(self):
        return self.matchStats["ADR"]

    def setADR(self, adr):
        self.matchStats["ADR"] = round(adr)

    def getHS(self):
        return str(self.matchStats["HS"]) + "%"

    def setHS(self, hs):
        self.matchStats["HS"] = hs

if __name__ == "__main__":
    match = Match(True, [13,11], "Reyna", "Haven")
    match.setKDA(7,1,1)
    test = 1