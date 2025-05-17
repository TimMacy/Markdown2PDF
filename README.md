# Markdown2PDF <a href="#-changelog"><img align="right" src="https://img.shields.io/badge/Version-17-white.svg" alt="Version: 17"></a>&nbsp;<a href="https://github.com/TimMacy/Markdown2PDF/blob/main/LICENSE"><img align="right" src="https://img.shields.io/badge/License-AGPL--3.0-blue.svg" alt="GNU Affero General Public License v3.0"></a><a href="#"><img align="right" src="https://img.shields.io/badge/Status-Discontinued-darkred.svg" alt="Markdown2PDF Status: Discontinued"></a>

This Python script converts Markdown (`.md`) files into PDF documents and was originally developed to help convert ChatGPT's Deep Research to PDF. Due to changes by OpenAI, this functionality is now natively supported, but they also removed the hyperlinks for the sources when copying the content. Therefore, this project is discontinued. For testing purposes, a demo Markdown file from before these changes were introduced is included in this repository. However, the script remains fully functional as a general Markdown-to-PDF converter. It can be used via the command line to convert individual Markdown files or in batches. Additionally, an app version quickly converts clipboard content to a PDF.

<p align="center">
  <img width="49.5%" alt="Markdown2PDF Example PDF Page 1" title="Markdown2PDF Example PDF Page 1" src="https://github.com/user-attachments/assets/6f560ace-e514-4074-89a5-3578e3a85a05" /><img width="1%" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" /><img width="49.5%" alt="Markdown2PDF Example PDF Page 2" title="Markdown2PDF Example PDF Page 2" src="https://github.com/user-attachments/assets/6c653e88-2d14-4016-a9d9-ad247fc914d7" />
</p>

> [!NOTE]
> Images are written as `([image]())` in the Markdown and thus cannot directly be included in the PDF. An empty space is added instead, allowing images to be pasted in effortlessly using a PDF editor.

<br>

## 🛠 Prerequisites (Command-line version)
Before running the script, ensure these are installed:

- **Python ≥ 3.9**
  - macOS: pre-installed
  - Linux: `sudo apt install python3`
  - Windows: [Download from python.org](https://python.org)
- **Pandoc**
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc`
  - Windows: `choco install pandoc`
- **XeLaTeX** (part of any full LaTeX distribution)
  - macOS: `brew install --cask mactex-no-gui`
  - Linux: `sudo apt install texlive-xetex`
  - Windows: [Download MiKTeX](https://miktex.org/download)

## 🚀 How to run Markdown2PDF (Command-line version)
### 📂 Batch Conversion (multiple files)
Navigate in the terminal to the folder containing the `.md` files, then run: `python3 /path/to/Markdown2PDF.py *.md`. The PDFs will be created in the same folder as the Markdown files.

### 📄 Single-file Conversion
To convert a single Markdown file into a PDF with a custom filename, run: `python3 /path/to/Markdown2PDF.py /path/to/file.md -o output.pdf`. Replace `file.md` and `output.pdf` with the actual filenames.

> [!TIP]
> Running `python3 /path/to/Markdown2PDF.py` with zero arguments uses the clipboard for input, and the 'Save As . . .' dialog appears to save the PDF.

## 📎 How to Use the App Version (Clipboard-to-PDF)
An app version is also available for macOS, Windows, and Linux:

1. **Download the app** for the required operating system from the [GitHub Releases](https://github.com/TimMacy/Markdown2PDF/releases) page.
2. **Copy the Markdown text** to the clipboard.
3. **Double-click the app file**, and the 'Save As . . .' dialog appears.
4. **Choose a save location**, adjust a file name if needed, and confirm.

No command line or setup required!

> [!IMPORTANT]
> When launching **Markdown2PDF** for the first time on macOS, Gatekeeper will block it until approved:
> 1. Open **System Settings → Privacy & Security** and scroll to the **Security** section at the bottom.
> 2. Then under **"Markdown2PDF.app was blocked to protect your Mac"**, click **Open Anyway**.
> 3. In the next **'Open "Markdown2PDF.app"?'** dialog window, click **Open** and authenticate if prompted.

<br>

## 📜 Changelog
- **17**: initial public release

<br>

## ⚖️ License
This project is licensed under the AGPL-3.0 License. See the [LICENSE](https://github.com/TimMacy/Markdown2PDF/blob/main/LICENSE) file for details.

<br>

## ⚠️ Disclaimer
Markdown2PDF is an independent, private project. It's not affiliated with, endorsed by, sponsored by, or officially connected to OpenAI. All trademarks are property of their respective owners.
