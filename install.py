import subprocess

# List of libraries to install
libraries = ['tkinter', 'datetime']

# Install each library
for lib in libraries:
    subprocess.run(['pip', 'install', lib])
