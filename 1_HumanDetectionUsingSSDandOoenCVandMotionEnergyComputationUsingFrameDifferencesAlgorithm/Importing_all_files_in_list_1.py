# This class creates a list of all files in the mentioned path
import os
class importingfiles():

  def get_candidates(self, root):
    '''
    Gathers all the files in the folder and its subfolders
    @args:
      {str} root: the root folder path
    @returns:
      {list} a list containing all the individual files paths
    '''
    self.filelist = []

    for root, dirs, files in os.walk(root):
      for file in files:
        #Since we have two other types that are not dataset
        if file!="Readme.rtf" and file!=".DS_Store":
          #print("Name of the file_Grid is:  "+file_Grid)
          self.filelist.append(os.path.join(root, file))

    print ("The number of all files are :"+ str(len (self.filelist)))
    return (self.filelist.sort())