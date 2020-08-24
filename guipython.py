from PIL import Image, ImageTk
from pymongo import MongoClient
import cv2
import tkinter as tk
from tkinter import Button,filedialog
import os
import glob
main = tk.Tk()
main.title("Face_Detection & Recognition")
main.iconbitmap("images/face.ico")
main.geometry("350x300")
face_cascade = cv2.CascadeClassifier(
        r'C:\Users\Admin\Python_Project\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\Admin\Python_Project\Lib\site-packages\cv2\data\haarcascade_eye.xml')


dir = {
    "id": "101",
    "dir": r"C:\Users\Admin\PycharmProjects\Python_Project\dataset"
}



def select_file():
    image1 = ImageTk.PhotoImage(Image.open("images/image.png"))
    button = Button(top_frame, text="Select Image", foreground="white", background="gray",width=20,font=('helvetica',20), command=face_detect).pack(pady=20)


def get_name(faces):
    client = MongoClient("localhost", 27017)
    print(client)
    db = client.image
    collection = db.img_dir
    record = {}
    collection.update({"dir": dir['dir']},{"$setOnInsert":dir}, upsert=True)
    record = collection.find({"dir": dir["dir"]})
    img_dir = ''
    for rec in record:
        img_dir = rec['dir']
    sub_dir = [f.name for f in os.scandir(img_dir) if f.is_dir()]
    name = []
    i = 0
    for (x, y, w, h) in faces:
        for dir_name in sub_dir:
            file = glob.glob(img_dir +'\\' +dir_name+'\\*')
            for file_name in file:
                img = cv2.imread(file_name)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face1 = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (a, b, c, d) in face1:
                    if x == a and y == b and w == c and h == d:
                        name.append(dir_name)
                        break
        if len(name) == len(faces):
            pass
        else:
            name.append('Unknown')

        i = i + 1

    return name


def get_faces(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_name = get_name(faces)
    i = 0
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        cv2.rectangle(img, (x, y - 35), (x + w, y),(255, 0, 0), cv2.FILLED)
        cv2.putText(img, face_name[i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), lineType=cv2.LINE_AA)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        i = i + 1
    return img


def face_detect():
    global folder_path
    filename = filedialog.askopenfilename(initialdir=r'C:\Users\Admin\PycharmProjects\Python_Project\input')
    folder_path.set(filename)
    print(filename)
    img = get_faces(filename)
    cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE)
    img = cv2.resize(img,(700, 600))
    cv2.imshow('output', img)
    cv2.waitKey(-10)
    cv2.destroyAllWindows()

folder_path = tk.StringVar()
global top_frame
top_frame = tk.Frame(main, bg="white")
top_frame.grid()
global right_frame
right_frame =tk.Frame(main)
right_frame.grid()
photo = ImageTk.PhotoImage(Image.open("images/logo.png"))
label = Button(top_frame, image=photo, text="hiii", bg="gray", command=select_file)
label.pack()

main.mainloop()


