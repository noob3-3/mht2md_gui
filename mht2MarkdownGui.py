import os
import email
import re
from email import policy
from bs4 import BeautifulSoup
from PIL import Image
from tkinter import Tk, Button, filedialog, messagebox, Label
from tkinter.ttk import Progressbar, Style

__author__ = "Kevin C. Jones"
__email__ = "jonesckevin@proton.me"
__site__ = "https://github.com/jonesckevin/mht2md.git"

convert_to_png = True


def extract_images_and_convert_to_md(mht_file, convert_to_png, progress_callback):
    base_name = os.path.splitext(os.path.basename(mht_file))[0]
    output_dir = os.path.join(os.path.dirname(mht_file), base_name)
    output_images_dir = os.path.join(output_dir, "img")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_images_dir, exist_ok=True)

    with open(mht_file, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    html_part = next((part.get_payload(decode=True).decode(part.get_content_charset())
                      for part in msg.walk() if part.get_content_type() == 'text/html'), None)
    if not html_part:
        raise ValueError("在MHT文件中没有找到HTML部分")

    soup = BeautifulSoup(html_part, 'html.parser')
    image_paths = {}

    parts = list(msg.walk())
    total_parts = len(parts)

    for index, part in enumerate(parts):
        if part.get_content_type().startswith('image/'):
            image_data = part.get_payload(decode=True)
            image_filename = os.path.basename(part.get('Content-Location'))
            image_path = os.path.join(output_images_dir, image_filename)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
            img_tag = soup.find('img', {'src': part.get('Content-Location')})
            if img_tag:
                img_tag['src'] = image_filename
                image_paths[part.get('Content-Location')] = image_filename

        progress_callback((index + 1) / total_parts * 50)  # Update progress to 50% after images

    steps_text = {}
    for text in soup.stripped_strings:
        match = re.match(r'^Step (\d+):', text)
        if match:
            step_number = int(match.group(1))
            steps_text[step_number] = steps_text.get(step_number, '') + ' ' + text.strip()

    markdown_content = '\n'.join(
        f"## Step {step_number}\n{step}\n### 执行:\n![Image](img/screenshot{step_number:04d}{'.png' if convert_to_png else '.JPEG'})\n"
        for step_number, step in sorted(steps_text.items()))

    md_file_path = os.path.join(output_dir, f'{base_name}.md')
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

    if convert_to_png:
        images = os.listdir(output_images_dir)
        total_images = len(images)
        for i, image_filename in enumerate(images):
            if image_filename.endswith('.JPEG'):
                jpeg_path = os.path.join(output_images_dir, image_filename)
                png_path = os.path.splitext(jpeg_path)[0] + '.png'
                with Image.open(jpeg_path) as img:
                    img.save(png_path, 'png')
                os.remove(jpeg_path)
            progress_callback(50 + (i + 1) / total_images * 50)  # Continue progress from 50% to 100%

    print(f"Markdown文件和图像已保存到 {output_images_dir}")


def select_and_process_file():
    file_path = filedialog.askopenfilename(filetypes=[("MHT files", "*.mht")])
    if file_path:
        try:
            progress_bar['value'] = 0
            root.update_idletasks()
            extract_images_and_convert_to_md(file_path, convert_to_png, update_progress)
            messagebox.showinfo("完成", f"Markdown和图像文件已生成：{file_path}")
        except Exception as e:
            messagebox.showerror("错误", str(e))


def update_progress(value):
    progress_bar['value'] = value
    root.update_idletasks()


if __name__ == "__main__":
    root = Tk()
    root.title("MHT to Markdown Converter")
    root.geometry("400x200")

    style = Style()
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TLabel", font=("Helvetica", 12))
    style.configure("TProgressbar", length=300, mode='determinate')

    label = Label(root, text="选择一个 MHT 文件进行转换")
    label.pack(pady=10)

    button = Button(root, text="选择MHT文件并转换", command=select_and_process_file)
    button.pack(pady=10)

    progress_bar = Progressbar(root, style="TProgressbar")
    progress_bar.pack(pady=20)

    root.mainloop()
