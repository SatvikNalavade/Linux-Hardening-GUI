from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QPlainTextEdit
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import Qt
import subprocess

class FirewallManagementModule(QWidget):
    def __init__(self, sudo_password):
        super(FirewallManagementModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        enable_button = QPushButton('Enable Firewall')
        enable_button.clicked.connect(self.enable_firewall)
        layout.addWidget(enable_button)

        disable_button = QPushButton('Disable Firewall')
        disable_button.clicked.connect(self.disable_firewall)
        layout.addWidget(disable_button)

        status_button = QPushButton('Check Firewall Status')
        status_button.clicked.connect(self.check_firewall_status)
        layout.addWidget(status_button)

        # Result textbox for displaying firewall status
        self.result_textbox = QPlainTextEdit()
        self.result_textbox.setReadOnly(True)

        # Set text color to blue
        char_format = QTextCharFormat()
        char_format.setForeground(Qt.blue)
        self.result_textbox.setCurrentCharFormat(char_format)

        layout.addWidget(self.result_textbox)

        # Checkboxes for specific firewall rules
        self.checkboxes = {
            'deny_incoming': QCheckBox('ufw default deny incoming'),
            'allow_outgoing': QCheckBox('ufw default allow outgoing'),
            'allow_ssh': QCheckBox('ufw allow 22/tcp # allow incoming SSH traffic'),
            'allow_http': QCheckBox('ufw allow 80/tcp # allow incoming HTTP traffic'),
            'allow_https': QCheckBox('ufw allow 443/tcp # allow incoming HTTPS traffic'),
            'allow_openvpn': QCheckBox('ufw allow 1194/udp # allow OpenVPN traffic'),
        }

        for checkbox in self.checkboxes.values():
            checkbox.setStyleSheet('QCheckBox { color: blue; }'
                                   'QCheckBox::indicator { background-color: white; border: 1px solid black; }'  # Set border
                                   'QCheckBox:checked { background-color: lightblue; }')  # Set background color for checked state
            layout.addWidget(checkbox)

        # Apply button
        self.apply_button = QPushButton('Apply Rules')
        self.apply_button.clicked.connect(self.apply_firewall_rules)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def set_apply_button_state(self, enabled):
        self.apply_button.setEnabled(enabled)

    def run_script(self, command):
        full_command = f"echo {self.sudo_password} | sudo -S {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_textbox.appendPlainText(result.stdout)
        else:
            error_message = f"Error ({result.returncode}): {result.stderr}"
            self.result_textbox.appendPlainText(error_message)

    def enable_firewall(self):
        enable_command = "ufw enable"
        self.run_script(enable_command)
        self.set_apply_button_state(True)  # Enable the "Apply Rules" button

    def disable_firewall(self):
        disable_command = "ufw disable"
        self.run_script(disable_command)
        self.set_apply_button_state(False)  # Disable the "Apply Rules" button

    def check_firewall_status(self):
        status_command = "ufw status"
        self.run_script(status_command)

        # Check the status of each checkbox based on the current rules
        for checkbox, command in zip(self.checkboxes.values(), self.get_firewall_rule_commands()):
            checkbox.setChecked(command in self.result_textbox.toPlainText())

    def apply_firewall_rules(self):
        # Get the commands for the selected and unselected rules
        selected_commands = [command for checkbox, command in zip(self.checkboxes.values(), self.get_firewall_rule_commands()) if checkbox.isChecked()]

        # Disable the selected rules and enable the unselected rules
        disable_commands = [f"ufw --force delete {command}" for command in self.get_firewall_rule_commands() if command not in selected_commands]
        enable_commands = [f"ufw --force insert 1 {command}" for command in selected_commands]

        # Execute the commands
        for command in disable_commands + enable_commands:
            self.run_script(command)

        # Refresh the firewall status
        self.check_firewall_status()

    def get_firewall_rule_commands(self):
        return [
            'ufw default deny incoming',
            'ufw default allow outgoing',
            'ufw allow 22/tcp',  # allow incoming SSH traffic
            'ufw allow 80/tcp',  # allow incoming HTTP traffic
            'ufw allow 443/tcp',  # allow incoming HTTPS traffic
            'ufw allow 1194/udp',  # allow OpenVPN traffic
        ]
