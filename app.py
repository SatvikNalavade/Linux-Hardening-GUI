from flask import Flask, render_template, request, flash
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to run a command with sudo
def run_command_with_sudo(command, password):
    try:
        command = f'echo {password} | sudo -S {command}'
        subprocess.run(command, shell=True, check=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return True, f"Command executed successfully: {command}"
    except subprocess.CalledProcessError as e:
        return False, f"Error executing command: {e.stderr}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        ufw_status = request.form.get('ufw_toggle', 0)
        incoming = request.form.get('incoming_toggle', 0)
        outgoing = request.form.get('outgoing_toggle', 0)
        ssh = request.form.get('ssh_toggle', 0)

        if not password:
            flash("Please enter your sudo password.", 'error')
        else:
            # Toggle UFW
            if ufw_status == '1':
                success, message = run_command_with_sudo("sudo ufw enable", password)
            else:
                success, message = run_command_with_sudo("sudo ufw disable", password)

            if not success:
                flash(message, 'error')

            # Configure UFW rules
            if incoming == '1':
                success, message = run_command_with_sudo("sudo ufw default allow incoming", password)
            else:
                success, message = run_command_with_sudo("sudo ufw default deny incoming", password)

            if not success:
                flash(message, 'error')

            if outgoing == '1':
                success, message = run_command_with_sudo("sudo ufw default allow outgoing", password)
            else:
                success, message = run_command_with_sudo("sudo ufw default deny outgoing", password)

            if not success:
                flash(message, 'error')

            if ssh == '1':
                success, message = run_command_with_sudo("sudo ufw allow ssh", password)
            else:
                success, message = run_command_with_sudo("sudo ufw delete allow ssh", password)

            if not success:
                flash(message, 'error')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
