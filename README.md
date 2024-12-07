# pdf-cut-white

在使用 Latex 书写论文时（或者其他时刻），花费了不少的时间处理 PDF 图表——`裁剪不必要的图表白边`。所幸就写个工具自动完成吧——自动化且精准。

While latex, it takes time to `cut the useless white part of pdf`, so here comes a tool for it.

---

**这个文档已经够短了，请务必读一遍先。**

> Please see [here](#mention) for english README.

# 提示
请重新安装依赖，以确保更新内容一致，`pip3 install -r requirements.txt`.

# 特性
工具可以对生成的 PDF 图表进行自动裁剪，减少人工操作和其他软件依赖（如`Acrobat`）。

# 使用

请安装python3.8及以上版本，详见[Install](#install)。

推荐使用命令行版本，详见[CLI](#cli)。

CLI 流程说明：
- 读取原始 PDF 文件中的每一页（实际上只会处理第一页，这里默认每个pdf是一个单页图表）
- 按页识别 PDF 中的白边（基于 pdf item 分析）
- 裁剪白边（本质上是通过缩减 media box 实现）
- 输入无白边的新 PDF 文件

若希望使用 GUI 版本，请确保能够成功安装 PySide6，详见[GUI](#gui)。

GUI 流程说明：
- 启用工具，选择输入文件夹和输出文件夹（必须使用不同的文件夹防止源文件覆盖）
- 扫描 pdf 文件（GUI 支持在列表中二次选择 PDF）（注意：仅会扫描一级目录，而不会扫描子目录）
- 确认无误后，点击完成 PDF 裁剪（仅选中的文件），并输出到输出文件夹下

## 注意事项
部分 pdf 输出会在最外围加上 RT 元素，导致无法裁剪，这时候可以添加`--ignore 1`参数，再做尝试。

请优先不带`ignore`尝试，有问题再带参数，人工检查一遍即可，这种情况也相对有有限（取决于绘图工具）。

> 发现任何问题，请参看`issue`，若仍无法解决，请提新`issue`（请`--verbose`执行附带 log）（若可以，请提交对应的 case.pdf）。

# 其他

已知部分限制：

- 只扫描一级目录，不支持递归。
  - 可以有效防止错误操作而产生大量的文件 IO。
  - 工具已实现自动化，以一级目录为单位也足够使用。
  - 同理，禁止对同目录/同文件进行操作。
- 对于原始 PDF 文件可以妥善完成裁剪，但如果是其他工具编辑（特别是裁剪）过的 PDF，再次裁剪则可能输出错误。
  - 因为该工具通过修正 PDF 中的 media box 实现裁剪，可能与其他工具不兼容。
- 偶尔会出现裁剪过度精细的情况，待修正。
  - 本质上，白边就是无内容的部分，因此工具会统计所有有含义的部分（如 textbox，image 等），并计算最大的有效坐标范围，这一范围以外的部分即视为白边。
- 有部分元素未处理
  - 可以参看`pdf_white_cut/worker.py::extract_pdf_boxs`，部分元素使用了原始的 bbox，可能导致结果保留的内容（白边）过多，对此请 issue 反馈，并附带用例和 log。


# Mention

Please redo `pip3 install -r requirements.txt` since dependencies changed (see [changelog](#Changelog) ).

# Feature

Automatic cut the useless white part of pdf. This pdf must be a single page of table or figure.

# Usage

## Install

- install `python3` (python 3.8 or above)
- install dependency: `pip3 install -r requirements.txt` or `pip3 install -r requirements.txt --user`

## CLI

Recommend to use `CLI (command line tool)`:

```sh
# cut single pdf
python cli.py -i in.pdf -o out.pdf

# cut all pdf files under a folder
python cli.py -id infolder -od outfolder
```

> MENTION: sometimes add `--ignore 1` if output is not the wanted.

## GUI

Make sure you **REALLY** require `GUI`:

```sh
# install PySide6, the official Qt for Python : )
pip install PySide6==6.3.2

# if success, run 
python gui.py
```


# Misc

## Limitation

Known limitation:

- Only scan one level folder
- Some pdf with edit may cause failure (TODO: it is it is `NotImplemented` logic)
- Support single page pdf, but may not support well for multiple pages (try it first)
- Some cases with too many white part may cause failure (TODO: it is `NotImplemented` logic)
  - see `pdf_white_cut/worker.py::extract_pdf_boxs`

## Changelog

- (bugfix & feat) support rotated pdf pages.
- (refactor) less files, less function defines.
- (dependency) bump to PySide6 for GUI with QT.
- (dependency) use `pdfminer.six` (a community fork) (since `pdfminer` is **not actively maintained**).
- (bugfix) missing `LTFigure` analysis.
- (bugfix) path process error in batch_cut_pdf.
- (bugfix) missing `LTTextBox` or `LTTextLine` analysis.
- (feature) GUI base on PySide2 (the official).
- (bugfix) failed for pdf which has been edited before - not fix the pos for the edited (pdfminer use relative pos).
- (feature) CLI using argparse.

## Dependency

- PyMuPDF: it is fitz which do well in pdf IO
- pypdf: a pure python module for pdf (upgrade of PyPDF2)
- pdfminer.six: scan pdf elements
- PySide6: optional for GUI only
- loguru: for log only
