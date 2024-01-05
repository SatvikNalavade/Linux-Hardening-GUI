from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess


class AntiVirusModule(QWidget):
    def __init__(self, sudo_password):
        super(AntiVirusModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        check_button = QPushButton('Check Installation')
        check_button.clicked.connect(self.run_check_script)
        layout.addWidget(check_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"echo '{self.sudo_password}' | sudo -S bash -c '{command}'"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def run_check_script(self):
        self.run_script("""tools=("clamav" "sophos-av" "esetnod32av" "bitdefender-scanner" "comodo")

                            echo "Checking for the availability of antivirus and anti-spyware tools:"

                            for tool in "${tools[@]}"; do
                                echo -n "Checking $tool..."

                                if command -v $tool &> /dev/null; then
                                    echo " Installed"
                                else
                                    echo " Not Installed"
                                fi
                            done

                            echo "Done."
                            """)

    def run_install_script(self):
        self.run_script("""
            # Check if ClamAV is already installed
            if command -v clamscan &> /dev/null; then
                echo "ClamAV is already installed. No action taken."
            else
                # Update package lists
                sudo apt update

                # Install ClamAV
                sudo apt install -y clamav

                # Install ClamAV's scanning engine
                sudo apt install -y clamav-daemon

                # Start the ClamAV service
                sudo systemctl start clamav-daemon

                # Enable the ClamAV service to start on boot
                sudo systemctl enable clamav-daemon

                # Print completion message
                echo "ClamAV installed successfully."
            fi
        """)



