# Face Recognition-Based File Access System

This Python-based security system uses **face recognition** as a password to access locked files. If a file is locked, it can only be accessed by a previously saved face. It also allows you to register new faces and lock/unlock files.

---

## 📸 Features

- 🔒 Lock files behind facial recognition
- 👤 Add new faces (passwords) via webcam
- 📁 Add more files to be protected
- 🧠 Face matching using `face_recognition` and `OpenCV`
- 🪞 Real-time face detection with live camera feed
- ❌ Deny access to unauthorized users
- ✅ Display file contents on successful face recognition

---

## 🛠️ Requirements

- Python 3.7+
- OpenCV
- face_recognition
- dlib
- numpy

### 📦 Install Dependencies

```bash
pip install opencv-python face_recognition numpy
