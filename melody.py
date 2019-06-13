from music21 import *
import nltk
import glob
import random
import pickle
import fileIO
from datetime import datetime
import operator
import ngram


class Melody:

    def rhythm_to_Melody(self, rhythms, chords):
        chordsDuration = []
        buf = 0.0
        previousPitchps = 0
        for c in chords:
            buf = buf + c.quarterLength
            chordsDuration.append(buf)

        buf = 0.0
        for m in rhythms:
            index = 0
            for i in range(len(chordsDuration)):
                if(i==0):
                    if(buf<chordsDuration[i]):
                        index=0
                else:
                    if(buf >= chordsDuration[i-1] and buf<chordsDuration[i]):
                        index = i
            if type(m) is note.Note:
                m.pitch = self.selectClosestNote3(previousPitchps, chords[index])
                previousPitchps = m.pitch.ps
            buf = buf + m.quarterLength
    ##    print(buf)
        return rhythms

    def cloneFigure(self, figure):
        if type(figure) is chord.Chord:
            c = chord.Chord()
            for p in figure.pitches:
                c.add(str(p))
            c.duration.quarterLength = figure.quarterLength
            return c
        elif type(figure) is note.Note:
            n = note.Note(str(figure.pitch), quarterLength = figure.quarterLength)
            return n
        elif type(figure) is note.Rest:
            r = note.Rest(quarterLength = figure.quarterLength)
            return r
        else:
            print("Error clonando objeto desconocido")

    def selectClosestNote(self, previousPitch, chord):
        noteSel = None
        if previousPitch is None:
            return random.choice(chord.pitches)
        else:
            minDist = 9999999999
            buf = 0
            try:
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [4, 5, 6, 7]:
                        n.pitch.octave = o
                        buf = abs(previousPitch.ps - n.pitch.ps)
                        if buf  < minDist:
                            if(previousPitch.ps!= n.pitch.ps):
                                noteSel = note.Note(str(n.pitch))
                                minDist = buf
            except:
                print ("error")
            return noteSel.pitch

    def selectClosestNote2(self, previousPitchps, chord):
        noteSel = None
        if previousPitchps == 0:
            return random.choice(chord.pitches)
        else:
            minDist = 9999999999
            buf = 0
            try:
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [3, 4, 5, 6]:
                        n.pitch.octave = o
                        buf = abs(previousPitchps - n.pitch.ps)
                        if buf < minDist and buf!=0:
                            if (n.pitch.ps>=60 and n.pitch.ps <82):
                                noteSel = note.Note(str(n.pitch))
                                minDist = buf
            except:
                print ("error")
            return noteSel.pitch



    def selectClosestNote3(self, previousPitchps, chord):
        noteSel = None
        noteSel2 = None
        if previousPitchps == 0:
            return random.choice(chord.pitches)
        else:
            minDist = 9999999999
            buf = 0
            try:
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [3, 4, 5, 6]:
                        n.pitch.octave = o
                        buf = abs(previousPitchps - n.pitch.ps)
                        if buf < minDist and buf!=0:
                            if (n.pitch.ps>=60 and n.pitch.ps <82):
                                noteSel = note.Note(str(n.pitch))
                                minDist = buf
                minDist = 9999999999
                buf = 0
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [3, 4, 5, 6]:
                        n.pitch.octave = o
                        buf = abs(previousPitchps - n.pitch.ps)
                        if buf < minDist and buf!=0 and noteSel.pitch.ps!= n.pitch.ps:
                            if (n.pitch.ps>=60 and n.pitch.ps <82):
                                noteSel2 = note.Note(str(n.pitch))
                                minDist = buf
            except:
                print ("error")
            return random.choice([noteSel.pitch, noteSel2.pitch])


    def selectClosestNote4(self, previousPitchps, chord):
        noteSel = None
        noteSel2 = None
        if previousPitchps == 0:
            return random.choice(chord.pitches)
        else:
            minDist = 9999999999
            buf = 0
            try:
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [3, 4, 5, 6]:
                        n.pitch.octave = o
                        buf = abs(previousPitchps - n.pitch.ps)
                        if buf < minDist:
                            if (n.pitch.ps>=60 and n.pitch.ps <82):
                                noteSel = note.Note(str(n.pitch))
                                minDist = buf
                minDist = 9999999999
                buf = 0
                for p in chord.pitches:
                    n = note.Note(str(p))
                    for o in [3, 4, 5, 6]:
                        n.pitch.octave = o
                        buf = abs(previousPitchps - n.pitch.ps)
                        if buf < minDist and noteSel.pitch.ps!= n.pitch.ps:
                            if (n.pitch.ps>=60 and n.pitch.ps <82):
                                noteSel2 = note.Note(str(n.pitch))
                                minDist = buf
            except:
                print ("error")
            return random.choice([noteSel.pitch, noteSel2.pitch])