# NiftyNovelCrawler

#### 这个名为 NiftyNovelCrawler 的脚本从 New.Nifty.org 抓取小说信息和章节内容。它首先检查本地缓存，如果未找到，则从网络获取并保存到缓存中。它提取小说的名称、作者、出版日期、更新日期和章节列表，并将这些信息和内容保存到 HTML 文件中。

### 如果您觉得这个脚本有用，请考虑支持 Nifty 网站。

## 食用方法：

1. 确保系统内安装了 `python 3.11.x`
2. 拉取 `git clone` 该项目
3. 进入clone的文件夹 `cd NiftyNovelCrawler`
4. 新建一些文件夹 `mkdir .venv cache downloads`
3. 使用 `python -m venv ./venv/` 安装虚拟环境
4. 安装依赖 `pip install -r requirements.txt`
5. 运行 `python main.py`
