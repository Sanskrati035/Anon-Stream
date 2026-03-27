# Anon-Stream: Real-time AI Privacy Engine 🚀

**Anon-Stream** is a privacy-focused streaming tool that dynamically identifies and **pixelates background intruders** in real-time. It ensures user privacy during video calls by keeping the primary user clear while instantly obscuring unauthorized persons in the frame.

## ✨ Key Features
* **Intruder Detection:** Uses spatial heuristics to detect faces outside the user's center-radius.
* **Dynamic Pixelation:** Real-time localized pixelation of background intruders using MediaPipe and OpenCV.
* **Virtual Camera Sink:** Broadcasts AI-processed frames to platforms like **Google Meet, Zoom, and MS Teams**.
* **Stream Persistence:** Includes "Last Frame Memory" to prevent signal loss (Green Screen) upon termination.
* **Minimalist UI:** A clean "Stealth Mode" experience with no distracting overlays.

## 🛠️ Tech Stack
* **Language:** Python
* **AI/ML:** MediaPipe (Selfie Segmenter & Face Detector), TFLite
* **Libraries:** OpenCV, NumPy, pyvirtualcam
* **Methodology:** Developed using **Scrum/Agile** principles.

## 🚀 Installation & Setup

1. **Clone the repository:**
   bash
   git clone [https://github.com/YOUR_USERNAME/anon-stream.git](https://github.com/YOUR_USERNAME/anon-stream.git)
   cd anon-stream
2.  **Install Dependencies:**
Bash
pip install -r requirements.txt
3. **Install Virtual Camera Driver:**
Download and extract the Unity Capture driver.
Go to the Install folder, right-click Install.bat, and Run as Administrator.
4.  **Run the Engine:**
Bash
python main.py

**How to Use:**

Run the main.py script.
Open Google Meet or Zoom.
In Video Settings, select "Unity Video Capture" as your camera.
To stop, press 'q' in the terminal.