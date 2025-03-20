import os, re, requests
from bs4 import BeautifulSoup

def get_novel_info(url):
    print(f"Fetching novel information: {url}")
    # 去掉协议部分
    url_path = url.replace("https://", "").replace("http://", "")
    # 构建文件路径
    file_path = os.path.join("cache", *url_path.split("/")) + ".html"
    
    # 检查缓存文件是否存在
    if os.path.exists(file_path):
        print(f"Reading novel information from cache: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        print(f"Fetching novel information from the web: {url}")
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            data = response.text
            # 保存到缓存文件
            save_to_cache(url, data)
        else:
            print(f"Request failed, status code: {response.status_code}")
            return None
    
    soup = BeautifulSoup(data, 'html.parser')
    
    # 获取小说名称
    novel_name_element = soup.select_one('html > body > main > div > div > header > div > div > h1')
    if not novel_name_element:
        novel_name_element = soup.select_one('html > body > main > div > div > div:nth-of-type(1) > header > div > div > h1')
    if novel_name_element:
        novel_name = novel_name_element.text
    else:
        print("Novel name not found")
        return None
    print(f"Novel name: {novel_name}")
    
    # 获取小说作者
    novel_author_element = soup.select_one('html > body > main > div > div > header > div > div > h2 > a > div > span > strong')
    if not novel_author_element:
        novel_author_element = soup.select_one('html > body > main > div > div > div:nth-of-type(1) > header > div > div > h2 > a > div > span > strong')
    novel_author = novel_author_element.text if novel_author_element else "Unknown author"
    print(f"Novel author: {novel_author}")
    
    # 获取发表日期
    novel_date_element = soup.select_one('html > body > main > div > div > header > div > div > p:nth-of-type(1) > span')
    if not novel_date_element:
        novel_date_element = soup.select_one('html > body > main > div > div > div:nth-of-type(1) > header > div > div > p > span')
    novel_date = novel_date_element.text if novel_date_element else "Unknown date"
    print(f"Publication date: {novel_date}")
    
    # 获取更新日期
    novel_update_element = soup.select_one('html > body > main > div > div > header > div > div > p:nth-of-type(2) > span')
    novel_update = novel_update_element.text if novel_update_element else "No update date"
    print(f"Update date: {novel_update}")
    
    # 获取章节列表
    chapters_elements = soup.select('html > body > main > div > div > section > ol > li > a')
    if chapters_elements:
        chapters = [chapter['href'] for chapter in chapters_elements]
        print(f"Chapters list: {chapters}")
    else:
        # 如果没有章节列表，则将当前页面作为唯一章节
        chapters = [url]
        print("No chapters list")
    
    return {
        "novel_name": novel_name,
        "novel_author": novel_author,
        "novel_date": novel_date,
        "novel_update": novel_update,
        "chapters": chapters
    }

def save_to_cache(url, data):
    # 去掉协议部分
    url_path = url.replace("https://", "").replace("http://", "")
    # 构建文件路径
    file_path = os.path.join("cache", *url_path.split("/"))
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # 保存文件
    with open(file_path + ".html", "w", encoding="utf-8") as file:
        file.write(data)
    print(f"Saved to cache: {file_path}.html")

def get_chapter_content(base_url, chapter_path):
    # 去掉协议部分
    chapter_path_clean = chapter_path.replace("https://", "").replace("http://", "")
    # 构建文件路径
    file_path = os.path.join("cache", *chapter_path_clean.split("/")) + ".html"
    
    # 检查缓存文件是否存在
    if os.path.exists(file_path):
        print(f"Reading chapter content from cache: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        chapter_url = base_url + chapter_path
        print(f"Fetching chapter content from the web: {chapter_url}")
        response = requests.get(chapter_url)
        if response.status_code == 200:
            data = response.text
            # 保存到缓存文件
            save_to_cache(chapter_url, data)
        else:
            print(f"Request for chapter failed, status code: {response.status_code}")
            return None
    
    soup = BeautifulSoup(data, 'html.parser')
    # 获取章节内容并保留<p>标签
    chapter_content_element = soup.select_one('html > body > main > div > div > div:nth-of-type(1) > article')
    chapter_content = str(chapter_content_element) if chapter_content_element else "<p>No chapter content</p>"
    
    # 替换所有的反引号为单引号
    chapter_content = chapter_content.replace("`", "'")

    return chapter_content