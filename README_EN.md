# mht2md_gui

[中文](README.md)

## Project From 
[githubJonesckevin/mht2md ](https://github.com/Jonesckevin/mht2md)

## Modifications
1. Modified the Markdown format to store images in a subdirectory under Markdown for a clearer directory structure

2. Added a GUI interface and actions for automatic compilation into executable tools on Windows and Linux, making it easier for users without a Python interpreter

## How to Use the Project
### Directly Download Releases 

### Compile by Yourself
1. Clone the code

`git clone https://github.com/noob3-3/mht2md_gui`

2. Switch directory

`cd mht2md_gui`

3. Install dependencies

`pip install -r requirements.txt`

4. Compile the executable file

`pyinstaller --onefile --windowed mht2MarkdownGui.py`

### Open the software, select the MHT file, and once the progress bar finishes, check the folder with the same name as the MHT file in the same directory, and start editing the Markdown 
