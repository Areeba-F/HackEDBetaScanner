import gspread
from pyzbar.pyzbar import decode
import cv2
import time
from datetime import datetime

'''
Qr Scanner

When run, will open a cv2 video capture. 
Hold QR code infront of camera, and wait for information pop-up

Press any key to close pop up, and continue to scan more QR codes
Press 'q' to quit program (might have to press multiple times)

Imports:
gspread          5.11.2             -pip install gspread
pyzbar           0.1.9              -pip install pyzbar
opencv-python    4.8.0.76           -pip install opencv-python
numpy            1.26.0 (needed for opencv download)


    * Press ANY KEY to close text pop-up and continue scanning
    * Press q to quit the program

** REPLACE 'Filename' to direct to the path to service_account.json

'''

# REPLACE WITH PATH TO JSON
Filename = "hackedbeta_service_account.json"

# Load google sheets
sa = gspread.service_account(filename=Filename)
sh = sa.open("HackED Beta 2023 Registration (Responses)")
wks = sh.worksheet('Form Responses 1')
allValues = wks.get_all_values()
# blank white image for pop-up
template = cv2.imread(r"Template.png")
camera = True

id = 0

# create video camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 150)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# Continue until 'q' pressed
while camera == True:

    id = 0

    success, frame = cam.read()

    # get qr code if in frame
    for i in decode(frame):

        print("QR code:",i.data.decode('utf-8'))
        id = i.data.decode('utf-8')
        time.sleep(3)

        # reload data from google sheet
        allValues = wks.get_all_values()

    cv2.imshow("QRscanner", frame)
    cv2.waitKey(1)


    # Iterate over each row in the spreadsheet 
    for i in range(len(allValues)):
        row = allValues[i]
        
        # check qr code against all id's
        if str(id) == (str(row[11])):
            colour = (0,0,0)
            print()
            print("Name:",row[2],row[3])

            # Waiver

            # if waiver is signed
            if row[13] == "TRUE":
                print("Waiver submitted!")
                waiver_answer = "Waiver submitted!"
                waiver_colour = (0, 150, 0)

            # if waiver NOT signed
            else:
                print("Waiver NOT submitted")  
                waiver_answer = "Waiver NOT submitted"
                waiver_colour = (0, 0, 150)

            # Payment

            # if paid
            if row[16] == "TRUE":
                print("Paid!")
                paid_answer = "Paid!"
                paid_colour = (0, 150, 0)

            # if NOT paid
            else:
                print("NOT Paid")  
                paid_answer = "NOT paid"
                paid_colour = (0, 0, 150)


            # Check in/check out

            now = datetime.now()

            current_time = now.strftime("%H:%M on %D")
            print("Current Time =", current_time)
            
            # if already checked OUT, check them in and show "checked in"
            if row[14] == "FALSE":
                check_answer = "in"
                check_colour = (0, 150, 0)

                value = 'O'+ str(i+1)
                print("Now Checked IN")
                wks.update_acell(value, 'TRUE')

                update_check = 'R'+ str(i+1)
                wks.update_acell(update_check, current_time)

            # if already checked IN, check them out and show "checked out"
            else:
                check_answer = "out"
                check_colour = (0, 0, 150)

                value = 'O'+ str(i+1)
                print("Now Checked OUT")
                wks.update_acell(value, 'FALSE')

                update_check = 'R'+ str(i+1)
                wks.update_acell(update_check, current_time)

            # create information pop-up
            cam.release()      
            string = row[2] + " " +row[3]
            template = cv2.imread(r"Template.png")

            image = cv2.putText(template, string, (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
            image = cv2.putText(template, paid_answer, (70, 480), cv2.FONT_HERSHEY_DUPLEX, 3, paid_colour, 2, cv2.LINE_AA)
            image = cv2.putText(template, waiver_answer, (70, 630), cv2.FONT_HERSHEY_DUPLEX, 3, waiver_colour, 2, cv2.LINE_AA)

            image = cv2.putText(template, "Now Checked", (70, 800), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 2, cv2.LINE_AA)
            image = cv2.putText(template, check_answer, (950, 800), cv2.FONT_HERSHEY_SIMPLEX, 5, check_colour, 4, cv2.LINE_AA)

            cv2.imshow("text",image)
            cv2.waitKey(0)
            cv2.destroyWindow("text")

            # restart camera
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FPS, 30)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 150)
            cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    # press 'q' to quit program
    # (might have to press a few times cause timing is a bitch)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyWindow("QRscanner")
        camera = False

# end
cam.release()
cv2.destroyAllWindows()