from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess

class BluetoothModule(QWidget):
    def __init__(self, sudo_password):
        super(BluetoothModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        disable_button = QPushButton('Disable Bluetooth')
        disable_button.clicked.connect(self.disable_bluetooth)
        layout.addWidget(disable_button)

        enable_button = QPushButton('Enable Bluetooth')
        enable_button.clicked.connect(self.enable_bluetooth)
        layout.addWidget(enable_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"echo {self.sudo_password} | sudo -S {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def disable_bluetooth(self):
        # Disable Bluetooth service
        self.run_script("systemctl stop bluetooth")
        # Prevent Bluetooth service from starting on boot
        self.run_script("sudo systemctl disable bluetooth")

    def enable_bluetooth(self):
        # Enable Bluetooth service
        self.run_script("sudo systemctl enable bluetooth")
        # Start Bluetooth service
        self.run_script("sudo systemctl start bluetooth")

# Example usage:
# sudo_password = "your_password"
# bluetooth_module = BluetoothControlModule(sudo_password)
# bluetooth_module.show()
