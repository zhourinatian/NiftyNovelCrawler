from utils.nifty_novel import get_novel_info, get_chapter_content
import os, re
from bs4 import BeautifulSoup

# 让用户选择保存格式
print("请选择本次需要保存的格式：")
print("1. TXT (default)")
print("2. HTML")
save_format = input("输入选项（1或2）： ").strip()

# 如果用户输入无效选项，默认保存为TXT
if save_format not in ["1", "2"]:
    save_format = "1"

while True:
    # 从用户输入获取URL
    url = input("请输入小说网址 ( 输入 q 或 exit 退出）： ").strip()
    if url.lower() in ['q', 'exit']:
        break

    # 示例用法
    novel_info = get_novel_info(url)
    if novel_info:
        base_url = "https://new.nifty.org"
        novel_name = novel_info["novel_name"]
        novel_author = novel_info["novel_author"]
        novel_date = novel_info["novel_date"]
        novel_update = novel_info["novel_update"]
        chapters = novel_info["chapters"]

        # 替换文件名中的非法字符
        novel_name = re.sub(r'[<>:"/\\|?*]', '_', novel_name)

        # 构建文件路径
        file_extension = "html" if save_format == "2" else "txt"
        file_path = os.path.join("downloads", f"{novel_name}.{file_extension}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 写入章节内容到文件
        with open(file_path, "w", encoding="utf-8") as file:
            for chapter in chapters:
                content = get_chapter_content(base_url, chapter)
                if save_format == "2":
                    file.write(f"<div>{content}</div>\n")
                    file.write("<hr>\n")
                else:
                    soup = BeautifulSoup(content, 'html.parser')
                    text_content = soup.get_text()
                    file.write(f"{text_content}\n")
                    file.write("="*50 + "\n")

        print(f"Novel saved to: {file_path}")