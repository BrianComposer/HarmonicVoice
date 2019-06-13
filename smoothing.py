from ngram import *

class Smoothing:

    def smoothingLaplaceBigramZERO(self, unigram, bigram, alfa):
        laplace = {}
        N = 0.0
        d = 0.0
        for token1 in unigram:
            N = 0.0
            for token2 in unigram:
                grm = (token1, token2)
                if grm in bigram:
                    N = N + bigram[grm]
            d = d + 1.0
            laplace[token1] = alfa / (N + alfa * d)
        return laplace

    def smoothingLaplaceTrigramZERO(self, unigram, trigram, alfa):
        laplace = {}
        N = 0
        d = 0
        for token1 in unigram:
            for token2 in unigram:
                N = 0
                for token3 in unigram:
                    grm = (token1, token2, token3)
                    if grm in trigram:
                        N = N + trigram[grm]
                d = d + 1
                laplace[(token1, token2)] = alfa / (N + alfa * d)
        return laplace

    def calculateBigramProbabilityLaplace(self, unigram, bigram, alfa):
        ng = Ngram()
        bigrm_prob = {}
        bigrmBuf = {}
        N = 0.0
        d = len(unigram)
        for token in unigram:
            N = 0.0
            bigrmBuf = ng.subBiGram(bigram, token)
            for t in bigrmBuf:
                N = N + bigrmBuf[t]

            for t in bigrmBuf:
                bigrm_prob[t]= ( bigrmBuf[t] + alfa ) / ( N + alfa * d)
        return bigrm_prob

    def calculateTrigramProbabilityLaplace(self, unigram, trigram, alfa):
        ng = Ngram()
        trigrm_prob = {}
        trigrmBuf = {}
        N = 0.0
        d = len(unigram) * len(unigram)
        for token1 in unigram:
            for token2 in unigram:
                N = 0.0
                trigrmBuf = ng.subTriGram(trigram, token1, token2)
                for t in trigrmBuf:
                    N = N + trigrmBuf[t]

                for t in trigrmBuf:
                    trigrm_prob[t]= ( trigrmBuf[t] + alfa ) / ( N + alfa * d)
        return trigrm_prob
