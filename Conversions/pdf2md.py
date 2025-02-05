import os
import pdfplumber

from Conversions.ConversionBase import FileConverter


class PdfToMarkdownConverter(FileConverter):
    def convert(self, progress_callback):
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_dir = os.path.join(self.output_dir, base_name)
        os.makedirs(output_dir, exist_ok=True)

        with pdfplumber.open(self.file_path) as pdf:
            total_pages = len(pdf.pages)

            for index, page in enumerate(pdf.pages):
                # Extract text with layout analysis
                text_content = self.extract_text_with_layout(page)

                markdown_content = f"# Page {index + 1}\n\n"
                markdown_content += text_content

                md_file_path = os.path.join(output_dir, f'page_{index + 1}.md')
                with open(md_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)

                progress_callback((index + 1) / total_pages * 100)

        return f"PDF文件已转换为Markdown，保存到: {output_dir}"

    def extract_text_with_layout(self, page):
        """Extract text from a PDF page with basic layout preservation."""
        lines = []
        for line in page.extract_text(layout=True).split('\n'):
            if line.strip():
                lines.append(line.strip())

        # Join the lines while keeping paragraph breaks
        text_content = '\n\n'.join(lines)
        return text_content
