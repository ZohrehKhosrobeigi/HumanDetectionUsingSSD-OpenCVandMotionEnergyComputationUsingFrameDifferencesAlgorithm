#This code detect persons in the video, crops the person.
# Then motion energy of the video is computed.
# Also, ROI coordinates are saved in a csv file
import Video_Capturing
import Importing_all_files_in_list_1
import GetName
import Check_existed_folder_to_create_2
from datetime import datetime


input_file = "input_videos"
outputfolder="Output_Files"
reports_folder="Output_Report"

#   Creating folders
finaloutputfoler = Check_existed_folder_to_create_2.createfolder ()
finaloutputfoler.createfolder (outputfolder)
finaloutputfoler.createfolder (reports_folder)

files = Importing_all_files_in_list_1.importingfiles ()#    Creating a list of files
files.get_candidates (input_file)
print ("*" * 100)
print (files.filelist)
lst_files=files.filelist

for video_file in lst_files:

    c = datetime.now ()
    # Displays Time, I use it to see how long each file takes
    current_time = c.strftime ('%H:%M:%S')
    print ('Current Time is:', current_time)


    print(video_file)
    getname = GetName.GetName ()
    ply1, session = getname.getName (video_file)
    csv_ROI_file= outputfolder + "/" + ply1 + "_" + session + "_ROI_HumanDetected_OpenCV_SSD.csv"
    csv_me_file= outputfolder + "/" + ply1 + "_" + session + "_ME_HumanDetected_OpenCV_SSD.csv"
    name4reports=reports_folder+"/"+ply1+"_"+session+"_Report_"
    finaloutputfoler.createfolder (name4reports)


    video_capturing = Video_Capturing.VideoCapturing ()
    video_capturing.videoCapturing (video_file, csv_ROI_file, csv_me_file, name4reports)


