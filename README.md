# pdf-cut-white

## Motivation
While latex, it takes time to `cut the unneccessary white part in pdf`, then, here comes a tool for it.

在使用Latex书写论文时，花费了不少的时间处理PDF图表——`裁剪不必要的图表白边`。

所幸就写个工具自动完成吧——自动化且精准。

## Feature
Automatic cut the unneccessary white part in pdf.
This pdf maybe a print result of table or figure.

工具可以对生成的PDF图表进行自动裁剪，减少人工操作和其他软件依赖（如Acrobat）。  

其自动的工作流程为：
* 读取原始PDF文件
* 识别PDF中的白边
* 裁剪白边（缩减media box）
* 输入无白边PDF文件

## Usage
Before all, install the necessary dependency:
* `pip install pdfminer PyPDF2`
* `pip3 install pdfminer3 PyPDF2`
* or `pip install -r requirements.txt`
* may add `--user` for user mode

Recommend to use `command line tool` (not the GUI):
* single file: `python cutwhite.py -i in.pdf -o out.pdf`
* folder: `python cutwhite.py -id infolder -od outfolder`

If you wanna use the GUI (base on PySide2: official Qt for Python):
* `pip install pyside2`
* if success, run `python gui.py`
* enjoy it~!

推荐使用命令行版本（命令如上），若希望使用GUI版本，请确保能够成功安装PySide2（命令如上）：
* 启用工具，选择输入文件夹和输出文件夹（必须使用不同的文件夹防止源文件覆盖）
* 扫描pdf文件（GUI支持在列表中二次选择PDF）（注意：仅会扫描一级目录，而不会扫描子目录）
* 确认无误后，点击完成PDF裁剪（仅选中的文件），并输出到输出文件夹下

## Limit
Known limit:
* Only scan one level folder
* Some pdf with edit may cause failure (TODO: it is a function missing)
* Support single page pdf, but may not support well for multiple pages (try it first)
* Some cases with too many white part may cause failure (TODO: it is a function missing)

已知部分限制：
* 只扫描一级目录，不支持递归。
    * 可以有效防止错误操作而产生大量的文件IO。
    * 工具已实现自动化，以一级目录为单位也足够使用。
    * 同理，禁止对同目录/同文件进行操作。
* 对于原始PDF文件可以妥善完成裁剪，但如果是其他工具编辑（特别是裁剪）过的PDF，再次裁剪则可能输出错误。
    * 因为该工具通过修正PDF中的media box实现裁剪，可能与其他工具不兼容。
* 偶尔会出现裁剪过度精细的情况，待修正。
    * 本质上，白边就是无内容的部分，因此工具会统计所有有含义的部分（如textbox，image等），并计算最大的有效坐标范围，这一范围以外的部分即视为白边。

## Misc
### Bug / Feature Missing
* (added) GUI base on PySide2 (the official).
* (fixed) failed for pdf which has been edited before - not fix the pos for the edited (pdfminer use relative pos).
* (fixed) no CLI - argparse now.

### Required
* PyPDF2 (edit box)
* pdfminer (scan elements) (for python2)
* pdfminer3 (for python3)

### Optional
* PySide2 (gui only)
* Pyinstaller (generate exe only)

### Mention
* No dependencies needed while use packaged exe version.
* For develop, need the `required`.
* For GUI and Bin, need the `optional` too.