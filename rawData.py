from music21 import *

class RawDataExtractor:
    def getRawDataH(self, obras):
        majorMode = ""
        minorMode = ""
        lydianMode = ""
        dorianMode = ""

    ##    acordes = {}
    ##    acordesFull = {}
        buf = ""
        for obra in obras:
            if "190.7" not in obra and "171.6" not in obra and "161.6" not in obra and "149.7" not in obra and "136.6" not in obra and "130.6" not in obra and "120a" not in obra and "1.6":

                print(str(obra))
                subObras = []
                ##Detectar si es una unica obra (score) o una coleccion de obras (opus)
                buf = converter.parse(obra)
                if (type(buf) is stream.Opus):
                    for b in buf.scores:
                        subObras.append(b)
                else:
                    subObras.append(buf)

                for b in subObras:

                    try:
                        #extraccion de los acordes
                        bChords = b.chordify()
        ##                b.show()
                        chords = bChords.recurse().getElementsByClass('Chord')

                        #Deteccion de la tonalidad
                        ks=b.flat.getElementsByClass(key.KeySignature)[0]
        ##                print(str(obra) + " " + str(ks))

                        #para el caso de monteverdi, cogemos la tonalidad por el ultimo acorde ya que music21 falla *******
        ##                print(chords[-1].root())
                        if(str(ks) =="<music21.key.KeySignature of no sharps or flats>"):
                            if("C" in str(chords[-1].root())):
                                ks=key.Key("C")
                            elif("G" in str(chords[-1].root())):
                                ks=key.Key("G")
                            elif("A" in  str(chords[-1].root())):
                                ks=key.Key("a")
                            elif("D" in  str(chords[-1].root())):
                                ks=key.Key("d")
                            elif("E" in  str(chords[-1].root())):
                                ks=key.Key("e")
                            elif("F" in  str(chords[-1].root())):
                                ks=key.Key("F")
                        elif(str(ks) == "<music21.key.KeySignature of 1 flat>"):
                            if("F" in str(chords[-1].root())):
                                ks=key.Key("F")
                            elif("C" in str(chords[-1].root())):
                                ks=key.Key("C")
                            elif("D" in  str(chords[-1].root())):
                                ks=key.Key("d")
                            elif("A" in  str(chords[-1].root())):
                                ks=key.Key("a")
                            elif("G" in str(chords[-1].root())):
                                ks=key.Key("g")
                        elif(str(ks) == "<music21.key.KeySignature of 1 sharp>"):
                            b.show()
                            if("G" in str(chords[-1].root())):
                                ks=key.Key("G")
                            elif("D" in str(chords[-1].root())):
                                ks=key.Key("D")
                            elif("E" in  str(chords[-1].root())):
                                ks=key.Key("e")
                            elif("A" in  str(chords[-1].root())):
                                ks=key.Key("a")
                            elif("C" in  str(chords[-1].root())):
                                ks=key.Key("C")
                        #**********************************************************************************

                        for c in chords:
                            try:
                                rn = roman.romanNumeralFromChord(c, ks)
                            except:
                                rn = None
                                print ("Error en acorde " + str(c))
                            if (rn is not None):
                                if(ks.mode=="major"):
                                    majorMode = majorMode + " " + str(rn.figure)
                                elif(ks.mode=="minor"):
                                    minorMode = minorMode + " " + str(rn.figure)
                                elif(ks.mode=="lydian"):
                                    lydianMode = lydianMode + " " + str(rn.figure)
                                elif(ks.mode=="dorian"):
                                    dorianMode = dorianMode + " " + str(rn.figure)
                                else:
                                    print(str(ks.mode))

                                #Lista de acordes para hacer las stopwords -----------------------------
            ##                    if rn.figure not in acordes:
            ##                        acordes[rn.figure] = 1
            ##                    else:
            ##                        acordes[rn.figure] += 1
            ##                    buf = str(rn.figure) + " " + str(rn.commonName) + " " +  str(ks) + " " + str(rn.pitches)
            ##
            ##                    if buf not in acordesFull:
            ##                        acordesFull[buf] = 1
            ##                    else:
            ##                        acordesFull[buf] += 1
                                #-----------------------------------------------------------------------
                    except:
                        print("Error al procesar la obra: " + str(b))
        ##    writeDict(acordes, "acordes.txt")
        ##    writeDict(acordesFull, "acordesFull.txt")
            else:
                print("excluyendo")
        return [majorMode, minorMode, lydianMode, dorianMode]

    def getRawDataR(self, obras):
        dataRaw = ""

        buf = ""
        for obra in obras:
            print(str(obra))
            if "190.7" not in str(obra) and "171.6" not in str(obra) and "161.6" not in str(obra) and "149.7" not in str(obra) and "136.6" not in str(obra) and "130.6" not in str(obra) and "120a" not in str(obra) and "1.6":
                subObras = []
                ##Detectar si es una unica obra (score) o una coleccion de obras (opus)
                buf = converter.parse(obra)

                if (type(buf) is stream.Opus):
                    for b in buf.scores:
                        subObras.append(b)
                else:
                    subObras.append(buf)

                for b in subObras:

                    try:
    ##                    for parte in b.parts[0]:
                        for compas in b.parts[0].getElementsByClass(classFilterList=[stream.Measure]):
                            #Para cada compas obtenemos todos los elementos de tipo Nota o Silencio, de forma ordenada
                            for elemento in compas.elements:
                                try:
                                    if(elemento.duration.type!='zero'):
                                        if(elemento.isRest):
                                            dataRaw = dataRaw + " " + "R" + str(elemento.quarterLength)
                                        else:
                                            dataRaw = dataRaw + " " + "N" + str(elemento.quarterLength)

                                except Exception as err:
                                    print(str(err))
                                    continue
                    except:
                        print("Error al procesar la obra: " + str(b))
            else:
                print("Excluyendo")
        return [dataRaw]