import cv2


class SaveVideo():
    def saveVideo(self,df_roi,video,output_video_path):
# the order of coordinate saved are: point_a_X_max,point_a_Y_max,point_b_X_max,point_b_Y_max

        # Accessing all the first items in the 'ROI' column
        point_a_X_max = min(df_roi['ROI'].apply(lambda x: x[0]))
        point_a_Y_max = min(df_roi['ROI'].apply (lambda x: x[1]))
        point_b_X_max = max(df_roi['ROI'].apply(lambda x: x[2]))
        point_b_Y_max = min(df_roi['ROI'].apply (lambda x: x[3]))

#Capturing video
        cap = cv2.VideoCapture (video)  # reading first frame only to know the width and height of the frame
        if not cap.isOpened ():
                print ("Failed to open video")
                exit ()


        ret, frame = cap.read ()
        if not ret:
            print ("Failed to read the video")
            cap.release ()
            return

        # Set the size for the output video

        # Determine the size of the ROI
        roi_width = point_b_X_max - point_a_X_max
        roi_height = point_b_Y_max - point_a_Y_max
        frame_rate =cap.get(cv2.CAP_PROP_FPS)
  # Adjust frame rate as needed


        # # Initialize VideoWriter with MP4 codec
        fourcc = cv2.VideoWriter_fourcc (*'mp4v')  # Codec for MP4 format
        #
        out = cv2.VideoWriter (output_video_path, fourcc, frame_rate, (roi_width, roi_height))


        while True:
            ret, frame = cap.read ()
            if not ret:
                break

            # Cropping and converting the frame to grayscale

            roi_max_current = frame[point_a_Y_max:point_b_Y_max,point_a_X_max:point_b_X_max]
            roi_max_current = cv2.cvtColor (roi_max_current, cv2.COLOR_BGR2GRAY)
            # Since the VideoWriter expects a color image, convert the grayscale image back to BGR
            roi_max_current_bgr = cv2.cvtColor (roi_max_current, cv2.COLOR_GRAY2BGR)
            # Write the processed frame to the output video
            out.write(roi_max_current_bgr)

            cv2.imshow ("hi", roi_max_current)#DISABLE IT FOR A FASTER RUN
            if cv2.waitKey (1) & 0xFF == ord ('q'):
                break

        cap.release ()
        cv2.destroyAllWindows ()

