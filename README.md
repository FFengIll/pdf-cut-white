# pdf-cut-white

# Motivation

While latex, it takes time to `cut the useless white part of pdf`, then, here comes a tool for it.

在使用Latex书写论文时（或者其他时刻），花费了不少的时间处理PDF图表——`裁剪不必要的图表白边`。

所幸就写个工具自动完成吧——自动化且精准。

这个文档已经够短了，请务必读一遍先。

# Feature

Automatic cut the useless white part of pdf. This pdf must be a single page of table or figure.

工具可以对生成的PDF图表进行自动裁剪，减少人工操作和其他软件依赖（如`Acrobat`）。

其自动的工作流程为：

- 读取原始PDF文件
- 识别PDF中的白边
- 裁剪白边（缩减media box）
- 输入无白边PDF文件

# Usage

- Install `python3`
- Install dependency `pip3 install -r requirements.txt`

> may add `--user` for user mode

Recommend to use `CLI (command line tool)`:

- cut single pdf: `python cli.py -i in.pdf -o out.pdf`
- cut all pdf just bellow dir: `python cli.py -id infolder -od outfolder`

> MENTION: sometimes add `--ignore 1` if failed.

If you **REALLY** wanna use the `GUI`:

- install PySide2, the official Qt for Python : ), `pip install pyside2`
- if success, run `python gui.py`

推荐使用命令行版本（命令如上），若希望使用GUI版本，请确保能够成功安装PySide2（命令如上）：

- 启用工具，选择输入文件夹和输出文件夹（必须使用不同的文件夹防止源文件覆盖）
- 扫描pdf文件（GUI支持在列表中二次选择PDF）（注意：仅会扫描一级目录，而不会扫描子目录）
- 确认无误后，点击完成PDF裁剪（仅选中的文件），并输出到输出文件夹下

注意：部分pdf输出会在最外围加上RT元素，导致无法裁剪，这时候可以添加`--ignore 1`参数，再做尝试。 请优先不带`ignore`尝试，有问题再带参数，人工检查一遍即可。

注意：发现任何问题，请参看`issue`，若仍无法解决，请提新`issue`（请`--verbose`执行并附带log）。

# Test
`pytest -s tests/test.py`

# Misc

## Limitation

Known limitation:

- Only scan one level folder
- Some pdf with edit may cause failure (TODO: it is a function missing)
- Support single page pdf, but may not support well for multiple pages (try it first)
- Some cases with too many white part may cause failure (TODO: it is a function missing)

已知部分限制：

- 只扫描一级目录，不支持递归。
    - 可以有效防止错误操作而产生大量的文件IO。
    - 工具已实现自动化，以一级目录为单位也足够使用。
    - 同理，禁止对同目录/同文件进行操作。
- 对于原始PDF文件可以妥善完成裁剪，但如果是其他工具编辑（特别是裁剪）过的PDF，再次裁剪则可能输出错误。
    - 因为该工具通过修正PDF中的media box实现裁剪，可能与其他工具不兼容。
- 偶尔会出现裁剪过度精细的情况，待修正。
    - 本质上，白边就是无内容的部分，因此工具会统计所有有含义的部分（如textbox，image等），并计算最大的有效坐标范围，这一范围以外的部分即视为白边。


## Bugfix & Feature
- (bugfix) path process error in batch_cut_pdf.
- (bugfix) missing literal or text.
- (feature) GUI base on PySide2 (the official).
- (bugfix) failed for pdf which has been edited before - not fix the pos for the edited (pdfminer use relative pos).
- (feature) CLI using argparse.

## Dependency
- PyPDF2: edit the pdf box
- pdfminer & pdfminer3: scan elements
- PySide2: optional for GUI only
