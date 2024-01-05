from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess
import tempfile
import os


class PortBlocking(QWidget):
    def __init__(self, sudo_password):
        super(PortBlocking, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        disable_button = QPushButton('Disable')
        disable_button.clicked.connect(self.run_disable_script)
        layout.addWidget(disable_button)

        enable_button = QPushButton('Enable')
        enable_button.clicked.connect(self.run_enable_script)
        layout.addWidget(enable_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, script):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(script)
            temp_file_path = temp_file.name

        try:
            full_command = f"echo {self.sudo_password} | sudo -S bash {temp_file_path}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.result_label.setText(result.stdout)
            else:
                self.result_label.setText(f"Error: {result.stderr}")

        finally:
            os.remove(temp_file_path)

    def run_disable_script(self):
        disable_script = """
                            #!/bin/bash

                            # Disable USB ports
                            for port in /sys/bus/usb/devices/*/authorized; do
                              echo 0 > "$port"
                            done

                            echo "Ports disabled successfully."
        """
        self.run_script(disable_script)

    def run_enable_script(self):
        enable_script = """
                            #!/bin/bash

                            # Enable USB ports
                            for port in /sys/bus/usb/devices/*/authorized; do
                              echo 1 > "$port"
                            done

                            echo "Ports enabled successfully."
        """
        self.run_script(enable_script)

