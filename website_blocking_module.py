from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox
import subprocess

class WebsiteBlockingModule(QWidget):
    def __init__(self, sudo_password):
        super(WebsiteBlockingModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        add_website_button = QPushButton('Add Website to Blocklist')
        add_website_button.clicked.connect(self.add_website_to_blocklist)
        layout.addWidget(add_website_button)

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

    def add_website_to_blocklist(self):
        # Input dialog to get the website to block
        website, ok = QInputDialog.getText(self, 'Website Blocking', 'Enter Website to Block:')
        if ok and website:
            # Add a wildcard for subdomains
            block_entry = f'127.0.0.1 {website} www.{website} *.{website}'
            self.run_script(f"echo '{block_entry}' | sudo tee -a /etc/hosts")
            self.result_label.setText(f"Website {website} and its subdomains added to blocklist.")
        elif not website and not ok:
            # User pressed Cancel
            pass
        else:
            QMessageBox.warning(self, 'Website Blocking', 'Please enter a website to block.')
