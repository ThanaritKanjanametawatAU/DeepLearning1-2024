from keras.models import load_model
from tkinter import *
import tkinter as tk
from keras.layers import BatchNormalization
import win32gui
from PIL import ImageGrab, Image, ImageOps, ImageDraw
import numpy as np
import matplotlib.pyplot as plt




# Load the model only once during the initialization
model = load_model('model/mnist.keras')

def predict_digit(img):
    # Convert the image to grayscale
    img = img.convert('L')
    # Resize the image to 28x28 pixels
    img = img.resize((28, 28), Image.LANCZOS)
    # Invert the image if necessary
    img = ImageOps.invert(img)

    # plt.imshow(img, cmap='gray')
    # plt.show()


    # Normalize and prepare the image for prediction
    img_array = np.array(img).reshape(1, 28, 28, 1) / 255.0
    result = model.predict([img_array])[0]
    return np.argmax(result), max(result)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.x = self.y = 0
        self.canvasLength = 280

        # Set Window Title
        self.title("MNIST Digit Recognizer")

        # Set Window Size
        self.geometry("960x360")

        self.canvas = tk.Canvas(self, width=self.canvasLength, height=self.canvasLength, bg="white", cursor="cross")
        self.canvas_small = tk.Canvas(self, width=28, height=28, bg="white", cursor="cross")
        self.label = tk.Label(self, text="     Draw a digit!!!", font=("Helvetica", 48))
        # Make the button wider
        self.classify_btn = tk.Button(self, text="Analyze", command=self.classify_handwriting, width=15, height=3)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all, width=15, height=3)

        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.canvas_small.grid(row=0, column=1, pady=2, padx=2)
        self.label.grid(row=0, column=2, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=2, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        self.canvas.bind("<Button-1>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

        self.small_image = Image.new('L', (28, 28), 255)
        self.draw_small = ImageDraw.Draw(self.small_image)

    def clear_all(self):
        self.canvas.delete("all")
        self.canvas_small.delete("all")
        self.small_image = Image.new('L', (28, 28), 255)
        self.draw_small = ImageDraw.Draw(self.small_image)
        self.label.configure(text="     Draw a digit!!!")

    def classify_handwriting(self):
        print("Classifying the digit...")
        img = self.small_image
        digit, acc = predict_digit(img)
        print(f"Predicted Digit: {digit}, Confidence: {acc * 100:.2f}%")
        self.label.configure(text=f"Predicted: {digit}\nConfidence: {acc * 100:.2f}%")

    def start_pos(self, event):
        self.x, self.y = event.x, event.y

    def draw_lines(self, event):
        if self.x and self.y:
            self.canvas.create_line(self.x, self.y, event.x, event.y, fill='black', width=12)
            self.draw_on_small_canvas(self.x, self.y, event.x, event.y)
        self.x, self.y = event.x, event.y

    def draw_on_small_canvas(self, x1, y1, x2, y2):
        scale = 28 / self.canvasLength
        self.canvas_small.create_line(x1 * scale, y1 * scale, x2 * scale, y2 * scale, fill='black', width=2)
        self.draw_small.line([x1 * scale, y1 * scale, x2 * scale, y2 * scale], fill='black', width=2)

app = App()
app.mainloop()
