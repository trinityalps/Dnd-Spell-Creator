from ImageCreator import create_image
from PyQt5.QtWidgets import QApplication, QPushButton

app = QApplication([])
button = QPushButton('Run')
def on_button_clicked():
    create_image()


button.clicked.connect(on_button_clicked)
button.show()
app.exec_()
