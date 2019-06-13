from music21 import *
import nltk
import glob
import operator
import fileIO
import smoothing
import ngram
import rawData

class Parsing:
    def startParsing(self, composerName, mode, maxTokens):
        try:
            #INICIALIZAR LAS CLASES
            fio = fileIO.FileIO()
            ng = ngram.Ngram()
            lp = smoothing.Smoothing()

            #LEER LOS DATOS EN CRUDO
            print(">>> Reading data raw")

            fileNames = fio.getFileNames(composerName, mode)
            dataRawFile = fileNames[0]
            dataRaw = fio.readText('raw/'+ dataRawFile)

##            TOKENIZACION
            print(">>> Tokenization")
            tokens = ng.getTokens(dataRaw)
##            printFrequencyChart(tokens)
##            return "ok"

##            STOP WORDS
            print(">>> Removing stop words")
            tokens = ng.removeStopWords(tokens)
##            GRAFICAS DE FRECUENCIAS
##            printFrequencyChart(tokens)

            #FILTRADO DE LOS MAS FECUENTES
            print(">>> Filtering " + str(maxTokens) +" most frequent tokens")
            tokens = ng.filterMostFrequentTokens(tokens, maxTokens)

##            UNIGRAMA
            print(">>> Counting unigram")
            unigram_count = ng.getUnigram(tokens)
            print(">>> Saving unigram")
            fio.save_obj(unigram_count, fileNames[5])

##            BIGRAMA
            print(">>> Counting bigram")
            bigram_count = ng.getBigram(tokens)
            bigram_prob = ng.calculateBigramProbability(unigram_count, bigram_count)

##            TRIGRAMA
            print(">>> Counting trigram")
            trigram_count = ng.getTrigram(tokens)
            trigram_prob = ng.calculateTrigramProbability(unigram_count, trigram_count)

##            SMOOTHING
            alfa = 0.0001
##            hacer mencion a un trabajo anterior el paper que indica una tecnica de smoothing apropiada
            print(">>> Laplace smoothing of bigram")
            bigram_prob_Laplace = lp.calculateBigramProbabilityLaplace(unigram_count, bigram_count, alfa)
            unigram_ZERO = lp.smoothingLaplaceBigramZERO(unigram_count, bigram_count, alfa)

            print(">>> Laplace smoothing of trigram")
            trigram_prob_Laplace = lp.calculateBigramProbabilityLaplace(unigram_count, trigram_count, alfa)
            bigram_ZERO = lp.smoothingLaplaceTrigramZERO(unigram_count, trigram_count, alfa)


            print(">>> Saving bigram")
            fio.save_obj(bigram_prob_Laplace, fileNames[1])
            fio.save_obj(unigram_ZERO, fileNames[3])

            print(">>> Saving trigram")
            fio.save_obj(trigram_prob_Laplace, fileNames[2])
            fio.save_obj(bigram_ZERO, fileNames[4])


            #PROCESO FINALIZADO
            print(">>> Process finished OK")
        except:
            print(">>> Process failed")

    def extractDataRaw(self):
        fio = fileIO.FileIO()
        rw = rawData.RawDataExtractor()

##        obras = corpus.getComposer('bach', 'xml')
##        obras =  glob.glob("D:\BackUpDrive\Documentos\Masters\Master IA UNED\TFM\corpus\jazz\*.xml")
##        obras = corpus.getComposer('monteverdi', 'mxl')
####        SOLO CONTIENEN MELODIAS
##        obras = corpus.getComposer('essenFolksong')
##        obras = corpus.getComposer('oneills1850')
##        obras = corpus.getComposer('ryansMammoth')
        composer = "bach"
        obras = corpus.getComposer(composer)

##        PARSING DE LAS OBRAS
##        dataRaw = rw.getRawDataH(obras[0:300])
##        fio.writeText(dataRaw[0] , 'raw/'+ fio.getFileNames(composer, "M")[0])
##        fio.writeText(dataRaw[1] , 'raw/'+ fio.getFileNames(composer, "m")[0])
        dataRawR = rw.getRawDataR(obras[0:100])

        fio.writeText(dataRawR[0], 'raw/'+ fio.getFileNames(composer, "R")[0])