# Twitch Image Resizer

A simple script to resize images to Twitch's required sizes (112x112, 56x56, 28x28) and save them in a folder with the same name as the original image. This project also includes instructions for integrating the script with macOS Finder using Automator and AppleScript.

## Prerequisites

- Python 3.x
- Pillow library

## Installation

1. Install the Pillow library:

    ```bash
    pip3 install Pillow
    ```

2. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/Twitch-Image-Resizer.git
    ```

## Usage

1. Open Terminal.
2. Navigate to the project directory:

    ```bash
    cd path/to/Twitch-Image-Resizer
    ```

3. Run the script with the path to your image:

    ```bash
    python3 main.py /path/to/your/image.png
    ```

## Integrate with Finder using Automator and AppleScript

### Create AppleScript

1. Open `Script Editor` on your Mac.
2. Paste the following AppleScript code:

    ```applescript
    on run {input, parameters}
        set inputPath to POSIX path of item 1 of input
        set scriptPath to "/path/to/your/main.py"
        set pythonPath to "/path/to/your/python3"

        do shell script quoted form of pythonPath & " " & quoted form of scriptPath & " " & quoted form of inputPath

        return input
    end run
    ```

3. Save this script as an application, for example, `Twitch Images.app`.

### Create Automator Service

1. Open Automator and create a new service.
2. Set "Service receives selected" to "files or folders" in "Finder".
3. Add the action "Run AppleScript".
4. Paste the following AppleScript code into the action:

    ```applescript
    on run {input, parameters}
        tell application "Twitch Images.app" to open input
    end run
    ```

5. Save the service with a name like "Twitch Image Resizer".

### Using the Service

1. In Finder, right-click on any image file.
2. Select "Twitch Image Resizer" from the context menu.
3. The script will create a folder with the same name as the original image and save the resized images in that folder.

## License

This project is licensed under the MIT License.
