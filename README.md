# Hand Gesture-Based Virtual Keyboard

![Patent Filed](https://img.shields.io/badge/Patent-Filed-blue)
![Status](https://img.shields.io/badge/status-prototype-green)
![Built With](https://img.shields.io/badge/Tech-OpenCV%20%7C%20cvzone%20%7C%20PyAutoGUI-blue)

A webcam-based **virtual keyboard** that allows users to type by hovering their fingers over on-screen keys. This project uses **real-time hand tracking** to enable contactless typing — ideal for public, medical, or assistive technology applications.

---

## 🧠 Patent Information

**📌 Patent Title:** *"A Hand Gesture-Based Virtual Keyboard"*  
**📅 Filed:** June 2025  
**🏢 Filed By:** Sharda University  
**📜 Under:** The Patents Act, 1970 (India)

> This invention enables touchless typing using webcam-based hand gesture recognition mapped to a dynamic virtual keyboard interface.

---

## ✨ Features

- 🔠 Real-time typing via hand hover on virtual keys
- 👆 Finger detection for key selection
- ⌨️ Complete keyboard layout (A-Z, numbers, space, delete, symbols)
- 🧠 PyAutoGUI integration for simulated typing on system
- 🕐 Countdown + typing delay to reduce accidental keypresses
- 📸 Live webcam feed overlaid with button grid

---

## 🛠️ Technologies Used

| Component       | Library           |
|-----------------|-------------------|
| Hand Detection  | cvzone, MediaPipe |
| Image Capture   | OpenCV            |
| Keystroke Emulation | PyAutoGUI    |
| GUI Drawing     | OpenCV            |
| Language        | Python 3.8+       |

---

## 📁 Project Structure

```
hand-gesture-virtual-keyboard/
├── virtual_keyboard.py       # Main logic with detection, drawing, typing
├── requirements.txt          # All dependencies
├── .gitignore                # Ignore cache/venv
├── LICENSE                   # MIT + patent mention
└── README.md                 # Project documentation
```

---

## 🚀 How to Run

1. Clone this repository
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Launch the keyboard app:

```bash
python virtual_keyboard.py
```

> Press `Q` to exit the application at any time.

---

## 🧪 How It Works

- Webcam captures hand using OpenCV
- cvzone’s HandTrackingModule detects finger positions
- Finger hover over key regions triggers a "press"
- PyAutoGUI simulates real system typing
- Delay ensures accidental presses are minimized

---

## 📌 Notes

- Designed for one hand interaction
- Works best in good lighting
- Ideal for no-touch environments

---

## 👤 Author

**Hridey Dalal**  
📧 [hrideydalal1@gmail.com](mailto:hrideydalal1@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/hridey-/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
Includes patent protection under The Patents Act, 1970 (India).
