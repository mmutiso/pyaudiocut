import sys
import os
from pydub import AudioSegment as AS

class CutAudio:
    '''
    This class provides all implementations related to extracting a part of an audio
    '''
    __supportedextensions = ['.mp3']
    __workingdirectory = ""
    __outputdirectory = ""

    def __init__(self, workingdir):
        self.__workingdirectory = workingdir
        self.__outputdirectory  = self.__workingdirectory + "\\" + "ProcessedAudios"
        self.__createDirectory(self.__outputdirectory)

    def __createDirectory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def cutaudiobynseconds(self, audiofilename, defaultduration=5):
        '''
        This method will remove from an audio file the first n seconds and return the trailing part.
        The default n is 5 seconds.

        The file name includes the extension

        This method is thread safe too. 
        '''
        audioinstance = AS.from_mp3(self.__workingdirectory + "\\" + audiofilename)
        
        audiolength = len(audioinstance) / 1000

        #The audio instance is an immutable object. We could store this in a different variable but since we arent reusing this one, lets overwrite
        # the same location in memory
        audioinstance = audioinstance[-(audiolength - defaultduration)*1000:]
        
        audioinstance.export(os.path.join(self.__outputdirectory, audiofilename))


    def readdirectorymp3contents(self):
        '''
        This methods reads the contents of a directory and only gets the names of 
        mp3 type files. It returns the names as a python list.
        '''
        mp3files = []
        os.chdir(self.__workingdirectory)
        
        for root, dir, files in os.walk("."):
            for filename in files:
                thename, ext = os.path.splitext(filename)
                if ext in self.__supportedextensions:
                    mp3files.append(filename)

        return mp3files
    
def extractdirpathfromcommandlinearguments():
    '''
    We expect only one argument; the directory with the music to convert.
    This function will validate if that argument is provided and return it if it is. 
    '''
    if len(sys.argv) < 2: # argument at index 0 is the script name, we expect 1 to be the dir and we dont have a problem is more arguments are passed
        raise Exception("Atleast one argument must be provided")

    dirpath = sys.argv[1]
    return dirpath

def main():
    '''
    The main method
    '''
    workingdir = extractdirpathfromcommandlinearguments()
    ca  = CutAudio(workingdir)
    audiomusicfiles = ca.readdirectorymp3contents()
    
    counter = 1;
    processingerrors = []
    for audiofile in audiomusicfiles:
        try:
            print("Processing [{}] - {} of {}".format(audiofile, counter, len(audiomusicfiles)))
            ca.cutaudiobynseconds(audiofile)            
        except Exception as ex:
            print("There is an error with this file, see exception message at the end")
            processingerrors.append((audiofile, str(ex)))   
        finally:
            counter += 1
    

    if len(processingerrors) > 0:
        print("Could not convert the following files")
        for err in processingerrors:
            print("[{}] with error: {}".format(err[0], err[1]))

    print("Execution complete")

if __name__ == '__main__':
    main()

