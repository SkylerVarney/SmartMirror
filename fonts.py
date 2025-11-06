from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QFont, QFontDatabase

class FontListApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.initUI()

    def initUI(self):
        # Create a layout
        layout = QVBoxLayout()

        # Get the list of available font families
        font_families = QFontDatabase().families()

        # Display font examples
        for font_family in font_families:
            label = QLabel()
            font = QFont(font_family, 12)
            label.setFont(font)
            label.setText(f"Font Family: {font_family}")
            layout.addWidget(label)

        # Create a scroll area and set its content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)

        # Set the layout for the main widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # Set the window properties
        self.setWindowTitle('Available Fonts')
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication([])
    font_list_app = FontListApp()
    font_list_app.show()
    app.exec()
