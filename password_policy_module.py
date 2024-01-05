from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QInputDialog
import subprocess

class PasswordPolicyModule(QWidget):
    def __init__(self, sudo_password):
        super(PasswordPolicyModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        # Set Minimum Days Button
        minDays_button = QPushButton('Set Minimum Days')
        minDays_button.clicked.connect(self.set_min_days)
        layout.addWidget(minDays_button)

        # Set Maximum Days Button
        maxDays_button = QPushButton('Set Maximum Days')
        maxDays_button.clicked.connect(self.set_max_days)
        layout.addWidget(maxDays_button)

        # Set Expiration Button
        expiration_button = QPushButton('Set Expiration Date')
        expiration_button.clicked.connect(self.set_expiration_date)
        layout.addWidget(expiration_button)

        # Set Password Strength Button
        strength_button = QPushButton('Set Password Strength')
        strength_button.clicked.connect(self.set_password_strength)
        layout.addWidget(strength_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"sudo -S bash -c '{command}'"
        process = subprocess.Popen(full_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ensure sudo_password is a string
        sudo_password = str(self.sudo_password) + '\n'

        stdout, stderr = process.communicate(input=sudo_password)

        if process.returncode == 0:
            self.result_label.setText(stdout)
        else:
            self.result_label.setText(f"Error: {stderr}")

    def set_min_days(self):
        username, ok_pressed = QInputDialog.getText(self, 'Set Minimum Days', 'Enter username:')
        if ok_pressed:
            min_days, ok_pressed = QInputDialog.getInt(self, 'Set Minimum Days', 'Enter minimum days:')
            if ok_pressed:
                self.run_script(f"sudo chage -m {min_days} {username}")

    def set_max_days(self):
        username, ok_pressed = QInputDialog.getText(self, 'Set Maximum Days', 'Enter username:')
        if ok_pressed:
            max_days, ok_pressed = QInputDialog.getInt(self, 'Set Maximum Days', 'Enter maximum days:')
            if ok_pressed:
                self.run_script(f"sudo chage -M {max_days} {username}")

    def set_expiration_date(self):
        username, ok_pressed = QInputDialog.getText(self, 'Set Expiration Date', 'Enter username:')
        if ok_pressed:
            expiration_date, ok_pressed = QInputDialog.getText(self, 'Set Expiration Date', 'Enter expiration date (YYYY-MM-DD):')
            if ok_pressed:
                self.run_script(f"sudo chage -E {expiration_date} {username}")

    def set_password_strength(self):
        # The script for setting password strength as mentioned in the reference
        script = """
        sudo apt-get install libpam-pwquality
        echo "minlen = 12" | sudo tee -a /etc/security/pwquality.conf
        echo "minclass = 3" | sudo tee -a /etc/security/pwquality.conf
        echo "minrepeat = 3" | sudo tee -a /etc/security/pwquality.conf
        echo "password requisite pam_pwquality.so retry=3" | sudo tee -a /etc/security/pam_common-password
        echo "libpam-pwquality is installed and configured."
        """
        self.run_script(script)
