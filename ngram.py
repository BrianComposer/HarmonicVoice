import nltk
import random

class Ngram:

    def getTokens(self, text):
        tokens = [t for t in text.split()]
        return tokens

    def printFrequencyChart(self, tokens):
        freq = nltk.FreqDist(tokens)
        freq.plot(50, cumulative=False)

    def removeStopWords(self, tokens):
        stopWords = []
        newTokens = []
        with open("stopWords.txt", "rt") as f:
            for line in f:
                value = line.replace("\n", "")
                stopWords.append(value)
        for token in tokens:
            if not token in stopWords:
                newTokens.append(token)
        return newTokens

    def filterMostFrequentTokens(self, tokens, maxnumber):
        freq = nltk.FreqDist(tokens)
        filterTokens = []
        newTokens = []
        for t in freq:
            if(len(filterTokens) < maxnumber):
                filterTokens.append(t)
        for t in tokens:
            if t in filterTokens:
                newTokens.append(t)
        return newTokens

    def getUnigram(self, tokens):
        unigrm_count = {}
        for token in tokens:
            if token not in unigrm_count:
                unigrm_count[token] = 1
            else:
                unigrm_count[token] += 1
        return unigrm_count

    def getBigram(self, tokens):
        bigrm = nltk.bigrams(tokens)
        bigrm_count = {}
        for grm in bigrm:
            if grm not in bigrm_count:
                bigrm_count[grm] = 1
            else:
                bigrm_count[grm] += 1
        return bigrm_count

    def getTrigram(self, tokens):
        trigrm = nltk.trigrams(tokens)
        trigrm_count = {}
        for grm in trigrm:
            if grm not in trigrm_count:
                trigrm_count[grm] = 1
            else:
                trigrm_count[grm] += 1
        return trigrm_count

    def calculateBigramProbability(self, unigram, bigram):
        bigrm_prob = {}
        bigrmBuf = {}
        for token in unigram:
            buf = 0.0
            bigrmBuf = self.subBiGram(bigram, token)
            for t in bigrmBuf:
                buf = buf + bigrmBuf[t]

            for t in bigrmBuf:
                bigrm_prob[t]= bigrmBuf[t] / buf
        return bigrm_prob

    def calculateTrigramProbability(self, unigram, trigram):
        trigrm_prob = {}
        trigrmBuf = {}
        for token1 in unigram:
            for token2 in unigram:
                buf = 0.0
                trigrmBuf = self.subTriGram(trigram, token1, token2)
                for t in trigrmBuf:
                    buf = buf + trigrmBuf[t]

                for t in trigrmBuf:
                    trigrm_prob[t]= trigrmBuf[t] / buf
        return trigrm_prob

    def subBiGram(self, dict, token):
        newDict = {}
        for value in dict:
            if(value[0]==token):
                newDict[value] = dict[value]
        return newDict

    def subTriGram(self, dict, token1, token2):
        newDict = {}
        for value in dict:
            if(value[0]==token1 and value[1]==token2):
                newDict[value] = dict[value]
        return newDict

    def getRandomTuple(self, subGram):
        r = 0.0
        buf = 0.0
        probabilities = []
        keys = list(subGram.keys())
        for i in range(len(subGram.keys())):
            buf = buf + subGram[keys[i]]
            probabilities.append(buf)

    ##    Case probability = 0, all are equiprobable
        if (buf == 0):
            if (keys is None or len(keys)==0):
                return subGram
            else:
                return random.choice(keys)[-1]
        elif (len(probabilities)==1):
            return keys[0][-1]
        else:
            r = random.random()
        for i in range(len(probabilities)):
            if(i==0):
                if (r <= probabilities[i]):
                    return keys[0][-1]
            elif(i == len(probabilities) - 1):
                if (r >= probabilities[i - 1]):
                    return keys[i][-1]
            else:
                if ((r >= probabilities[i - 1]) and (r <= probabilities[i])):
                     return keys[i][-1]
        return "-1"

