import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

class GenerateImageThread(QThread):
    image_generated = pyqtSignal(QImage)

    def __init__(self, api_key, prompt):
        super().__init__()
        self.api_key = api_key
        self.prompt = prompt

    def run(self):
        # Make a request to the OpenAI Image Generation API
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            },
            json={
                'model': 'image-alpha-001',
                'prompt': self.prompt,
                'num_images': 1
            }
        )

        # Get the URL of the generated image from the response
        url = response.json()['data'][0]['url']

        # Load the image from the URL using QImage and QPixmap
        image = QImage()
        image.loadFromData(requests.get(url).content)

        # Emit a signal with the generated image
        self.image_generated.emit(image)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the button and label
        self.button = QPushButton('Generate Image', self)
        self.button.clicked.connect(self.generate_image)
        self.label = QLabel(self)

        # Set the window properties
        self.setWindowTitle('OpenAI Image Generator')
        self.setGeometry(100, 100, 800, 600)

        # Add the button and label to the window
        self.button.setGeometry(50, 50, 200, 50)
        self.label.setGeometry(300, 50, 400, 500)

    def generate_image(self):
        # Create a thread to generate the image
        self.thread = GenerateImageThread(api_key='YOUR_API_KEY', prompt='a cat sitting on a bed')
        self.thread.image_generated.connect(self.display_image)
        self.thread.start()

    def display_image(self, image):
        # Set the image in the label
        pixmap = QPixmap(image)
        self.label.setPixmap(pixmap)

if __name__ == '__main__':
    # Create the application and window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Run the application
    sys.exit(app.exec_())
