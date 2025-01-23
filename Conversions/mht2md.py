# MHT to Markdown Converter
import email
import os
import re
import subprocess
from email import policy
from PIL import Image
from bs4 import BeautifulSoup
from Conversions.ConversionBase import FileConverter

# MHT to Markdown Converter
class MHTToMarkdownConverter(FileConverter):
    def convert(self, progress_callback):
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_dir = os.path.join(self.output_dir, base_name)
        output_images_dir = os.path.join(output_dir, "img")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(output_images_dir, exist_ok=True)
        convert_to_png = True
        with open(self.file_path, 'rb') as f:
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

        progress_callback(100)
        return f"Markdown文件已生成到: {md_file_path}"
        # Open the file explorer at the output directory
        self.open_file_explorer(output_dir)

    def open_file_explorer(self,directory):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(directory)
            elif os.name == 'posix':
                if 'darwin' in os.sys.platform:  # macOS
                    subprocess.run(['open', directory])
                else:  # Assume Linux
                    subprocess.run(['xdg-open', directory])
        except Exception as e:
            print(f"Could not open file explorer: {e}")

