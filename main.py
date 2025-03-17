from utils.nifty_novel import get_novel_info, get_chapter_content
import os

# 从用户输入获取URL
url = input("请输入小说URL: ")

# 示例用法
novel_info = get_novel_info(url)
if novel_info:
    base_url = "https://new.nifty.org"
    novel_name = novel_info["novel_name"]
    novel_author = novel_info["novel_author"]
    novel_date = novel_info["novel_date"]
    novel_update = novel_info["novel_update"]
    chapters = novel_info["chapters"]

    # 构建文件路径
    file_path = os.path.join("downloads", f"{novel_name}.html")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 写入小说信息和章节内容到HTML文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"<h1>{novel_name}</h1>\n")
        file.write(f"<h2>作者: {novel_author}</h2>\n")
        file.write(f"<p>发表日期: {novel_date}</p>\n")
        file.write(f"<p>更新日期: {novel_update}</p>\n")
        file.write("<h3>章节内容:</h3>\n")

        for chapter in chapters:
            content = get_chapter_content(base_url, chapter)
            file.write(f"<div>{content}</div>\n")
            file.write("<hr>\n")

    print(f"小说已保存到: {file_path}")
