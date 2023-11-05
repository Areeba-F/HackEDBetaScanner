import cv2
template = cv2.imread(r"Template.png")

check_answer = "in"
check = "Now Checked"
waiver_answer = "Waiver NOT submitted"
colour = (0, 0, 150)
string = "Areeba Fazal"
waiver_colour = (0, 0, 150)
check_colour = (0, 150, 0)

paid_answer = "Paid!"
paid_colour = (0, 150, 0)

image = cv2.putText(template, string, (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
image = cv2.putText(template, paid_answer, (70, 480), cv2.FONT_HERSHEY_DUPLEX, 3, paid_colour, 2, cv2.LINE_AA)
image = cv2.putText(template, waiver_answer, (70, 630), cv2.FONT_HERSHEY_DUPLEX, 3, waiver_colour, 2, cv2.LINE_AA)

image = cv2.putText(template, "Now Checked", (70, 800), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 2, cv2.LINE_AA)
image = cv2.putText(template, check_answer, (950, 800), cv2.FONT_HERSHEY_SIMPLEX, 5, check_colour, 4, cv2.LINE_AA)
cv2.imshow("text",image)
cv2.waitKey(0)