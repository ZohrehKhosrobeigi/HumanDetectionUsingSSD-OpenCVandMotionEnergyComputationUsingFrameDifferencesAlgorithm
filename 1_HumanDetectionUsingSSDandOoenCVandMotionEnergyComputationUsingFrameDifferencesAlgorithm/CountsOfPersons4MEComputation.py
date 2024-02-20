#THIS CLASS TAKES COORIDNATE BOXES AND POST-PROCESS THEM
#I CAN ADD Non-Maximum Suppression (NMS) TO THIS CLASS
import os
class CountsOfPersons4MEComputation():
    def __init__(self):
        self.frame=0
        self.frame_n=0
        self.point_a_X, self.point_a_Y, self.point_b_X, self.point_b_Y, self.label=0,0,0,0,0


    def countsOfPersons4MEComputation(self,frame,box_details,frame_n,report_folder):  # this method is used to check the counts of objects detected and counts of boxes for each frame. Then compute the motion energy for a person

        c = CountsOfPersons4MEComputation ()#HAVING THE NAME OF CLASS TO USE IT AS A REPORT FILE FOR THIS CLASS
        report_file_name = report_folder + "/" + c.__class__.__name__ + ".txt"

        file_exists = os.path.isfile (report_file_name)# write only one time
        wf_report = open (report_file_name, "a")
        if not(file_exists):
            wf_report.write ("This file shows errors that happen in "+str(c)+ " Class\n")

        wf_report.write("Print frame number: "+str(frame_n)+ " print box info: "+str(box_details.current_frame_detections))

        dict_boxes = box_details.current_frame_detections

        if len ((list (dict_boxes.keys ()))) == 1:

            # here I checked the count of persons detected. if it is only one person and only one box for that person, motion energy of the person is comuted.
            # note if there exist more than one box for a person, Non-Maximum Suppression (NMS) can be used to select only one box.
            person_id1 = list (dict_boxes.keys ())[0]
            self.point_a_X, self.point_a_Y, self.point_b_X, self.point_b_Y, self.label = dict_boxes[person_id1]["Point_a_X"], dict_boxes[person_id1]["Point_a_Y"], \
                                                dict_boxes[person_id1]["Point_b_X"], dict_boxes[person_id1]["Point_b_Y"], \
                                                dict_boxes[person_id1]["Label"]

        else:
            wf_report.write ("More than one person is detected in frame: " + str (frame_n) +", boxes info: "+str(dict_boxes)+ "\n")

        self.frame=frame
        self.frame_n=frame_n

        return self.point_a_X, self.point_a_Y, self.point_b_X, self.point_b_Y, self.label,self.frame,self.frame_n  # Return coordinator of the box.