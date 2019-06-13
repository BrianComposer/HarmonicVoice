from music21 import *
import composer
import fileIO
import ngram
import parsing



##p = parsing.Parsing()
##p.extractDataRaw()
##p.startParsing("bach","R", 50)

##fio = fileIO.FileIO()
##unigram = fio.load_obj(fio.getFileNames("jazz", "r")[5])
##ng = ngram.Ngram()
##ng.printFrequencyChart(unigram)



comp = composer.Composer()
for i in range(100):
    try:
##        res = comp.composeABA_bach(key.Key('C'), "major")
        res = comp.composePhraseChoral("bach", key.Key('C'), "major")
        sco = comp.generateScore(res[0], res[1], key.Key('C'))
        sco.write("xml", fp="D:\\BackUpDrive\\Documentos\\Masters\\Master IA UNED\\TFM\\Codigo\\results\\bach\\bach" + str(i) + ".xml" )
        sco.show()
        print("Generando..." + str(i))
    except Exception as e:
        print("Error..." + str(i) + " " + str(e))








