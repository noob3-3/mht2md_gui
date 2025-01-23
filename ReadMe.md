# mht2md_gui

[English](README_EN.md)

## 项目来自于 
[githubJonesckevin/mht2md ](https://github.com/Jonesckevin/mht2md)

## 修改内容
1. 将Markdown的格式修改，将图片存储到Markdown的下一级目录下，目录结构更清晰
2. 添加GUI 界面，添加actions自动编译win和linux下可执行工具，方便没有python解释器的人群使用
3. 支持Excel转Markdown

## 项目使用方式
### 直接下载Releases 

### 自己编译
1. 克隆代码

`git clone https://github.com/noob3-3/mht2md_gui`

2. 切换目录

`cd mht2md_gui`

3. 安装依赖

`pip install -r requirements.txt`

4. 编译可执行文件

`pyinstaller --onefile --windowed mht2MarkdownGui.py`

### 打开软件，选择MHT文件，进度条结束，查看MHT同目录下的同名文件夹，开始编辑Markdown 

## todo
1. [x] Excel    转 Markdown
2. [ ] pdf      转 Markdown

3. [ ] Markdown 转 pdf
4. [ ] Markdown 转 Excel
5. [ ] Markdown 转 html

