import pickle

class FileIO:

    def save_obj(self, obj, name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def writeText(self, text, filename):
        with open(filename, "wt") as f:
            f.write(text)

    def readText(self, filename):
        with open(filename, "r") as f:
            content = f.read()
            return(content)

    def writeList(self, list, filename):
        with open(filename, "wt") as f:
            for i in list:
                f.write(str(i) + "\n")

    def readList(self, filename):
        with open(filename, "r") as f:
            list = []
            for line in f:
                value = line.replace("\n", "")
                list.append(value)
            return(list)

    def writeDict(self, dict, filename):
        with open(filename, "wt") as f:
            for i in dict.keys():
                f.write(str(i) + " " + str(dict[i]) + "\n")

    def readDict(self, filename):
        with open(filename, "r") as f:
            dict = {}
            for line in f:
                values = line.replace("\n", "").split(" ")
                dict[values[0]] = float(values[1])
            return(dict)

    def getFileNames(self, composerName, mode):

        if(mode=="M"):
            mode = "major"
        elif (mode=="m"):
            mode = "minor"
        elif(mode.lower()=="r" or mode.lower()=="rhythm" or mode.lower()=="ritmo"):
            mode = "rhythm"

        dataRawFile = "dataRaw" + composerName.capitalize() + mode.capitalize()+ ".txt"
        dataBigramFile = composerName.lower() + "_" +  mode.lower() + "_2gram"
        dataTrigramFile = composerName.lower() + "_" +  mode.lower() + "_3gram"
        dataUnigramFileZero = composerName.lower() + "_" +  mode.lower() + "_1gramZero"
        dataBigramFileZero = composerName.lower() + "_" +  mode.lower() + "_2gramZero"
        dataUnigramFile = composerName.lower() + "_" +  mode.lower() + "_1gram"

        return [dataRawFile, dataBigramFile, dataTrigramFile, dataUnigramFileZero, dataBigramFileZero, dataUnigramFile]

