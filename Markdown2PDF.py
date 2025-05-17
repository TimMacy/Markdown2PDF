import sys
import os
import re
import time
import shutil
import tempfile
import argparse
import subprocess

"""
************************************************************************
*                                                                      *
*                    Copyright © 2025 Tim Macy                         *
*                    GNU Affero General Public License v3.0            *
*                    Version: 17.0 - Markdown2PDF                      *
*                    All Rights Reserved.                              *
*                                                                      *
*             Visit: https://github.com/TimMacy                        *
*                                                                      *
************************************************************************
"""

# function to process ([Name](URL)) citations -> [^N]
def process_markdown_link_citations(markdown_content):
    citation_pattern = r'\(\[([^\]]+)\]\((.*?)\)\)'
    citations_found = {}
    next_index = 1
    matches = list(re.finditer(citation_pattern, markdown_content))
    processed_content_list = list(markdown_content)

    match_data = []
    for match in matches:
        original_markdown = match.group(0)
        source_name = match.group(1).strip()
        url = match.group(2).strip()
        start, end = match.span()

        # assign index based on unique original_markdown
        if original_markdown not in citations_found:
            current_index = next_index
            citations_found[original_markdown] = {'index': current_index, 'name': source_name, 'url': url}
            next_index += 1
        else:
            current_index = citations_found[original_markdown]['index']

        footnote_marker = f'[^{current_index}]'

        # space removal logic
        effective_start = start
        if start > 0 and markdown_content[start - 1].isspace():
            if start > 1 and markdown_content[start - 2].isalnum():
                effective_start = start - 1

        match_data.append({
            'effective_start': effective_start,
            'end': end,
            'marker': footnote_marker
        })

    match_data.sort(key=lambda r: r['effective_start'], reverse=True)
    for r in match_data:
        processed_content_list[r['effective_start']:r['end']] = list(r['marker'])

    final_processed_content = "".join(processed_content_list)

    # get the unique citation data, now sorted by their assigned index
    citation_data_list = sorted(list(citations_found.values()), key=lambda c: c['index'])
    return final_processed_content, citation_data_list


# function to generate definitions for [^N] markers
def generate_pandoc_footnote_definitions(citations):
    if not citations: return ""
    definitions_md = "\n\n"
    for citation in citations:
        safe_url = citation['url'].replace(' ', '%20')
        definitions_md += f"[^{citation['index']}]: [{citation['name']}]({safe_url})\n"
    return definitions_md

# main conversion function
def convert_markdown_to_pdf_pandoc(markdown_file, output_pdf):
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{markdown_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # image replacement
    image_pattern = r'\(\[image\]\(\)\)'
    markdown_content = re.sub(
        image_pattern,
        r'\\vspace{250pt}',
        markdown_content
    )

    # title stripping
    first_title_match = re.search(r'^# .*', markdown_content, re.MULTILINE)
    if first_title_match:
        markdown_content = markdown_content[first_title_match.start():]
    else:
        print("Warning: No H1 title found at the start of the content.")

    # combine content and definitions
    processed_content, citations = process_markdown_link_citations(markdown_content)
    footnote_definitions_md = generate_pandoc_footnote_definitions(citations)
    final_markdown_content = processed_content + footnote_definitions_md

    # Pandoc conversion
    temp_md_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md', encoding='utf-8') as temp_md:
            temp_md.write(final_markdown_content)
            temp_md_path = temp_md.name

        # LaTeX config
        header_inject = r'''
        \usepackage{etoolbox}
        \usepackage{enotez}
        \usepackage{hyperref}
        \hyphenpenalty=10000
        \exhyphenpenalty=100
        \hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}
        \setenotez{
        list-heading = {},
        backref=true
        }
        \AtBeginDocument{\let\footnote\endnote}
        '''

        after_inject = r'''
        \newpage
        \begingroup
        \parindent 0pt
        \parskip 6pt plus 2pt minus 2pt
        \normalsize
        \section*{References}
        {\leftskip=1em
        \printendnotes
        }
        \endgroup
        ''' if citations else ''

        # Pandoc command
        pandoc_command = [
            'pandoc',
            temp_md_path,
            '--from', 'markdown+footnotes',
            '-o', output_pdf,
            '--pdf-engine=xelatex',
            '-V', 'geometry:left=2cm,right=2cm,top=2cm,bottom=2cm',
            '-V', 'fontsize=12pt',
            '-V', 'mainfont=Helvetica',
            f'-V', f'header-includes={header_inject}',
        ]
        if citations:
            pandoc_command.extend(['-V', f'include-after={after_inject}'])

        # execute Pandoc
        subprocess.run(pandoc_command, check=True)

    # error handling
    except FileNotFoundError:
        print("Error: 'pandoc' command not found.")
        if temp_md_path: print(f"Intermediate markdown kept at: {temp_md_path}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\nError during Pandoc execution (return code {e.returncode})")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected Python error occurred: {e}")
        sys.exit(1)
    finally:
        if temp_md_path and os.path.exists(temp_md_path):
            os.remove(temp_md_path)

# default-name helper, use first H1
def _suggested_pdf_name(md: str) -> str:
    m = re.search(r'^#\s*(.+)', md, re.MULTILINE)
    if m:
        title = m.group(1).strip()
        title = re.sub(r'[\/\\\?\%\*\:\|"<>\n\r]+', '', title)
        title = title.strip()
        if not title:
            title = time.strftime("%Y-%m-%d_%H-%M-%S")
    else:
        title = time.strftime("%Y-%m-%d_%H-%M-%S")

    max_len = 100
    if len(title) > max_len:
        title = title[:max_len].rstrip()

    return f"{title}.pdf"

# clipboard
def get_clipboard_markdown() -> str:
    # macOS
    if sys.platform == "darwin":
        cmd = ["pbpaste"]
    # linux
    elif sys.platform.startswith("linux"):
        if shutil.which("xclip"):
            cmd = ["xclip", "-selection", "clipboard", "-o"]
        elif shutil.which("xsel"):
            cmd = ["xsel", "-b", "-o"]
        else:
            sys.exit("Need xclip or xsel to read the clipboard on Linux.")
    # windows
    elif sys.platform.startswith("win"):
        cmd = ["powershell", "-NoProfile", "-Command", "Get-Clipboard"]
    else:
        sys.exit("Unsupported OS.")

    try:
        md = subprocess.check_output(cmd).decode("utf-8")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Failed to read clipboard: {e}")
    if not md.strip():
        sys.exit("Clipboard is empty - copy some Markdown first.")
    return md

# "Save As . . ." dialog
def ask_save_path(md_text: str) -> str:
    default_name = _suggested_pdf_name(md_text)

    # macOS (osascript)
    if sys.platform == "darwin":
        script = f'''
            set f to choose file name with prompt "Save PDF as:" \
                     default name "{default_name}"
            POSIX path of f
        '''
        try:
            path = subprocess.check_output(["osascript", "-e", script]).decode().strip()
        except subprocess.CalledProcessError:
            sys.exit("Cancelled.")
    # linux (zenity/kdialog)
    elif sys.platform.startswith("linux"):
        if shutil.which("zenity"):
            try:
                path = subprocess.check_output([
                    "zenity", "--file-selection", "--save", "--confirm-overwrite",
                    "--filename", default_name]).decode().strip()
            except subprocess.CalledProcessError:
                sys.exit("Cancelled.")
        elif shutil.which("kdialog"):
            try:
                path = subprocess.check_output([
                    "kdialog", "--getsavefilename", os.getcwd(), "*.pdf",
                    "Save PDF as"]).decode().strip()
            except subprocess.CalledProcessError:
                sys.exit("Cancelled.")
        else:
            # Fallback: plain CLI prompt
            path = input(f"Save PDF as [{default_name}]: ").strip() or default_name
    # windows (PowerShell dialog)
    elif sys.platform.startswith("win"):
        ps = f"""
        Add-Type -AssemblyName System.Windows.Forms
        $dlg = New-Object System.Windows.Forms.SaveFileDialog
        $dlg.Filter = "PDF files (*.pdf)|*.pdf"
        $dlg.FileName = "{default_name}"
        if($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){{ $dlg.FileName }}
        """
        try:
            path = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps]).decode().strip()
        except subprocess.CalledProcessError:
            sys.exit("Cancelled.")
    else:
        sys.exit("Unsupported OS.")

    if not path.lower().endswith(".pdf"):
        path += ".pdf"
    return path

# main function
def main():
    # clipboard version
    if len(sys.argv) == 1:
        md_text  = get_clipboard_markdown()
        pdf_path = ask_save_path(md_text)
        with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.md', encoding='utf-8') as tmp:
            tmp.write(md_text)
            tmp_path = tmp.name
        try:
            convert_markdown_to_pdf_pandoc(tmp_path, pdf_path)
        finally:
            os.remove(tmp_path)
        return

    # Command-line version
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument('input_files', nargs='+', help='One or more Markdown files')
    parser.add_argument('-o', '--output', help='Output PDF file (only for single input)')
    args = parser.parse_args()
    for md in args.input_files:
        out = args.output if len(args.input_files)==1 and args.output else os.path.splitext(md)[0] + '.pdf'
        convert_markdown_to_pdf_pandoc(md, out)
if __name__ == "__main__":
    main()
