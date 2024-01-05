import os
import sys
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMainWindow, QVBoxLayout, QLabel, QPushButton, QApplication, QWidget, QMessageBox
from authentication import get_sudo_password

class SudoInputDialog(QMainWindow):
    def __init__(self):
        super(SudoInputDialog, self).__init__()
        self.setWindowTitle('Login')

        # Get the current username
        self.current_username = os.getlogin()

        # Create widgets
        self.username_label = QLabel(f'<font color="#3498db">Username: {self.current_username}</font>')
        self.password_label = QLabel('<font color="#3498db">Password:</font>')

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.cancel_button = QPushButton('Cancel')

        # Set up layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.username_label)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.cancel_button)

        # Apply modern stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: #ecf0f1;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 1px solid #2980b9;
            }
        ''')

        # Connect signals
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.close)

    def handle_login(self):
        # Only close the dialog if a password is provided
        password = self.password_input.text()
        if password:
            # Check the password with the sudo script
            if run_sudo_script(password):
                self.close()
            else:
                QMessageBox.warning(self, 'Sudo Script Failed', 'Please re-enter your sudo password.')
        else:
            QMessageBox.warning(self, 'Empty Password', 'Please enter a password.')

    def get_credentials(self):
        self.show()
        QApplication.processEvents()
        app = QApplication.instance()  # Get the existing instance of QApplication
        app.exec_()

        return self.current_username, self.password_input.text()

def get_sudo_password():
    sudo_input_dialog = SudoInputDialog()
    username, password = sudo_input_dialog.get_credentials()

    if password:
        return password
    else:
        QMessageBox.warning(None, 'Operation Canceled', 'You canceled the operation. The application will exit.')
        return None

if __name__ == '__main__':
    sudo_password = get_sudo_password()

    if sudo_password is not None:
        app = QApplication(sys.argv)
        window = UbuntuHardeningApp(sudo_password)
        window.show()
        sys.exit(app.exec_())
