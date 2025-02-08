# BubeiDanci_takeout 使用说明

BubeiDanci_takeout 是一个工具，用于帮助你导出“不背单词”App中的生词本数据。按照以下步骤，你就可以轻松导出你的生词本！

## 使用步骤

### 1. 获取 Cookie

1. 打开浏览器，登录“不背单词”官网，进入“生词本”页面：[不背单词 - 生词本](https://www.bbdc.cn/newword)
   
2. 按下 **F12** 键，打开开发者工具（如果你使用的是 Chrome 或 Edge，快捷键直接生效）。

3. 在开发者工具的顶部，点击 **Network**（网络）标签页。

4. 刷新页面（按 **F5**），然后在左侧的请求列表中找到任意一个请求（任意一行都可以）。

5. 点击该请求，在右侧的详细信息中，找到 **Cookie** 字段，复制其内容（内容可能较长）。

### 2. 配置工具

1. 克隆 **BubeiDanci_takeout** 项目的代码，或直接下载项目中的 `main.py` 文件。

   > 运行该工具需要 Python 环境。如果尚未安装 Python，请从 [Python官网](https://www.python.org/downloads/) 下载并安装。

2. 在项目根目录下打开终端，输入以下命令安装依赖并运行工具：

   ```bash
   pip install requests  # 安装所需的requests库
   python main.py        # 运行工具
   ```


3. 在工具开始运行后，提示输入 Cookie。将你刚才复制的 Cookie 粘贴到该位置。

4. 提交后，工具会自动解析你的 Cookie 并开始导出你的生词本数据。

### 完成

导出完成后，你就可以得到你“不背单词”中的生词本数据啦！轻松查看你的学习进度吧。

如果有任何问题，请查看项目中的文档或在GitHub提交issue反馈。