import csv
import os
class CSVWriter():
    def cSVWrtier(self,roi,filename,header):
        file_exists = os.path.isfile (filename)

        with open (filename, 'a', newline='') as file:  # Write first frame as Zero
            writer = csv.writer (file)

            if file_exists:
                writer.writerow (roi)
                    #   Write CSV headers
            else:
                writer.writerow (header)#if file is not exist and it is the first time to creat it add header as well
                writer.writerow (roi)
