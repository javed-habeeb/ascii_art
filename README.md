# 🎨 ASCII Art Generator (Python + OpenCV)

A simple command-line tool that converts images into ASCII art using Python and OpenCV. Designed to work smoothly in WSL, Linux, and Windows.

---

## ✨ Features

- Converts `.png` / `.jpg` images to ASCII
- Background pixel removal for clean output
- Smart resizing for terminal fit
- Scrollable output using `less`
- Works inside WSL or any UNIX-style terminal
- Now supports ANSI 256-color grayscale rendering(optional,uses 'less -R')
- width adjustable

--

## 📁 Project Structure

ascii_art/
├── ascii_art_script.py # Main Python script
├── test_images/ # Folder to place input images
├── venv/ # (Optional) virtual environment folder
├── requirements.txt # Dependencies
└── README.md # This file


---

## 🛠️ Setup Instructions (for WSL / Linux / macOS)

### 1️⃣ Create a virtual environment

bash:
python3 -m venv venv
source venv/bin/activate

### 1️⃣Install the required packages
bash:
pip install requirements.txt
(note:only opencv-python is needed)

### 1️⃣Using the script
1. Add your image into the test_images/ folder if you can't specify the path of the image on your system
2. Run the script (python3 ascii_art_script.py)
   you'll be asked to either specify the path to image or (if inside test_images/ folder,its name. for e.g.,cat.png)

NOTE:
	*)the final output is piped into 'less' text viewer
        *)If you see Could not load image, check your path and file extension.
⚙️ Customization Options:

	You can tweak these values directly in the script:

		width: default is 110 (adjust for wider or smaller terminal)
		background_threshold: default is 245 (lower this if white areas aren't removed)
