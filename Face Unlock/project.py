import face_recognition
import cv2 as cv
import numpy as np
import os

# Function to add new faces into 'Valid faces' directory to work as Passwords
def add_face():
    print("Add new Face")
    temp,frame=cam.read()

    rgb_frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB) # Convert BGR frame to RGB
    face=face_recognition.face_locations(rgb_frame)
    face_encoding=face_recognition.face_encodings(rgb_frame,face)

    encode=face_encoding[0]
    name=input("Enter name for this face: ")
    faces.append(encode)
    names.append(name)

    path=os.path.join("Valid faces",f"{name}.jpg")
    cv.imwrite(path,frame)

# Function to display file content when correct face is recognized
def access_file(file_name):
    with open(file_name,"r") as f:
        if not f:
            print("Error opening file")
        else:
            print("File content:-\n")
            print(f.read())

#__main__
cam=cv.VideoCapture(0)

# List to hold encoding and names of faces
faces=[]
names=[]

# Extract all names and encoding from 'Valid faces' if present
for f in os.listdir("ValidFaces"):
    img_path=os.path.join("Valid faces",f)  
    img=face_recognition.load_image_file(img_path)
    encoded_img=face_recognition.face_encodings(img)
    if encoded_img:
        faces.append(encoded_img[0])
        names.append(f.split('.')[0])
    else:
        print("Error encoding a face! Skipping...")
        continue

# If no face is present in directory, ask user to add new face (password)
if not faces:
    print("No valid faces found!")
    while True:
        temp,frame=cam.read()
        cv.imshow("No valid faces! Press 'y' to add a face as password or 'n' to exit",frame)
        choice1=cv.waitKey(20)
        if choice1==ord('y'):
            add_face()
            break
        elif choice1==ord('n'):
            print("No valid faces. Ending the program.")
            exit()

locked_files=["locked.txt"] # List to keep track of locked files

# If user want to add new faces or locked files
choice2='f'
while choice2=='f' or choice2=='v':
    choice2=input("Enter 'f' if you wish to add locked files or 'v' valid faces: ").lower()
    if choice2=='f':
        new_file=input("Enter name of the File: ")
        locked_files.append(new_file)
    elif choice2=='v':
        add_face()

file_name=input("Enter file name to access: ")

# If the file is locked (present in locked_files list)
if file_name in locked_files:
    print("File is locked. Face recognition required")
    flag=False
    while True:
        # Start analyzing faces from webcam
        temp,frame=cam.read()
        rgb_frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        face=face_recognition.face_locations(rgb_frame)
        face_encoding=face_recognition.face_encodings(rgb_frame,face)
        # Compare Encoding of detected face with the saved face's encoding
        for(top,right,bottom,left),face_encoding in zip(face,face_encoding):
            check=face_recognition.compare_faces(faces,face_encoding) # Returns True if matching face if found (value less than thershold)
            name="Unknown"
            # Calculate the most matching face among all and retrive it's name
            face_distance=face_recognition.face_distance(faces,face_encoding)
            match=np.argmin(face_distance)

            if check[match]:
                name=names[match]
            # Print messages accordingly 
            if name=="Unknown":
                color=(0,0,255)
                message="Access Denied"
            else:
                color=(0,255,0)
                message="Access Granted"
                if flag is False:
                    access_file(file_name)
                    flag=True
            # Display rectangle around face along with confimation text for better understanding
            cv.rectangle(frame,(left,top),(right,bottom),color,2)
            cv.putText(frame,f"{name}-{message}",(left,top),cv.FONT_HERSHEY_SIMPLEX,1,color,2)
        # Press 'x' to stop webcam from reading
        cv.imshow("Recognising face, Press 'x' to exit",frame)
        if cv.waitKey(20)==ord('x'):
            break
    cam.release()
    cv.destroyAllWindows()
# If file is not locked, simply grant access
else:
    print("File is not locked. Access granted")
    access_file(file_name)

