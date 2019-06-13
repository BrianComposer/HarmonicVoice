from music21 import *
import nltk
import glob
import random
import pickle
import fileIO
from datetime import datetime
import operator
import ngram

class Rhythm:
    def getRhythm_from_Bigram(self, bigram, startSymbol, totalDuration):
        noteList = []
        duration = 0
        ng = ngram.Ngram()
        buf = createNote_or_Rest(startSymbol)
        for item in buf:
            noteList.append(item)
            duration = duration + item.quarterLength
        symbol = startSymbol
        while (duration< totalDuration):
            symbol = ng.getRandomTuple(ng.subBiGram(bigram, symbol))
            buf = createNote_or_Rest(symbol)
            for item in buf:
                noteList.append(item)
                duration = duration + item.quarterLength
        return noteList

    def getRhythm_from_Trigram(self, trigram, firstSymbol, secondSymbol, totalDuration, anacrusa, quarterLengthNotaFinal):
        noteList = []
        symbolList = []
        ng = ngram.Ngram()
        duration = 0
        silenceDuration = 0
        iteration = 0

        duracionMaxima = totalDuration - quarterLengthNotaFinal

        #append the quarter silence
        if(anacrusa == True):
            buf = self.createNote_or_Rest("R1.0")
            for item in buf:
                noteList.append(item)
                duration = duration + item.quarterLength
            symbolList.append("R1.0")

        buf = self.createNote_or_Rest(firstSymbol)
        for item in buf:
            noteList.append(item)
            duration = duration + item.quarterLength
        symbolList.append(firstSymbol)

        buf = self.createNote_or_Rest(secondSymbol)
        for item in buf:
            noteList.append(item)
            duration = duration + item.quarterLength
        symbolList.append(secondSymbol)

        symbol1 = firstSymbol
        symbol2 = secondSymbol
        while (duration < duracionMaxima):
            symbol3 = ng.getRandomTuple(ng.subTriGram(trigram, symbol1, symbol2))
            #Comprobamos que los tresillos solo aparezcan en los tiempos fuertes de los compases
            if(self.checkTuplet_to_Beat(duration, symbol3)):
                #Comprobamos que no se exceda un maximo numero de tiempos en silencio
                if (self.checkSilence(silenceDuration, symbol3)):
                    buf = self.createNote_or_Rest(symbol3)
                    #Comprobamos que no se exceda la duracion maxima del ritmo
                    durBuf = duration
                    for item in buf:
                        durBuf = durBuf + item.quarterLength
                    if durBuf<= duracionMaxima:
                        for item in buf:
                            noteList.append(item)
                            duration = duration + item.quarterLength
                            #Acumulamos la duracion de los silencios para controlar el numero maximo
                            if("R" in symbol3):
                                silenceDuration = silenceDuration + item.quarterLength
                            else:
                                silenceDuration = 0
                        symbol1 = symbol2
                        symbol2 = symbol3
                        symbolList.append(symbol3)
            iteration +=1
            if iteration == 50: return None
    ##    print("Ritmo calculado con duracion:" + str(duration))


        #append the last note
        if(quarterLengthNotaFinal > 0):
            sbuf = ""
            if (quarterLengthNotaFinal==1.0):
                sbuf = "N1.0"
            elif (quarterLengthNotaFinal==2.0):
                sbuf = "N2.0"
            elif (quarterLengthNotaFinal==3.0):
                sbuf = "N3.0"
            elif (quarterLengthNotaFinal==4.0):
                sbuf = "N4.0"
            buf = self.createNote_or_Rest(sbuf)
            for item in buf:
                noteList.append(item)
                duration = duration + item.quarterLength
            symbolList.append(sbuf)

        return [noteList, symbolList]

    def createNote_or_Rest(self, symbol):
        buf = None
        duration = 0.0
        buf = ""
        notes = []
        numerador = 0
        denominador = 0
        if(symbol[0] =="N"):
            buf = symbol.replace("N","")
            if ("/" in buf):
                numerador = float(buf.split("/")[0])
                denominador = float(buf.split("/")[1])
                duration = float(numerador/ denominador)
                for i in range(int(denominador)):
                    notes.append(note.Note("C", quarterLength = duration))
            else:
                duration = float(buf)
                notes.append(note.Note("C", quarterLength = duration))
        elif (symbol[0] =="R"):
            buf =symbol.replace("R","")
            if ("/" in buf):
                numerador = float(buf.split("/")[0])
                denominador = float(buf.split("/")[1])
                duration = float(numerador/ denominador)
                for i in range(int(denominador)):
                    notes.append(note.Rest(quarterLength = duration))
            else:
                duration = float(buf)
                notes.append(note.Rest(quarterLength = duration))
        return notes

    def checkTuplet_to_Beat(self, acumulatedDuration, symbol):
        if("/" in symbol):
            numerador = float(symbol.replace("N","").replace("R","").split("/")[0])
            denominador = float(symbol.replace("N","").replace("R","").split("/")[1])
            if(numerador==1):
                #Tresillo de corchea
                if acumulatedDuration % 1 == 0:
                    return True
            elif(numerador==2):
                #Tresillo de negra
                if acumulatedDuration % 2 ==0:
                    return True
            elif(numerador==4):
                #Tresillo de blanca
                if acumulatedDuration % 4 == 0:
                    return True
            return False
        else:
            return True

    def checkSilence(self, acumulatedDurationOfSilences, symbol):
        if("R" in symbol):
            if(acumulatedDurationOfSilences >= 1.5):
                return False
            else:
                return True
        else:
            return True
