import cv2  # OpenCV for camera and image processing
from cvzone.HandTrackingModule import HandDetector  # Hand detection from cvzone
import pyautogui  # To simulate real keyboard presses
import time  # For handling delays and timing

# Initialize camera
cap = cv2.VideoCapture(0)  # Start webcam (camera index 0)
cap.set(3, 1280)  # Set video frame width
cap.set(4, 720)   # Set video frame height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)  # Create detector with 95% confidence

# Define keyboard layout as rows of keys
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"]
]

# Button class to define key behavior
class Button:
    def _init_(self, pos, text, width=60, height=60):
        self.pos = pos  # Top-left corner of button
        self.width = width  # Button width
        self.height = height  # Button height
        self.text = text  # Text on the button
        self.last_press_time = time.time()  # Last time the button was pressed
        self.is_clicked = False  # If the button is currently clicked

    def draw(self, img):
        # Draw button on the image
        x, y = self.pos
        color = (0, 255, 0) if self.is_clicked else (200, 200, 150)
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), color, cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + self.width, y + self.height), (255, 0, 0), 3)

        # Draw the text centered on the button
        font_scale = 1.5
        thickness = 2
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, thickness)[0]
        text_x = x + (self.width - text_size[0]) // 2
        text_y = y + (self.height + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 0, 0), thickness)

    def check_click(self, lmList):
        # Check if index finger is over the button
        if lmList:
            x, y = self.pos
            fx, fy = lmList[8][0], lmList[8][1]  # Index finger tip coordinates
            return x < fx < x + self.width and y < fy < y + self.height
        return False

# Create list of button objects
buttonList = []
button_size = 75
spacing_x, spacing_y = 15, 15
start_x, start_y = 100, 180

# Generate buttons based on the key layout
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        x = start_x + (button_size + spacing_x) * j
        y = start_y + (button_size + spacing_y) * i
        buttonList.append(Button((x, y), key, button_size, button_size))

# Create special buttons (space, delete, @, .)
special_y = start_y + (button_size + spacing_y) * len(keys)
space_button = Button((start_x, special_y), "SPACE", 300, button_size)
delete_button = Button((start_x + 320, special_y), "DELETE", 130, button_size)
at_button = Button((start_x + 470, special_y), "@", button_size, button_size)
dot_button = Button((start_x + 550 + 20, special_y), ".", button_size, button_size)  # 20px gap added

# Add special buttons to the list
buttonList.extend([space_button, delete_button, at_button, dot_button])

# Initialize variables for typed text and timing
text_output = ""
first_key_pressed = False
first_key_start_time = None
key_delay_time = 3  # Seconds between key presses
initial_wait_time = 5  # Delay before keyboard starts
first_key_delay_time = 5  # Delay before first key press is allowed
last_pressed_time = None
start_time = time.time()

# Main loop
while True:
    success, img = cap.read()  # Capture frame from webcam
    img = cv2.flip(img, 1)  # Flip image for mirror view

    elapsed_time = time.time() - start_time

    # Show countdown before keyboard becomes active
    if elapsed_time < initial_wait_time:
        remaining_time = int(initial_wait_time - elapsed_time)
        cv2.putText(img, f"Starting in {remaining_time}s...", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        cv2.imshow("Virtual Keyboard", img)
        cv2.waitKey(1)
        continue

    # Detect hands
    hands, img = detector.findHands(img, flipType=False)

    # Draw all buttons and reset click state
    for button in buttonList:
        button.draw(img)
        button.is_clicked = False

    # Delay before allowing the first key press
    if not first_key_pressed:
        if first_key_start_time is None:
            first_key_start_time = time.time()
        first_key_elapsed = time.time() - first_key_start_time
        if first_key_elapsed < first_key_delay_time:
            remaining_time = int(first_key_delay_time - first_key_elapsed)
            cv2.putText(img, f"First key in {remaining_time}s...", (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            cv2.imshow("Virtual Keyboard", img)
            cv2.waitKey(1)
            continue

    # Check if any hand is detected
    if hands:
        lmList = hands[0]['lmList']  # Get landmarks for first hand
        for button in buttonList:
            if button.check_click(lmList):  # If finger is over button
                current_time = time.time()

                if not first_key_pressed:
                    first_key_pressed = True
                    last_pressed_time = current_time

                # Add delay between repeated key presses
                if last_pressed_time is None or current_time - last_pressed_time >= key_delay_time:
                    last_pressed_time = current_time
                    button.is_clicked = True

                    # Handle special keys
                    if button.text == "DELETE":
                        if len(text_output) > 0:
                            text_output = text_output[:-1]  # Remove last character
                            pyautogui.press('backspace')  # Simulate backspace key
                    elif button.text == "SPACE":
                        text_output += " "  # Add space to text
                        pyautogui.press('space')  # Simulate space key
                    else:
                        text_output += button.text  # Add character to output
                        pyautogui.press(button.text.lower())  # Simulate the key press

                    print(f"Button {button.text} clicked")  # Log the pressed key

    # Display the typed text on screen
    cv2.rectangle(img, (40, 40), (1150, 120), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, text_output, (60, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Show the final image
    cv2.imshow("Virtual Keyboard", img)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
