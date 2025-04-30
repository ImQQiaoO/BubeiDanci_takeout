# BubeiDanci_takeout 使用说明

**BubeiDanci_takeout** 是一个工具，用于帮助你导出“不背单词”App中的**生词本**数据。按照以下步骤，你就可以轻松导出你的**生词本**！

> [!WARNING]
> 由于闲鱼用户[switch玩家](https://m.tb.cn/h.6m1xhb3?tk=qWGpVVxrRaW)盗卖此软件的运行结果，并没有注明软件来源，自[v0.4.4](https://github.com/ImQQiaoO/BubeiDanci_takeout/releases/tag/v0.4.4)版本后，此项目不再分发二进制文件，直至没有人再对此软件进行盗卖活动为止。
> 
> 开源软件维护不易，我在此奉劝，少干那些拾人牙慧的腌臜之事！好自为之！

### 使用步骤

1. 点击当前界面右侧 `Releases`，选择合适的版本下载（请下载以**BBDCTakeOut**开头的压缩包）。
2. 打开浏览器，登录“不背单词”官网，进入“**生词本**”页面：[不背单词 - 生词本](https://www.bbdc.cn/newword)
3. 按下 `F12` 键，打开开发者工具（如果你使用的是 Chrome 或 Edge，快捷键直接生效）。
4. 在开发者工具的顶部，点击 `Network`（网络）标签页。
5. 刷新页面（按 `F5`），然后在弹出的请求列表中找到名称为 `newword` 的请求。
6. 点击该请求，在右侧的详细信息中，找到 `Cookie` 字段，复制其内容（内容可能较长）。
   
   以上步骤请参考下图。
   ![如何获取cookie](/README_imgs/how_to_get_cookie.png)
7. **解压**下载好的安装包，双击以 `.exe` 结尾的文件，按照提示输入刚才复制的 `Cookie` 字段即可。


### 完成

导出完成后，你就可以得到你“不背单词”中的**生词本**数据啦！轻松查看你的学习进度吧。

如果您对本项目有任何问题，请查看项目中的文档或在GitHub提交[issue](https://github.com/ImQQiaoO/BubeiDanci_takeout/issues)反馈。

如果您觉得好用，请在本项目的右上角为我点亮Star，这是您对我最大的支持与鼓励。

### 功能预览
1. 导出至PDF:
   ![pdf_preview](/README_imgs/pdf_preview.png)

2. 导出至PDF时的紧凑模式：
   ![compact_mode](/README_imgs/compact_mode.png)

2. 导出至PDF时的默写模式：
   
   默写释义：
   ![dictation_ch](/README_imgs/dictation_ch.png)

   默写单词：
   ![dictation_en](/README_imgs/dictation_en.png)

   > 紧凑模式下不支持默写。

### 声明

> [!IMPORTANT]
> 中文翻译并非导出自不背单词，而是使用 [ECDICT](https://github.com/skywind3000/ECDICT-ultimate) 的数据，无法做到与不背单词一致。

---
#### 其他
> 通过 [Releases](https://github.com/ImQQiaoO/BubeiDanci_takeout/releases) 下载的可执行文件可能会被 Windows Defender 等杀毒软件误报。这是因为本项目使用 PyInstaller 将源代码打包成二进制文件进行分发，某些杀毒软件可能将未签名的可执行文件误认为潜在威胁。如果您不信任从 Releases 下载的二进制文件，您可以选择直接从源代码进行构建。