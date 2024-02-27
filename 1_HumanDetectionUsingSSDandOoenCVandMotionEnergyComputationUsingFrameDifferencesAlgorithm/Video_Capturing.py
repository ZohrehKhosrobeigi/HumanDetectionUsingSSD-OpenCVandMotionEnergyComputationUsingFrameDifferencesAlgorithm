#THIS CLASS READ VIDEO AND PASS IT TO HUMANDETECTION CLASS TO DETECT PERSONS IN THE VIDEO.
# THEN USING EXTRACTED BOXES, MOTION ENERGY OF THE PERSON IS COMPUTED.
#The CROPPED VIDEO IS SHOWN FINALLY

import cv2
import HumanDetectionSSD
import CountsOfPersons4MEComputation
import MotionEnergyComputation
import CSVWriter

class VideoCapturing():


    def __init__(self):

        self.dict_ROI={}

    def videoCapturing(self, video_name, output_ROI_csv,output_ME_csv,report_folder):

        csv_writer = CSVWriter.CSVWriter () #writing the motion enrgy of first frame as 0
        csv_writer.cSVWrtier ([1,0], output_ME_csv, header=["Frame", "ME"])


        frame_n = 1# here is the first frame of video that I consider it as previouse frame. SO, I can subtract next frame by the previouse frame.
        cap = cv2.VideoCapture (video_name)# reading first frame
        if not cap.isOpened ():
            print ("Failed to open video")
            exit ()

        #   Process the first frame
        #   Previous frame

        ret, prev_frame = cap.read ()  # reading frame first time to have a frame as previous frame
        get_box_human = HumanDetectionSSD.HumanDetection ()#Human detection to detect persons and have box coordinates
        get_box_human.humanDetection_Box (prev_frame, frame_n,report_folder)

        #   Calling this class to check the counts of persons detected and counts of boxes for each player. It is a kind of preprocessing
        prev_frame_counts_persons_ME_comput=CountsOfPersons4MEComputation.CountsOfPersons4MEComputation()
        prev_frame_counts_persons_ME_comput.countsOfPersons4MEComputation(prev_frame, get_box_human, frame_n,report_folder)  #I do not show the first frame in the video but use it as previouse frame to substract this from the current one
        #### Proccesing rest of the frames, frames id >1
        while True:
            frame_n += 1

            ret, current_frame = cap.read ()
            if not ret:
                break
            #   Human Detection
            get_box_human = HumanDetectionSSD.HumanDetection ()#Human detection to detect persons and have box coordinates
            get_box_human.humanDetection_Box (current_frame,frame_n,report_folder )

            #   Calling this class to check the counts of persons detected and counts of boxes for each player.
            current_frame_counts_persons_ME_comput = CountsOfPersons4MEComputation.CountsOfPersons4MEComputation ()
            current_frame_counts_persons_ME_comput.countsOfPersons4MEComputation (current_frame, get_box_human, frame_n,report_folder)


            #   Motion Energy Computation

            motion_computation = MotionEnergyComputation.MotionEnergyComputation ()  # calling ME computation class
            motion_computation.motionEnergyComputation (prev_frame_counts_persons_ME_comput, current_frame_counts_persons_ME_comput, output_ME_csv, report_folder,output_ROI_csv)
            prev_frame_counts_persons_ME_comput=current_frame_counts_persons_ME_comput#keeping current roi_frame as prevouse one to subtract from next frame


            # if current_frame_counts_persons_ME_comput.label==0:# WHEN THERE IS NO DETECTION, AVOID HAVEING ERROR TO SHOW THE VIDEO
            #     print(current_frame_counts_persons_ME_comput.label)
            #     current_frame_counts_persons_ME_comput.label="000"
            # cv2.imshow (current_frame_counts_persons_ME_comput.label, motion_computation.roi_max_current)
            # cv2.waitKey (1000)
            # cv2.destroyAllWindows ()
            # if cv2.waitKey (1) & 0xFF == ord ('q'):
            #     break



        cap.release ()
        cv2.destroyAllWindows ()


        return self.dict_ROI





