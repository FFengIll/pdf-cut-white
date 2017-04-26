# pdf-cut-white

该工具可以用于自动批量裁剪PDF白边。  
使用该工具请直接下载dist文件夹中对应的文件即可。  
使用非常简单，若仍需要帮助说明，请参见[Usage](#Usage)

## Motivation
在使用Latex书写论文时，花费了不少的时间处理PDF图表——裁剪不必要的图表白边。  
所幸就写个工具自动完成吧——自动化且精准。

## Feature
工具可以对生成的PDF图表（如Latex文档撰写时生成的图表）进行自动裁剪，减少人工操作和其他软件依赖（如Acrobat）。  
其自动的工作流程为：
- 读取原始PDF文件
- 识别PDF中的白边
- 裁剪白边（缩减media box）
- 输入无白边PDF文件

## Usage
* 启用工具
* 选择输入文件夹和输出文件夹（建议使用不同的文件夹防止源文件覆盖）
* 扫描文件，而后可以在列表中选择需要裁剪的PDF。（注意：仅会扫描一级目录，而不会扫描子目录）
* 确认无误后，点击完成PDF裁剪（仅选中的文件），并输出到输出文件夹下

## Comment
* 之所以只扫描一级目录而不递归，是为了防止错误操作而产生大量的扫描、创建等工作。因为工具已经是自动化的了，所以以一级目录为单位进行操作也足够了。
* 对于原始PDF文件，本工具可以妥善完成裁剪，但如果是用其他工具裁剪过的PDF，再次裁剪则可能输出错误。因为该工具通过修正PDF中的media box实现裁剪，可能与其他工具不兼容。
* 本质上，白边就是无内容的部分，因此工具会统计所有有含义的部分（如textbox，image等），并计算最大覆盖的坐标范围，这一范围以外的部分即视为白边。

## Dependency
Required:
* PyPDF2 (edit box)
* pyminer (scan elements)

Optional:
* PyQT (GUI)
* Pyinstaller (generate exe)

Mention: 
* No dependencies needed while use packaged exe version.
* For develop, need the required.
* For GUI and Bin, need the optional too.