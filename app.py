from flask import Flask, request, render_template 
import csv
import cv2
import os

  

app = Flask(__name__)   
  
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        ID = request.form.get("fname")
        name = request.form.get("lname") 
        #return "Your name is "+first_name + last_name
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("C:\\Users\\Manish\\Desktop\\New folder (2)\\TrainingImage" + os.sep + name.replace(" ","") + "."+ID+ '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                #display the frame
                cv2.imshow('frame', img)
                #wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 100
                elif sampleNum > 100:
                    break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for email : " + ID + " Name : " + name
        row = [ID, name]
        with open("C:\\Users\\Manish\\Desktop\\New folder (2)\\employeesdetail"+os.sep+"employeesDetails.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()
    
    return render_template("form.html")
  
if __name__=='__main__':
   app.run()
