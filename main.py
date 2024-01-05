import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget, QSplitter, QSizePolicy, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

# Login Module
from sudo_input import get_sudo_password
from authentication import get_sudo_password

# Level 1 Modules
from update_module import Update
from port_blocking_module import PortBlocking
from antivirus_module import AntiVirusModule
from website_blocking_module import WebsiteBlockingModule
from geniune_os_module import Genuinity
from block_DNS_module import BlockDNSModule
from rtp_port_module import BlockRTPModule
from bluetooth_module import BluetoothModule

# Level 2 Modules
from patch_management_module import PatchManagementModule
from file_permission_module import FilePermissionModule
from cryptography_module import CryptographyModule
from ssh_module import SSHConfigurationModule
from firewall_management_module import FirewallManagementModule
from password_policy_module import PasswordPolicyModule

# Level 3 Modules
from patch_advanced_module import PatchManagementAdvancedModule
from file_integrity_module import FileIntegrityCheckModule
from user_and_group_module import UserGroupManagementModule
from ssh_advanced_module import SSHAdvancedModule

class UbuntuHardeningApp(QMainWindow):
    def __init__(self):
        super(UbuntuHardeningApp, self).__init__()

        # Initialize features for each level
        self.level_features = {
            'Level 1': [
                'Updates',
                'Port Blocking',
                'Antivirus and Antispy Check',
                'Website Blocking',
                'Block DNS',
                'Block RTP',
                'Block Bluetooth'
            ],
            'Level 2': [
                'Patch Management',
                'File Permission',
                'Cryptography',
                'SSH Hardening',
                'Firewall Management',
                'Password Policy'
            ],
            'Level 3': [
                'Patch Management Advanced',
                'File Integrity Check',
                'User and Group Management',
                'Firewall Advanced',
                'SELinux',
                'Application Whitelisting',
                'SSH Hardening Advanced'
            ]
        }

        # Set default level
        self.current_level = 'Level 1'
        self.selected_level_button = None
        self.selected_feature_button = None
        self.feature_buttons = []  # Store references to feature buttons

        # Ask user for sudo password
        self.sudo_password = get_sudo_password()
        if self.sudo_password is None:
            sys.exit()  # Exit the application if the user cancels password input

        self.init_ui()
        self.set_default_level()  # Set the default level and apply the selected color

    def init_ui(self):
        self.setWindowTitle('Ubuntu Hardening App')
        self.setGeometry(100, 100, 800, 600)

        # Apply a modern stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #3498db;
                color: black;
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2c7cb7;
                border: 1px solid #2c7cb7;
            }
            QPushButton:selected {
                background-color: #004080;  /* Dark Blue */
                color: white;
                border: 1px solid #004080;
            }
            QLabel {
                font-size: 18px;
                padding: 10px;
                color: black;
            }
            QFrame {
                background-color: #f0f0f0;
                height: 2px;
                margin: 5px 0px;
            }
            QStackedWidget {
                border: 2px solid #3498db;
                border-radius: 5px;
            }
        ''')

        # Create a central widget to hold the top bar, side menu, and stacked widget
        central_widget = QWidget()

        # Create a vertical layout for the central widget
        central_layout = QVBoxLayout(central_widget)

        # Create a top bar with hardening levels
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.level1_button = QPushButton('Level 1')
        self.level2_button = QPushButton('Level 2')
        self.level3_button = QPushButton('Level 3')

        self.level1_button.clicked.connect(self.set_level_1)
        self.level2_button.clicked.connect(self.set_level_2)
        self.level3_button.clicked.connect(self.set_level_3)

        top_bar_layout.addWidget(self.level1_button)
        top_bar_layout.addWidget(self.level2_button)
        top_bar_layout.addWidget(self.level3_button)

        # Add a QFrame as a horizontal line separator
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)

        # Create a QSplitter to manage the side menu and the stacked widget
        splitter = QSplitter(Qt.Horizontal)

        # Set the stretch factor for the top bar to 0, making it take minimum space
        splitter.setStretchFactor(0, 0)
        # Set the stretch factor for the stacked widget to 4
        splitter.setStretchFactor(1, 4)

        # Create a side menu
        self.side_menu = QWidget()
        self.side_menu_layout = QVBoxLayout(self.side_menu)

        # Add title and buttons to the layout
        self.update_side_menu()

        # Create a stacked widget for dynamic content on the right
        self.stacked_widget = QStackedWidget()

        # Add placeholder widgets for features
        self.firewall_widget = QLabel('Select Option from Menu')

        self.stacked_widget.addWidget(self.firewall_widget)

        # Add side menu and stacked widget to the splitter
        splitter.addWidget(self.side_menu)
        splitter.addWidget(self.stacked_widget)

        # Add the top bar, separator, and splitter to the central layout
        central_layout.addWidget(top_bar)
        central_layout.addWidget(separator_line)
        central_layout.addWidget(splitter)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def update_side_menu(self):
        # Clear existing feature buttons and their references
        for i in reversed(range(self.side_menu_layout.count())):
            item = self.side_menu_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Add menu title
        menu_title = QLabel('Menu')
        menu_title.setAlignment(Qt.AlignCenter)  # Align the title in the center
        menu_title.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.side_menu_layout.addWidget(menu_title)

        # Add feature buttons based on the current level
        features = self.level_features[self.current_level]

        # Clear existing feature buttons and their references
        self.feature_buttons = []

        for feature in features:
            button = QPushButton(feature)
            button.clicked.connect(self.show_feature)
            button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

            # Level 1

            if feature == 'Updates':
                button.clicked.connect(self.show_update_content)

            if feature == 'Port Blocking (USB)':
                button.clicked.connect(self.show_port_blocking_content)

            if feature == 'Antivirus and Antispy Check':
                button.clicked.connect(self.show_antivirus_content)

            if feature == 'Website Blocking':
                button.clicked.connect(self.show_website_blocking_content)

            if feature == 'Block DNS':
                button.clicked.connect(self.show_block_DNS_content)

            if feature == 'Block RTP':
                button.clicked.connect(self.show_block_RTP_content)

            if feature == 'Block Bluetooth':
                button.clicked.connect(self.show_block_bluetooth_content)

            if feature == 'Ubuntu OS Genuinity':
                button.clicked.connect(self.show_os_genuine_content)

            # Level 2

            if feature == 'Patch Management':
                button.clicked.connect(self.show_patch_management_content)

            if feature == 'File Permission':
                button.clicked.connect(self.show_file_permission_content)

            if feature == 'Cryptography':
                button.clicked.connect(self.show_cryptography_content)

            if feature == 'SSH Hardening':
                button.clicked.connect(self.show_ssh_content)

            if feature == 'Firewall Management':
                button.clicked.connect(self.show_firewall_content)

            if feature == 'Password Policy':
                button.clicked.connect(self.show_password_content)

            # Level 3

            if feature == 'Patch Management Advanced':
                button.clicked.connect(self.show_patch_advanced_content)

            if feature == 'File Integrity Check':
                button.clicked.connect(self.show_file_integrity_content)

            if feature == 'User and Group Management':
                button.clicked.connect(self.show_user_and_group_content)

            if feature == 'SSH Hardening Advanced':
                button.clicked.connect(self.show_ssh_advanced_content)

            self.side_menu_layout.addWidget(button)
            self.feature_buttons.append(button)  # Store references to feature buttons

    def show_feature(self):
        # Implement feature display logic here
        sender = self.sender()
        feature_name = sender.text()
        print(f"Displaying content for {feature_name}")

        # Update the style of the selected feature button
        self.update_feature_button_style(sender)

    def update_feature_button_style(self, button):
        # Update the style of the selected feature button
        if self.selected_feature_button:
            self.selected_feature_button.setStyleSheet('QPushButton { background-color: #3498db; color: black; border: 1px solid #3498db; border-radius: 5px; padding: 5px; margin: 5px; }')
        button.setStyleSheet('QPushButton { background-color: #004080; color: white; border: 1px solid #004080; border-radius: 5px; padding: 5px; margin: 5px; }')
        self.selected_feature_button = button

    def set_default_level(self):
        # Set the default level and update the side menu
        self.update_side_menu()
        print("Setting Default Level")

        # Update the style of the selected level button
        self.update_level_button_style(self.level1_button)

    def set_level_1(self):
        # Set the current level to 1 and update the side menu
        self.current_level = 'Level 1'
        self.update_side_menu()
        print("Setting Hardening Level 1")

        # Update the style of the selected level button
        self.update_level_button_style(self.level1_button)

    def set_level_2(self):
        # Set the current level to 2 and update the side menu
        self.current_level = 'Level 2'
        self.update_side_menu()
        print("Setting Hardening Level 2")

        # Update the style of the selected level button
        self.update_level_button_style(self.level2_button)

    def set_level_3(self):
        # Set the current level to 3 and update the side menu
        self.current_level = 'Level 3'
        self.update_side_menu()
        print("Setting Hardening Level 3")

        # Update the style of the selected level button
        self.update_level_button_style(self.level3_button)

    def update_level_button_style(self, button):
        # Update the style of the selected level button
        level_buttons = [self.level1_button, self.level2_button, self.level3_button]

        if button in level_buttons and button != self.selected_level_button:
            if self.selected_level_button:
                self.selected_level_button.setStyleSheet('QPushButton { background-color: #3498db; color: black; border: 1px solid #3498db; border-radius: 5px; padding: 5px; margin: 5px; }')
            button.setStyleSheet('QPushButton { background-color: #004080; color: white; border: 1px solid #004080; border-radius: 5px; padding: 5px; margin: 5px; }')
            self.selected_level_button = button

    # Level 1 Functions

    def show_update_content(self):
        update_content = Update(self.sudo_password)
        self.stacked_widget.addWidget(update_content)
        self.stacked_widget.setCurrentWidget(update_content)

    def show_port_blocking_content(self):
        port_blocking_content = PortBlocking(self.sudo_password)
        self.stacked_widget.addWidget(port_blocking_content)
        self.stacked_widget.setCurrentWidget(port_blocking_content)

    def show_antivirus_content(self):
        # Display the Antivirus content in the stacked widget
        antivirus_content = AntiVirusModule(self.sudo_password)
        self.stacked_widget.addWidget(antivirus_content)
        self.stacked_widget.setCurrentWidget(antivirus_content)

    def show_website_blocking_content(self):
        website_blocking_content = WebsiteBlockingModule(self.sudo_password)
        self.stacked_widget.addWidget(website_blocking_content)
        self.stacked_widget.setCurrentWidget(website_blocking_content)

    def show_block_DNS_content(self):
        # Display the block DNS  content in the stacked widget
        block_DNS_content = BlockDNSModule(self.sudo_password)
        self.stacked_widget.addWidget(block_DNS_content)
        self.stacked_widget.setCurrentWidget(block_DNS_content)

    def show_block_RTP_content(self):
        # Display the block DNS  content in the stacked widget
        block_RTP_content = BlockRTPModule(self.sudo_password)
        self.stacked_widget.addWidget(block_RTP_content)
        self.stacked_widget.setCurrentWidget(block_RTP_content)

    def show_block_bluetooth_content(self):
        block_bluetooth_content = BluetoothModule(self.sudo_password)
        self.stacked_widget.addWidget(block_bluetooth_content)
        self.stacked_widget.setCurrentWidget(block_bluetooth_content)

    def show_os_genuine_content(self):
        os_genuine_content = Genuinity(self.sudo_password)
        self.stacked_widget.addWidget(os_genuine_content)
        self.stacked_widget.setCurrentWidget(os_genuine_content)

    # Level 2 Functions

    def show_patch_management_content(self):
        # Display the patch management content in the stacked widget
        patch_management_content = PatchManagementModule(self.sudo_password)
        self.stacked_widget.addWidget(patch_management_content)
        self.stacked_widget.setCurrentWidget(patch_management_content)

    def show_file_permission_content(self):
         # Display the file permission content in the stacked widget
        file_permission_content = FilePermissionModule(self.sudo_password)
        self.stacked_widget.addWidget(file_permission_content)
        self.stacked_widget.setCurrentWidget(file_permission_content)

    def show_cryptography_content(self):
        # Check if the current level is 'Level 2' and if the 'Cryptography' feature is selected
        cryptography_content = CryptographyModule(self.sudo_password)
        self.stacked_widget.addWidget(cryptography_content)
        self.stacked_widget.setCurrentWidget(cryptography_content)

    def show_ssh_content(self):
        ssh_content = SSHConfigurationModule(self.sudo_password)
        self.stacked_widget.addWidget(ssh_content)
        self.stacked_widget.setCurrentWidget(ssh_content)

    def show_firewall_content(self):
        firewall_content = FirewallManagementModule(self.sudo_password)
        self.stacked_widget.addWidget(firewall_content)
        self.stacked_widget.setCurrentWidget(firewall_content)

    def show_password_content(self):
        password_content = PasswordPolicyModule(self.sudo_password)
        self.stacked_widget.addWidget(password_content)
        self.stacked_widget.setCurrentWidget(password_content)

    # Level 3 Functions

    def show_patch_advanced_content(self):
        patch_advanced_content = PatchManagementAdvancedModule(self.sudo_password)
        self.stacked_widget.addWidget(patch_advanced_content)
        self.stacked_widget.setCurrentWidget(patch_advanced_content)

    def show_file_integrity_content(self):
        file_integrity_content = FileIntegrityCheckModule(self.sudo_password)
        self.stacked_widget.addWidget(file_integrity_content)
        self.stacked_widget.setCurrentWidget(file_integrity_content)

    def show_user_and_group_content(self):
        user_and_group_content = UserGroupManagementModule(self.sudo_password)
        self.stacked_widget.addWidget(user_and_group_content)
        self.stacked_widget.setCurrentWidget(user_and_group_content)

    def show_ssh_advanced_content(self):
        ssh_advanced_content = SSHAdvancedModule(self.sudo_password)
        self.stacked_widget.addWidget(ssh_advanced_content)
        self.stacked_widget.setCurrentWidget(ssh_advanced_content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UbuntuHardeningApp()
    window.show()
    sys.exit(app.exec_())
