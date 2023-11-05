# HackEDBetaScanner
QR Scanner for HackED Beta Registration

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

** REPLACE 'Filename' to direct to the path to service_account.json that connects to the spreadsheet

