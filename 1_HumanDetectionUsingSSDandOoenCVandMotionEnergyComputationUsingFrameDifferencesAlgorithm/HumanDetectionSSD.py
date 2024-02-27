#THIS CLASS DETECT PERSONS IN THE VIDEO AND EXTRACT COORDINATES OF A BOX AROUND THE PERSON.
# SOMETIMES, SSD DETECTS SEVERAL BOXES FOR A PERSON PER FRAME. I JUST KEEP ONE WITH GREATER COFIDENCE VALUE
#I use the threshold of 65% since in our dataset, some frames have been masked.
import os
import cv2
import numpy as np
class HumanDetection():
    def __init__(self):
        self.current_frame_detections={}

    def humanDetection_Box(self, frame,frame_n,report_folder):

        c=HumanDetection()#HAVING THE NAME OF CLASS TO USE IT AS A REPORT FILE FOR THIS CLASS
        report_file_name= report_folder + "/" + c.__class__.__name__ + ".txt"
        if frame_n==3 :
            print()
        file_exists = os.path.isfile (report_file_name)# write only one time
        wf_report = open (report_file_name, "a")

        if not (file_exists):
            wf_report.write("This file shows errors that happen in  "+str(c)+ " Class\n")

        #CONFIG THE MODEL
        prototyp = "SSD_models/MobileNetSSD_deploy.prototxt"
        weigths = "SSD_models/MobileNetSSD_deploy.caffemodel"
        model = cv2.dnn.readNetFromCaffe (prototyp, weigths)
        person_class_ID = 15  # Class ID for 'person' is 15
        detections_dict = {}
        blob = cv2.dnn.blobFromImage (frame, scalefactor=0.007843, size=(300, 300), mean=127.5)
        model.setInput (blob)
        detections = model.forward ()

#ssd detects 100 objects, but here i just need a person. So, to be faster, I change it to 1 and I loop over only a person
        for i in range (1):# loop, iterates over the detected objects in a frame processed by the SSD (Single Shot MultiBox Detector) model. gives the number of detections made by the SSD model in the current frame. The loop iterates over each detection to process them individually.
            class_id = int (detections[0, 0, i, 1])
            confidence = detections[0, 0, i, 2]
            wf_report.write("*********** i is: "+str(i)+"\n")
            h, w = frame.shape[:2]#having the size of the image or frame
            box = detections[0, 0, i, 3:7] * np.array ([w, h, w, h])#This part scales the normalized coordinates (which are relative to the size of the image and range between 0 and 1) to the actual pixel coordinates in the frame. w and h are the width and height of the frame, respectively. Multiplying the normalized coordinates by the actual size of the image converts them into pixel values.
            (point_a_X, point_a_Y, point_b_X, point_b_Y) = box.astype ('int')#start and end of point a, and start and end of point b

            #The size of the bounding box is determined by the difference between (endX, endY) and (xX, startY):
            # Assign an ID to the detection
            detection_id = len (detections_dict) + 1
            # Store the bounding box coordinates with the detection ID. SDD may detect several box for an object in a frame. I keep all of that

            label = f"Person: {detection_id} Confidence: {confidence * 100:.2f}% frame: {frame_n}"
            temp_dic = {"ObjId": i, " ClassId": class_id, "Point_a_X": point_a_X,
                        "Point_a_Y": point_a_Y, "Point_b_X": point_b_X, "Point_b_Y": point_b_Y,
                        "Confidence": confidence, "Label": label}

            if confidence > 0.65 and class_id == person_class_ID:

                if detection_id==1:# have only one person with id one. so when in the video there are two persons, it only keep info for id 1.

                    if detection_id in list (self.current_frame_detections.keys ()):# here i create a dictionary of persons detected and boxes for each person
                        z=self.current_frame_detections[detection_id]
                        if z["Confidence"]<confidence:
                            self.current_frame_detections[detection_id] = temp_dic
                            wf_report.write ("Greater confidence, dictionary is: " + str (temp_dic) + " ,")
                    else:
                        self.current_frame_detections[detection_id] = temp_dic
                        wf_report.write ("dictionary is: " + str (temp_dic) + " ,")

            else:#  if confident is less than 0.9 report or class id is not 15.


                """
                
                in a moment the guy goes down, and SSD detects it with an id 9. I do not know what this id is
                 but it is not for person. I consider those frames with coordinate of 0.
                So, I uncomment here only for video P029 
                temp_dic = {"ObjId": i, " ClassId": class_id, "Point_a_X": 0,
                            "Point_a_Y": 0, "Point_b_X": 1, "Point_b_Y": 1,
                            "Confidence": confidence, "Label": label}
                self.current_frame_detections[detection_id] = temp_dic

                """

                wf_report.write("Error: class_id is not for human: "+str (class_id)+" i is: "+str (i)+" Confident is: "+str (confidence)+"\n")

        wf_report.write ("Final dictionary is: " + str (self.current_frame_detections) + " ,")
        return self.current_frame_detections
