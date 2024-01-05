from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog
import subprocess

class SSHConfigurationModule(QWidget):
    def __init__(self, sudo_password):
        super(SSHConfigurationModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        connection_limit_button = QPushButton('Set Connection Limit')
        connection_limit_button.clicked.connect(self.set_connection_limit)
        layout.addWidget(connection_limit_button)

        timeout_button = QPushButton('Set Idle Timeout')
        timeout_button.clicked.connect(self.set_idle_timeout)
        layout.addWidget(timeout_button)

        disable_ssh1_button = QPushButton('Disable SSH 1 Protocol')
        disable_ssh1_button.clicked.connect(self.disable_ssh1_protocol)
        layout.addWidget(disable_ssh1_button)

        enable_ssh1_button = QPushButton('Enable SSH 1 Protocol')
        enable_ssh1_button.clicked.connect(self.enable_ssh1_protocol)
        layout.addWidget(enable_ssh1_button)

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

    def set_connection_limit(self):
        # Input dialog to get the maximum number of allowed SSH connections
        max_connections, ok = QInputDialog.getInt(self, 'SSH Configuration', 'Enter Max Connections:', 10, 1, 100)
        if ok:
            self.run_script(f"echo 'MaxSessions {max_connections}' | sudo tee -a /etc/ssh/sshd_config")
            self.result_label.setText("Connection limit updated. Please restart the SSH service.")

    def set_idle_timeout(self):
        # Input dialog to get the SSH idle timeout value
        idle_timeout, ok = QInputDialog.getInt(self, 'SSH Configuration', 'Enter Idle Timeout (seconds):', 300, 60, 3600)
        if ok:
            self.run_script(f"echo 'ClientAliveInterval {idle_timeout}' | sudo tee -a /etc/ssh/sshd_config")
            self.run_script("echo 'ClientAliveCountMax 0' | sudo tee -a /etc/ssh/sshd_config")
            self.result_label.setText("Idle timeout updated. Please restart the SSH service.")

    def disable_ssh1_protocol(self):
        # Disable SSH 1 protocol
        self.run_script("sudo sed -i 's/Protocol 1/Protocol 2/' /etc/ssh/sshd_config")
        self.result_label.setText("SSH 1 protocol disabled. Please restart the SSH service.")

    def enable_ssh1_protocol(self):
        # Enable SSH 1 protocol
        self.run_script("sudo sed -i 's/Protocol 2/Protocol 1/' /etc/ssh/sshd_config")
        self.result_label.setText("SSH 1 protocol enabled. Please restart the SSH service.")
