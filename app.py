from email import message
from flask import Flask, jsonify , render_template , Response
from AttendanceProject import camera_output
import csv

app=Flask(__name__)


@app.route("/")
def home():
 return render_template("home.html")

@app.route('/video_feed')
def video_feed():
    return Response(camera_output(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/attendance")
def attendance():
       data=[]
       with open("Attendance.csv") as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row)
            
                return render_template('attendance.html', data=data)    

@app.route("/clear")
def clear():
    with open("Attendance.csv","w+") as file:
        file.close()
        #return render_template("clearstatus.html",message="cleared")
        msg={"message":"cleared"}
        return jsonify(msg)

if __name__ == "__main__":
    app.run(debug=True)