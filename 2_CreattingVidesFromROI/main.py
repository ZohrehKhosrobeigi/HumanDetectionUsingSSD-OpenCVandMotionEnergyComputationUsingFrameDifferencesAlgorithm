# Cropping a video using ROI coordinate extracted by "1_HumanDetectionAndMotionEnergyComputation" and frames.
# New VIDEOS ARE SAVED.
import json
from datetime import datetime

import Importing_all_files_in_list_1
import GetName
import Check_existed_folder_to_create_2
import CreateVideo
import CSV_DF_reader

# Reading files from folder
input_video_file = "iVideo"

input_csv_roi = "iOutput_Files"
outputfolder="Output_Video_ROI"

finaloutputfoler = Check_existed_folder_to_create_2.createfolder ()
finaloutputfoler.createfolder (outputfolder)

files = Importing_all_files_in_list_1.importingfiles ()
files.get_candidates (input_csv_roi)
print ("*" * 100)
print (files.filelist)
lst_roi_files=files.filelist


files = Importing_all_files_in_list_1.importingfiles ()
files.get_candidates (input_video_file)
print ("*" * 100)
print (files.filelist)
lst_video_files=files.filelist

for video_file in lst_video_files:

    c = datetime.now ()
    # Displays Time
    current_time = c.strftime ('%H:%M:%S')
    print ('Current Time is:', current_time)


    getname = GetName.GetName ()
    ply1, session = getname.getName (video_file)
    new_video_ROI_file = outputfolder + "/" + ply1 + "_" + session + "_ROI_HumanDetected_OpenCV_SSD.mp4"

    scv_ROI_file = input_csv_roi + "/" + ply1 + "_" + session + "_ROI_HumanDetected_OpenCV_SSD.csv"
    print(video_file)
    csvdfreader = CSV_DF_reader.CSVDFReader ()
    csvdfreader.csvdfReader (scv_ROI_file)


    # Deserialize the JSON , since I read it as dataframe, to have list of coordinates as numbers and list, I should Deserialize it eventhough it is considered as a string
    # columns_to_serialize
    csvdfreader.df_file["ROI"] = csvdfreader.df_file["ROI"].apply (json.loads)

    creating_video=CreateVideo.SaveVideo()
    creating_video.saveVideo(csvdfreader.df_file,video_file ,new_video_ROI_file)


