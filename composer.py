from music21 import *
import nltk
import glob
import random
import pickle
import fileIO
from datetime import datetime
import operator
import ngram
from  melody import *
from rhythm import *
from harmony import *

class Composer:
    def generateScore(self, chords, melody, tonality):
        s1 = stream.Stream()
        p1 = stream.Part()
        k1 = tonality
        p1.append(k1)
        p1.insert(0, instrument.Flute())
        if(melody is not None):
            for m in melody:
                p1.append(m)
            s1.append(p1)
        p2 = stream.Part()
        p2.append(k1)
        p2.insert(0, instrument.Piano())
        for c in chords:
            p2.append(c)
        s1.append(p2)
        return s1

    def composePhrase(self, composerName, tonality, mode, firstH, secondH, firstR, secondR, anacruse):
        dt = datetime.now()
        random.seed(dt.microsecond)
        fio = fileIO.FileIO()
        h = Harmony()
        rt = Rhythm()
        ml = Melody()
        iteration = 0

        #De momento solo funciona en 4 por 4
        beats_per_measure = 4
        #Longitud en compases de la frase
        fraseLenght = 8
        semifraseLenght = int(fraseLenght / 2)
        ritmoLenght = int(beats_per_measure * fraseLenght / 4)

        durationChord = "quarter"
        if durationChord == "whole":
            numberOfChords = int(1 * semifraseLenght)
        elif durationChord == "half":
            numberOfChords = int(2 * semifraseLenght)
        elif durationChord == "quarter":
            numberOfChords = int(4 * semifraseLenght)
        elif durationChord == "eight":
            numberOfChords = int(8 * semifraseLenght)

        fio.getFileNames(composerName, mode)

        unigram = fio.load_obj(fio.getFileNames(composerName, mode)[5])
        bigram = fio.load_obj(fio.getFileNames(composerName, mode)[1])
        bigram_R = fio.load_obj(fio.getFileNames(composerName, "R")[1])
        trigram = fio.load_obj(fio.getFileNames(composerName, mode)[2])
        trigram_R = fio.load_obj(fio.getFileNames(composerName, "R")[2])

        unigram_s = sorted(unigram.items(), key=operator.itemgetter(1), reverse=True)
        cadenceOK = False

        iteration = 0
        while not cadenceOK:
            chords_A1 = h.getHarmony_from_Trigram(trigram, bigram, tonality, firstH, numberOfChords, durationChord)
            if "v" in chords_A1[1][-1].lower():
                cadenceOK = True
            elif "iv" in chords_A1[1][-1].lower():
                cadenceOK = True
            if "vi" in chords_A1[1][-1].lower():
                cadenceOK = True
            iteration +=1
            if iteration == 100: raise Exception("Error in the process: to many trials")

        iteration = 0
        cadenceOK = False
        while not cadenceOK:
            chords_A2 = h.getHarmony_from_Trigram(trigram, bigram, tonality, secondH, numberOfChords, durationChord)
            if "i" == chords_A2[1][-1].lower():
                cadenceOK = True
            iteration +=1
            if iteration == 100: raise Exception("Error in the process: to many trials")

        rimto1 = None
        iteration = 0
        while (rimto1 is None):
            rimto1 = rt.getRhythm_from_Trigram(trigram_R, firstR, secondR, ritmoLenght, anacruse, 0)
            iteration +=1
            if iteration == 100: raise Exception("Error in the process: to many trials")

        rimto1b = None
        iteration = 0
        while (rimto1b is None):
            rimto1b = rt.getRhythm_from_Trigram(trigram_R, firstR, secondR, ritmoLenght, False, 1.0)
            iteration +=1
            if iteration == 100: raise Exception("Error in the process: to many trials")

        rimto1c = None
        iteration = 0
        while (rimto1c is None):
            rimto1c = rt.getRhythm_from_Trigram(trigram_R, firstR, secondR, ritmoLenght, False, 2.0)
            iteration +=1
            if iteration == 100: raise Exception("Error in the process: to many trials")


        ritmoCompleto = []
        for r in rimto1[0]:
            ritmoCompleto.append(r)
        for r in rimto1b[0]:
            ritmoCompleto.append(r)
        for r in rimto1[0]:
            ritmoCompleto.append(ml.cloneFigure(r))
        for r in rimto1c[0]:
            ritmoCompleto.append(r)

        acordesCompleto = []
        for c in chords_A1[0]:
            acordesCompleto.append(c)
        for c in chords_A2[0]:
            acordesCompleto.append(c)

        melodyGenerated = ml.rhythm_to_Melody(ritmoCompleto, acordesCompleto)
        print(str(chords_A1[1]) + str(chords_A2[1]))
        return [acordesCompleto, melodyGenerated]



    def composePhraseChoral(self, composerName, tonality, mode):
        dt = datetime.now()
        random.seed(dt.microsecond)
        fio = fileIO.FileIO()
        h = Harmony()
        rt = Rhythm()
        ml = Melody()
        iteration = 0

        #De momento solo funciona en 4 por 4
        beats_per_measure = 4
        #Longitud en compases de la frase
        fraseLenght = 4
        semifraseLenght = int(fraseLenght / 2)
        ritmoLenght = int(beats_per_measure * fraseLenght)

        durationChord = "quarter"
        if durationChord == "whole":
            numberOfChords = int(1 * fraseLenght)
        elif durationChord == "half":
            numberOfChords = int(2 * fraseLenght)
        elif durationChord == "quarter":
            numberOfChords = int(4 * fraseLenght)
        elif durationChord == "eight":
            numberOfChords = int(8 * fraseLenght)

        fio.getFileNames(composerName, mode)

        unigram = fio.load_obj(fio.getFileNames(composerName, mode)[5])
        bigram = fio.load_obj(fio.getFileNames(composerName, mode)[1])
        bigram_R = fio.load_obj(fio.getFileNames(composerName, "R")[1])
        trigram = fio.load_obj(fio.getFileNames(composerName, mode)[2])
        trigram_R = fio.load_obj(fio.getFileNames(composerName, "R")[2])

        unigram_s = sorted(unigram.items(), key=operator.itemgetter(1), reverse=True)
        isOK = False

        iteration = 0
        while not isOK:
            chordsA = h.getHarmony_from_Trigram(trigram, bigram, tonality, "I", numberOfChords, durationChord)
            if "II" in chordsA[1][-2] and "V" in chordsA[1][-1]:
                isOK = True
            iteration +=1
            if iteration == 1000: raise Exception("Error in the process A: to many trials")
        print("harmony A..... OK")
        iteration = 0
        isOK = False
        while not isOK:
            chordsB = h.getHarmony_from_Trigram(trigram, bigram, tonality, "I6", numberOfChords, durationChord)
            if chordsB[1][-2]=="V" and chordsB[1][-1]=="I":
                isOK = True
            iteration +=1
            if iteration == 1000: raise Exception("Error in the process B: to many trials")
        print("harmony B..... OK")

        ritmoA = None
        iteration = 0
        isOK = False
        while not isOK:
            ritmoA = rt.getRhythm_from_Trigram(trigram_R, "N1.0", "N1.0", ritmoLenght, False, 0)
            if ritmoA is not None:
                if ritmoA[1][-1]=="N1.0":
                    isOK = True
            iteration +=1
            if iteration == 1000: raise Exception("Error in the process RA: to many trials")
        print("rhythm A..... OK")

        ritmoB = None
        iteration = 0
        isOK = False
        while not isOK:
            ritmoB = rt.getRhythm_from_Trigram(trigram_R, "N1.0", "N1.0", ritmoLenght, False, 0)
            if ritmoB is not None:
                if ritmoB[1][-1]=="N1.0":
                    isOK = True
            iteration +=1
            if iteration == 1000: raise Exception("Error in the process RB: to many trials")
        print("rhythm B..... OK")

        ritmoCompleto = []
        for r in ritmoA[0]:
            ritmoCompleto.append(r)
        for r in ritmoB[0]:
            ritmoCompleto.append(r)

        acordesCompleto = []
        for c in chordsA[0]:
            acordesCompleto.append(c)
        for c in chordsB[0]:
            acordesCompleto.append(c)

        melodyGenerated = ml.rhythm_to_Melody(ritmoCompleto, acordesCompleto)
        print(str(chordsA[1]) + str(chordsB[1]))
        return [acordesCompleto, melodyGenerated]


    def composeABA_jazz(self, tonality, mode):
        composerName= "jazz"
        ml = Melody()

        inicios = [["N1/3", "N1/3"], ["N1.0", "N1/3"], ["N1/3", "N0.5"], ["R1.0", "N1/3"], ["N0.25", "N0.25"], ["R0.5", "N0.5"], ["N0.5", "N0.5"], ["N1.5", "N0.5"], ["N2/3", "N0.5"]]
        inicioA = random.choice(inicios)
        inicioB = random.choice(inicios)

        acordes = [["I7", "v"], ["i", "iii7"], ["v7", "v"], ["v", "ii7"], ["I7", "ii7"], ["i", "v"], ["ii7", "i"], ["v", "v7"] ]
        acordesA = random.choice(acordes)
        acordesB = random.choice(acordes)

        seccionA = self.composePhrase(composerName, tonality, mode, acordesA[0], acordesA[1], inicioA[0], inicioA[1], True)
        seccionB = self.composePhrase(composerName, key.Key('G'), mode, acordesB[0], acordesB[1], inicioB[0], inicioB[1], True)

        acordesCompleto = []
        for c in seccionA[0]:
            acordesCompleto.append(c)
        for c in seccionB[0]:
            acordesCompleto.append(c)
        for c in seccionA[0]:
            acordesCompleto.append(ml.cloneFigure(c))


        notasCompleto = []
        for c in seccionA[1]:
            notasCompleto.append(c)
        for c in seccionB[1]:
            notasCompleto.append(c)
        for c in seccionA[1]:
            notasCompleto.append(ml.cloneFigure(c))

        return [acordesCompleto, notasCompleto]



    def composeABA_bach(self, tonality, mode):
        composerName= "bach"
        ml = Melody()

        inicios = [["N0.5", "N0.5"], ["N1.0", "N1.0"], ["R1.0", "N1.0"], ["N1.0", "N2.0"]]
        inicioA = random.choice(inicios)
        inicioB = random.choice(inicios)

        acordes = [["I", "V"], ["I", "V7"], ["I", "IV"], ["I", "vi"]]
        acordesA = random.choice(acordes)
        acordesB = random.choice(acordes)

        seccionA = self.composePhrase(composerName, tonality, mode, acordesA[0], acordesA[1], inicioA[0], inicioA[1], True)
        seccionB = self.composePhrase(composerName, key.Key('G'), mode, acordesB[0], acordesB[1], inicioB[0], inicioB[1], True)

        acordesCompleto = []
        for c in seccionA[0]:
            acordesCompleto.append(c)
        for c in seccionB[0]:
            acordesCompleto.append(c)
        for c in seccionA[0]:
            acordesCompleto.append(ml.cloneFigure(c))


        notasCompleto = []
        for c in seccionA[1]:
            notasCompleto.append(c)
        for c in seccionB[1]:
            notasCompleto.append(c)
        for c in seccionA[1]:
            notasCompleto.append(ml.cloneFigure(c))

        return [acordesCompleto, notasCompleto]


    def composeABA_essen(self, tonality, mode):
        composerName= "essen"
        ml = Melody()

        inicios = [["N0.5", "N0.5"], ["N0.5", "N0.25"], ["N0.75", "N0.25"], ["N1.0", "N0.5"], ["N1.0", "N1.0"]]
        inicioA = random.choice(inicios)
        inicioB = random.choice(inicios)

        acordes = [["i", "V"], ["i", "ii"], ["i", "IV"]]
        acordesA = random.choice(acordes)
        acordesB = random.choice(acordes)

        seccionA = self.composePhrase(composerName, tonality, mode, acordesA[0], acordesA[1], inicioA[0], inicioA[1], random.choice([True, False]))
        seccionB = self.composePhrase(composerName, key.Key('F'), mode, acordesB[0], acordesB[1], inicioB[0], inicioB[1], random.choice([True, False]))

        acordesCompleto = []
        for c in seccionA[0]:
            acordesCompleto.append(c)
        for c in seccionB[0]:
            acordesCompleto.append(c)
        for c in seccionA[0]:
            acordesCompleto.append(ml.cloneFigure(c))


        notasCompleto = []
        for c in seccionA[1]:
            notasCompleto.append(c)
        for c in seccionB[1]:
            notasCompleto.append(c)
        for c in seccionA[1]:
            notasCompleto.append(ml.cloneFigure(c))

        return [acordesCompleto, notasCompleto]



    def composeABA_palestrina(self, tonality, mode):
        composerName= "palestrina"
        ml = Melody()

        inicios = [["N0.5", "N0.5"], ["N1.0", "N1.0"], ["N2.0", "N2.0"], ["N2.0", "N1.0"]]
        inicioA = random.choice(inicios)
        inicioB = random.choice(inicios)

        acordes = [["I", "V"], ["I", "IV"], ["I", "ii"]]
        acordesA = random.choice(acordes)
        acordesB = random.choice(acordes)

        seccionA = self.composePhrase(composerName, tonality, mode, acordesA[0], acordesA[1], inicioA[0], inicioA[1], True)
        seccionB = self.composePhrase(composerName, key.Key('G'), mode, acordesB[0], acordesB[1], inicioB[0], inicioB[1], True)

        acordesCompleto = []
        for c in seccionA[0]:
            acordesCompleto.append(c)
        for c in seccionB[0]:
            acordesCompleto.append(c)
        for c in seccionA[0]:
            acordesCompleto.append(ml.cloneFigure(c))


        notasCompleto = []
        for c in seccionA[1]:
            notasCompleto.append(c)
        for c in seccionB[1]:
            notasCompleto.append(c)
        for c in seccionA[1]:
            notasCompleto.append(ml.cloneFigure(c))

        return [acordesCompleto, notasCompleto]


    def composeABA_monteverdi(self, tonality, mode):
        composerName= "monteverdi"
        ml = Melody()

        inicios = [["N2.0", "N2.0"], ["N1.0", "N1.0"], ["N3.0", "N1.0"], ["N4.0", "N2.0"], ["N4.0", "N1.0"], ["N4.0", "N4.0"]]
        inicioA = random.choice(inicios)
        inicioB = random.choice(inicios)

        acordes = [["I", "V"], ["I", "IV"], ["I", "ii"]]
        acordesA = random.choice(acordes)
        acordesB = random.choice(acordes)

        seccionA = self.composePhrase(composerName, tonality, mode, acordesA[0], acordesA[1], inicioA[0], inicioA[1], False)
        seccionB = self.composePhrase(composerName, key.Key('G'), mode, acordesB[0], acordesB[1], inicioB[0], inicioB[1], False)

        acordesCompleto = []
        for c in seccionA[0]:
            acordesCompleto.append(c)
        for c in seccionB[0]:
            acordesCompleto.append(c)
        for c in seccionA[0]:
            acordesCompleto.append(ml.cloneFigure(c))


        notasCompleto = []
        for c in seccionA[1]:
            notasCompleto.append(c)
        for c in seccionB[1]:
            notasCompleto.append(c)
        for c in seccionA[1]:
            notasCompleto.append(ml.cloneFigure(c))

        return [acordesCompleto, notasCompleto]






