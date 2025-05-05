import sys
import time
import threading
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QComboBox, 
                           QSpinBox, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import pyautogui
import keyboard
import os

class PrecisionClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrecisionClicker Lite v1.0")
        self.setFixedSize(400, 500)  # Sabit boyut
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QComboBox {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox:hover {
                border: 1px solid #666666;
            }
            QSpinBox {
                background-color: #3b3b3b;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QSpinBox:hover {
                border: 1px solid #666666;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QFrame {
                background-color: #3b3b3b;
                border-radius: 5px;
            }
            #githubButton {
                background-color: #24292e;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            #githubButton:hover {
                background-color: #2f363d;
            }
            #versionLabel {
                color: #0d6efd;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        # Initialize variables
        self.clicking = False
        self.click_thread = None
        self.click_type = "left"
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("PrecisionClicker Lite")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0d6efd;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Version with GitHub username
        version_label = QLabel("v1.0 | @AliAkgun0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #555555;")
        layout.addWidget(line)
        
        # Click type selection
        click_frame = QFrame()
        click_layout = QVBoxLayout(click_frame)
        click_type_label = QLabel("Click Type:")
        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(["Left Click", "Right Click", "Middle Click"])
        click_layout.addWidget(click_type_label)
        click_layout.addWidget(self.click_type_combo)
        layout.addWidget(click_frame)
        
        # Interval selection
        interval_frame = QFrame()
        interval_layout = QVBoxLayout(interval_frame)
        interval_label = QLabel("Interval (ms):")
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 10000)
        self.interval_spin.setValue(1000)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.interval_spin)
        layout.addWidget(interval_frame)
        
        # Status label
        self.status_label = QLabel("Press F6 to start/stop clicking")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #0d6efd; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # GitHub button
        github_frame = QFrame()
        github_layout = QVBoxLayout(github_frame)
        self.github_button = QPushButton("Visit My GitHub")
        self.github_button.setObjectName("githubButton")
        self.github_button.clicked.connect(lambda: webbrowser.open('https://github.com/AliAkgun0'))
        github_layout.addWidget(self.github_button)
        layout.addWidget(github_frame)
        
        # About
        about_frame = QFrame()
        about_layout = QVBoxLayout(about_frame)
        about_label = QLabel("A modern auto-clicker with advanced features.\nBuilt with Python and PyQt5.")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setWordWrap(True)
        about_layout.addWidget(about_label)
        layout.addWidget(about_frame)
        
        # Connect signals
        self.click_type_combo.currentTextChanged.connect(self.update_click_type)
        
        # Setup hotkey
        keyboard.on_press_key("F6", self.toggle_clicking)
    
    def update_click_type(self, text):
        self.click_type = text.lower().split()[0]
    
    def toggle_clicking(self, _):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        self.clicking = True
        self.status_label.setText("Status: Clicking... (Press F6 to stop)")
        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.daemon = True
        self.click_thread.start()
    
    def stop_clicking(self):
        self.clicking = False
        self.status_label.setText("Status: Stopped (Press F6 to start)")
        if self.click_thread:
            self.click_thread.join(timeout=1.0)
    
    def click_loop(self):
        while self.clicking:
            # Get current mouse position
            current_pos = pyautogui.position()
            
            # Perform click
            if self.click_type == "left":
                pyautogui.click(current_pos[0], current_pos[1])
            elif self.click_type == "right":
                pyautogui.rightClick(current_pos[0], current_pos[1])
            else:  # middle
                pyautogui.middleClick(current_pos[0], current_pos[1])
            
            # Wait for the specified interval
            time.sleep(self.interval_spin.value() / 1000.0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrecisionClicker()
    window.show()
    sys.exit(app.exec_()) 