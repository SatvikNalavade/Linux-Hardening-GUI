from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess

class BlockDNSModule(QWidget):
    def __init__(self, sudo_password):
        super(BlockDNSModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        blockDNSPort_button = QPushButton('Block DNS Port')
        blockDNSPort_button.clicked.connect(self.run_blockDNSport_script)
        layout.addWidget(blockDNSPort_button)

        blockDNSProtocol_button = QPushButton('Block DNS Protocol')
        blockDNSProtocol_button.clicked.connect(self.run_blockDNSprotocol_script)
        layout.addWidget(blockDNSProtocol_button)

        UnblockDNSPort_button = QPushButton('Unblock DNS Port')
        UnblockDNSPort_button.clicked.connect(self.run_unblockDNSPort_script)
        layout.addWidget(UnblockDNSPort_button)

        UnblockDNSProtocol_button = QPushButton('Unblock DNS Protocol')
        UnblockDNSProtocol_button.clicked.connect(self.run_unblockDNSProtocol_script)
        layout.addWidget(UnblockDNSProtocol_button)

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


    def run_blockDNSport_script(self):
        self.run_script("""
iptables -F
iptables -A INPUT -p udp --dport 53 -j DROP
iptables -A OUTPUT -p udp --dport 53 -j DROP
iptables -A INPUT -p tcp --dport 53 -j DROP
iptables -A OUTPUT -p tcp --dport 53 -j DROP
echo "DNS port disabled"
""")

    def run_blockDNSprotocol_script(self):
        self.run_script("""
iptables -F
iptables -A INPUT -p udp --sport 53 -j DROP
iptables -A OUTPUT -p udp --sport 53 -j DROP
iptables -A INPUT -p tcp --sport 53 -j DROP
iptables -A OUTPUT -p tcp --sport 53 -j DROP
echo "DNS protocol disabled"
""")

    def run_unblockDNSPort_script(self):
        self.run_script("""
iptables -F
iptables -A INPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT
echo "DNS port Enabled"
""")

    def run_unblockDNSProtocol_script(self):
        self.run_script("""
iptables -F
iptables -A INPUT -p udp --sport 53 -j ACCEPT
iptables -A OUTPUT -p udp --sport 53 -j ACCEPT
iptables -A INPUT -p tcp --sport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 53 -j ACCEPT
echo "DNS protocol Enabled"
""")
