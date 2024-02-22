#THIS CLASS TAKES COORDINATE BOXES AND CROP ROI AND THEN COMPUTE MOTION ENERGY.
#MIN FOR POINT A AND MAX FOR POINT B IS DEFINED TO HAVE LARGERST BOX. THEN, I USE THE SAME COORDINATES FOR PREVIOUS AND
#CURRENT FRAM TO CROP ROI AND THEN COMPUTING MOTION ENERGY
import os
import cv2
import numpy as np
import csv
import CSVWriter

class MotionEnergyComputation():
    def __init__(self):
        self.roi_max_current=0
        self.frame_n=0

    def motionEnergyComputation(self,current_frame_coordinat,prev_frame_coordinat,csv_file,report_folder,output_ROI_csv):
        c = MotionEnergyComputation ()#HAVING THE NAME OF CLASS TO USE IT AS A REPORT FILE FOR THIS CLASS
        report_file_name = report_folder + "/" + c.__class__.__name__ + ".txt"
        file_exists = os.path.isfile (report_file_name)  # write only one time
        wf_report = open (report_file_name, "a")
        if not (file_exists):
            wf_report.write ("This file shows errors that happen in"+ str(c)+" Class\n")
        wf_report.write ("Frame number is: "+str(current_frame_coordinat.frame_n)+" ,")


        # define the max between xs.Then, I will have largest coordinates
        #a should be smaller and b should be bigger to have the larger box
        point_a_X_max=min(current_frame_coordinat.point_a_X,prev_frame_coordinat.point_a_X)
        point_a_Y_max=min(current_frame_coordinat.point_a_Y,prev_frame_coordinat.point_a_Y)
        point_b_X_max=max(current_frame_coordinat.point_b_X,prev_frame_coordinat.point_b_X)
        point_b_Y_max=max(current_frame_coordinat.point_b_Y,prev_frame_coordinat.point_b_Y)

        point_a_X_max = max (point_a_X_max, 0)# When one of the coordinates are zero or negative, put that one to having undefined coordiante
        point_a_Y_max = max (point_a_Y_max, 0)
        point_b_X_max = max (point_b_X_max, 0)
        point_b_Y_max = max (point_b_Y_max, 0)

        """image[y1:y2, x1:x2], (x1, y1) and (x2, y2) are the coordinates of the top-left and bottom-right corners of the rectangle, respectively. point a(x1,y1), point b(x2,y2)
        
        Note that the image[y1:y2, x1:x2] syntax is used to crop the image in the y direction first, and then in the x direction.
        This is because images are represented as 2D arrays in OpenCV, with the first dimension corresponding to the y axis (row) and the second dimension corresponding to the x axis (column).
        
        In typical image processing operations with NumPy and OpenCV, an image (or frame) can be sliced using the syntax image[y1:y2, x1:x2] to extract a region defined by the top-left corner (x1, y1) and the bottom-right corner (x2, y2). Here:
        
        y1:y2 specifies the row indices (vertical slice) of the region.
        x1:x2 specifies the column indices (horizontal slice) of the region.
        Given the variables in your code (point_a_X_max, point_a_Y_max, point_b_X_max, point_b_Y_max), it appears they are meant to represent the maximum extents of a bounding box in the previous frame, where:
        
        point_a_X_max and point_a_Y_max are the coordinates for the top-left corner of the bounding box.
        point_b_X_max and point_b_Y_max are the coordinates for the bottom-right corner of the bounding box."""

        roi_max_prev = prev_frame_coordinat.frame[point_a_Y_max:point_b_Y_max,point_a_X_max:point_b_X_max]  # use the same coordinates
        roi_max_prev = cv2.cvtColor (roi_max_prev, cv2.COLOR_BGR2GRAY)

        self.roi_max_current = current_frame_coordinat.frame[point_a_Y_max:point_b_Y_max,point_a_X_max:point_b_X_max]
        self.roi_max_current = cv2.cvtColor (self.roi_max_current, cv2.COLOR_BGR2GRAY)


        lst_diff = cv2.absdiff (roi_max_prev, self.roi_max_current)
        # Count pixels with significant change
        count_pixels_changed_greater20 = np.sum (lst_diff >20)#it counts how many values in lst_diff are greater than 20. The expression lst_diff > 20 creates a boolean array where each element is True if the corresponding element in lst_diff is greater than 20, and False otherwise. The np.sum() function then counts how many True values are in this boolean array, effectively giving you the count of values in lst_diff that are greater than 20.
        # Sum of differences
        sum_of_diff = np.sum (lst_diff[lst_diff > 20])
        wf_report.write("This is the division: "+str(count_pixels_changed_greater20)+"\n")
        if count_pixels_changed_greater20:
            mean_dif=sum_of_diff/count_pixels_changed_greater20 # I compute mean as normalization

        else:
            mean_dif = sum_of_diff / 1

######################## Writing section
        #wrting ME
        buffer = []
        # Accumulate data in the buffer
        buffer.append ([current_frame_coordinat.frame_n, mean_dif])
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            # Write CSV headers
            writer.writerows (buffer)


        csv_writer = CSVWriter.CSVWriter ()  # writing the ROI
        csv_writer.cSVWrtier ([current_frame_coordinat.frame_n,[point_a_X_max,point_a_Y_max,point_b_X_max,point_b_Y_max]], output_ROI_csv, header=["FrameNumber", "ROI"])

        #######################################

        self.frame_n=current_frame_coordinat.frame_n# I want to use it te have a dict of roi per each frame, then I can creat a new video.
        return self.roi_max_current,self.frame_n








