import markdown
from pathlib import Path


markdown_file_path = Path('info.md').absolute()
markdown_content = markdown_file_path.read_text(encoding='utf-8')
html_content = markdown.markdown(markdown_content)
html_file_path = Path('ProjectFiles/info.html')
html_file_path.write_text(html_content, encoding='utf-8')
