import os
import shutil

class createfolder():
    def createfolder(self,foldername):
        #foldername="finaloutput"
        if os.path.exists(foldername):
            try:
               # shutil.rmtree (foldername)
                os.rmdir (foldername)

                #print ("% s removed successfully" % foldername)
                os.makedirs (foldername)
                print ("folder is created successfully " + str (foldername))
            except OSError as error:
                print (error)
                print ("File path can not be removed")

        elif not os.path.exists(foldername):
            os.makedirs(foldername)
            print("folder is created successfully "+str(foldername))
        else:
            try:
                shutil.rmtree (foldername)
            except OSError as e:
                print ("Error during creating folder: %s - %s." % (e.filename, e.strerror))
