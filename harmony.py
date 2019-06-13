from music21 import *
import nltk
import glob
import random
import pickle
import fileIO
from datetime import datetime
import operator
import ngram


class Harmony:

    def getChord(self, symbol, tonality):
        chord = roman.RomanNumeral(symbol, tonality)
        return chord.pitches

    def getHarmony_from_Bigram(self, bigram, tonality, firstSymbol, numberChords, duration):
        chordList = []
        symbolList = []
        ng = ngram.Ngram()
        c = chord.Chord(self.getChord(firstSymbol, tonality))
        c.duration.type = duration
        chordList.append(c)
        symbolList.append(firstSymbol)
        symbol = firstSymbol
        for i in range(numberChords - 1):
            symbol = ng.getRandomTuple(subBiGram(bigram, symbol))
            c = chord.Chord(self.getChord(symbol, tonality))
            c.duration.type = duration
            chordList.append(c)
            symbolList.append(symbol)
        return [chordList, symbolList]

    def getHarmony_from_Trigram(self, trigram, bigram, tonality, firstSymbol, numberChords, duration):
        chordList = []
        symbolList = []
        ng = ngram.Ngram()

        c = chord.Chord(self.getChord(firstSymbol, tonality))
        c.duration.type = duration
        chordList.append(c)
        symbolList.append(firstSymbol)
        symbol1 = firstSymbol

        symbol2 = ng.getRandomTuple(ng.subBiGram(bigram, firstSymbol))
        c = chord.Chord(self.getChord(symbol2, tonality))
        c.duration.type = duration
        chordList.append(c)

        for i in range(numberChords - 2):
            symbol3 = ng.getRandomTuple(ng.subTriGram(trigram, symbol1, symbol2))
            c = chord.Chord(self.getChord(symbol3, tonality))
            c.duration.type = duration
            chordList.append(c)
            symbolList.append(symbol3)
            symbol1 = symbol2
            symbol2 = symbol3
        return [chordList, symbolList]

    def voiceLeading(self, chords):
        ## Restringimos todos los acordes a cuatro notas
        for c in chords:
            if len(c.pitches)==2:
                n1 = note.Note()
                n1.pitch = c.pitches[1]
                n2 = note.Note()
                n2.pitch = c.root()
                c.add(n1)
                c.add(n2)
            elif len(c.pitches)==3:
                n = note.Note(str(c.root()))
                n.octave -= 1
                c.add(n)
            elif len(c.pitches) == 5:
                c.remove(str(c.fifth))
                print("Se ha suprimido la quinta en el siguiente acorde: " + str(c))
            elif len(c.pitches) > 5:
                print("Acorde con mas de cinco notas: " + str(c))

        #Buscamos la distribucion de las voces que minimiza la distancia
        #respetando el bajo
        for i in range(1, len(chords)):
            encuentra = False
            minDist = 9999999999
            dist = 0.0
            octaves = [chords[i].pitches[0].octave, chords[i].pitches[1].octave, chords[i].pitches[2].octave, chords[i].pitches[3].octave]
            for o0 in range(1,9):
                chords[i].pitches[0].octave = o0
                for o1 in range(1,9):
                    chords[i].pitches[1].octave = o1
                    for o2 in range(1,9):
                        chords[i].pitches[2].octave = o2
                        for o3 in range(1,9):
                            chords[i].pitches[3].octave = o3
                            dist = distanceChord2(chords[i], chords[i-1])
                            if (dist < minDist):
                                if checkVoiceTesitures(chords[i]) and checkVoiceDisposition(chords[i]) and checkParallelMovement(chords[i-1], chords[i]) :
                                    minDist = dist
                                    octaves = [chords[i].pitches[0].octave, o1, o2, o3]
                                    encuentra = True
            if not encuentra:
                print("No se encuentra disposicion para el acorde Nº" + str(i) + " " + str(chords[i]))
            chords[i].pitches[0].octave = octaves[0]
            chords[i].pitches[1].octave = octaves[1]
            chords[i].pitches[2].octave = octaves[2]
            chords[i].pitches[3].octave = octaves[3]

    def distanceChord(self, chord1, chord2):
        buf = 0
        for i in range (1, 4):
                buf = buf + abs(chord1.pitches[i].ps - chord2.pitches[i].ps)
        return buf

    def distanceChord2(self, chord1, chord2):
        buf = 0
        for i in range (0, 4):
            for j in range (0, 4):
                buf = buf + abs(chord1.pitches[i].ps - chord2.pitches[j].ps)
        return buf

    def checkVoiceTesitures(self, chord):
        if(chord.pitches[0].ps>40) and (chord.pitches[0].ps<=60):
            if (chord.pitches[1].ps>48) and (chord.pitches[1].ps<=69):
                if (chord.pitches[2].ps>52) and (chord.pitches[2].ps<=76):
                    if (chord.pitches[3].ps>64) and (chord.pitches[3].ps<=81):
                        return True
        return False

    def checkVoiceCrossings(self, chord):
        if(chord.pitches[0].ps < chord.pitches[1].ps):
            if (chord.pitches[1].ps < chord.pitches[2].ps):
                if (chord.pitches[2].ps < chord.pitches[3].ps):
                    return True
        return False

    def checkVoiceDisposition(self, chord):
        if abs(chord.pitches[1].ps - chord.pitches[2].ps) <= 12:
            if abs(chord.pitches[2].ps - chord.pitches[3].ps) <= 12:
                return True
        return False

    def checkParallelMovement(self, chord1, chord2):
        v0 = chord2.pitches[0].ps - chord1.pitches[0].ps
        v1 = chord2.pitches[1].ps - chord1.pitches[1].ps
        v2 = chord2.pitches[2].ps - chord1.pitches[2].ps
        v3 = chord2.pitches[3].ps - chord1.pitches[3].ps

        #Prohibidos los movimientos paralelos
        if (v0>0 and v1>0 and v2>0 and v3>0) or (v0<0 and v1<0 and v2<0 and v3<0):
            return False
        return True
