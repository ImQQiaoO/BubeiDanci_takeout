# BubeiDanci_takeout 使用说明

**BubeiDanci_takeout** 是一个工具，用于帮助你导出“不背单词”App中的**生词本**数据。按照以下步骤，你就可以轻松导出你的**生词本**！

### 使用步骤

1. 点击当前界面右侧 `Releases`，选择合适的版本下载。
2. 打开浏览器，登录“不背单词”官网，进入“**生词本**”页面：[不背单词 - 生词本](https://www.bbdc.cn/newword)
3. 按下 `F12` 键，打开开发者工具（如果你使用的是 Chrome 或 Edge，快捷键直接生效）。
4. 在开发者工具的顶部，点击 `Network`（网络）标签页。
5. 刷新页面（按 `F5`），然后在弹出的请求列表中找到名称为 `newword` 的请求。
6. 点击该请求，在右侧的详细信息中，找到 `Cookie` 字段，复制其内容（内容可能较长）。
7. 解压下载好的安装包，双击以 `.exe` 结尾的文件，按照提示输入刚才复制的 `Cookie` 字段即可。

### 构建方法

> 如果选择了从 `Releases` 处下载该软件，则不必关心下面从源代码构建项目的操作。

1. 克隆 **BubeiDanci_takeout** 项目的代码，或直接下载项目中 `src` 下的全部文件。

   > 运行该工具需要 Python 环境。如果尚未安装 Python，请从 [Python官网](https://www.python.org/downloads/) 下载并安装。
   >
2. 在项目根目录下打开终端，输入以下命令安装依赖并运行工具：

   ```bash
   pip install -r requirements.txt  # 安装所需的依赖库
   python main.py                   # 运行工具
   ```
3. 在工具开始运行后，提示输入 `Cookie`。将你刚才复制的 `Cookie` 粘贴到该位置。
4. 提交后，工具会自动解析你的 `Cookie` 并开始导出你的生词本数据。

### 完成

导出完成后，你就可以得到你“不背单词”中的**生词本**数据啦！轻松查看你的学习进度吧。

如果您对本项目有任何问题，请查看项目中的文档或在GitHub提交[issue](https://github.com/ImQQiaoO/BubeiDanci_takeout/issues)反馈。

如果您觉得好用，请在本项目的右上角为我点亮Star，这是您对我最大的支持与鼓励。

### 声明

> [!IMPORTANT]
> 中文翻译并非导出自不背单词，而是使用 [ECDICT](https://github.com/skywind3000/ECDICT-ultimate) 的数据，无法做到与不背单词一致。

---
#### 其他
> 通过 [Releases](https://github.com/ImQQiaoO/BubeiDanci_takeout/releases) 下载的可执行文件可能会被 Windows Defender 等杀毒软件误报。这是因为本项目使用 PyInstaller 将源代码打包成二进制文件进行分发，某些杀毒软件可能将未签名的可执行文件误认为潜在威胁。如果您不信任从 Releases 下载的二进制文件，您可以选择直接从源代码进行构建。我们提供了详细的[构建指南](#构建方法)，您可以通过源代码并按照说明进行构建，从而获得更高的安全性和信任度。