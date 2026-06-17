# 高光谱遥感影像基础操作解题报告

## 一、题目理解

本题要求对给定高光谱遥感影像完成基础操作，主要包括两部分：

1. 将高光谱影像可视化，并保存为 `png` 图片。
2. 提取影像中典型地物的光谱信息，绘制光谱曲线，并保存为 `png` 图片。

题目给出的参考数据来源是 EHU 的 Hyperspectral Remote Sensing Scenes 页面。本次实现默认使用其中的 Salinas 数据集，同时代码也尽量兼容该页面中的其他常见 `.mat` 格式高光谱数据集。

## 二、资料使用情况

前期提供的 xlsx 表格中包含高光谱、假彩色合成、Spectral Python 和相关开源代码资料。这些资料对理解高光谱影像可视化有帮助，但不能完全直接作为本题代码使用。

本题最终采用的主要技术路线是：

- 使用 `scipy.io.loadmat` 读取 `.mat` 格式高光谱数据。
- 使用 `numpy` 进行波段提取、归一化和光谱均值计算。
- 使用 `matplotlib` 输出影像可视化结果和光谱曲线图。

## 三、实现思路

### 1. 高光谱影像可视化

高光谱影像通常是一个三维数组，格式为：

```text
高度 x 宽度 x 波段数
```

以 Salinas 数据为例，其影像大小为：

```text
512 x 217 x 204
```

程序从高光谱数据中选取 3 个波段，分别映射到 RGB 三个通道，经过百分位拉伸归一化后保存为假彩色图像。

对应脚本：

```bash
python T2/1.py
```

默认输出：

```text
T2/1.png
```

### 2. 地物光谱曲线绘制

光谱曲线需要同时使用影像数据和地物标注数据。程序读取：

```text
data/Salinas_corrected.mat
data/Salinas_gt.mat
```

其中影像文件提供每个像素在不同波段上的反射值，标注文件提供每个像素所属的地物类别。程序会自动选择样本数量较多的非背景类别，对每一类抽样计算平均光谱，并绘制曲线。

对应脚本：

```bash
python T2/2.py
```

默认输出：

```text
T2/2.png
```

## 四、代码文件说明

本题主要文件如下：

```text
T2/1.py          生成高光谱假彩色可视化图
T2/2.py          生成典型地物光谱曲线图
T2/hsi_utils.py  通用工具函数，用于识别 .mat 变量、读取数据、选择波段和类别名称
T2/README.md     运行说明
requirements.txt Python 依赖
```

其中 `hsi_utils.py` 的作用是提高代码通用性。不同数据集的 `.mat` 文件变量名可能不同，例如 Salinas、Indian Pines、Pavia 等数据集的变量名并不完全一致。该工具文件会优先识别常见变量名，如果识别失败，则自动寻找三维数组作为高光谱影像、二维数组作为地物标注。

## 五、运行方式

安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

运行可视化：

```bash
python T2/1.py
python T2/2.py
```

如果要换成其他 EHU 数据集，例如 Indian Pines，可以指定输入文件：

```bash
python T2/1.py --input data/Indian_pines_corrected.mat --output T2/indian_pines_image.png
python T2/2.py --cube data/Indian_pines_corrected.mat --gt data/Indian_pines_gt.mat --output T2/indian_pines_spectra.png
```

## 六、1G 内存限制说明

本题特别要求注意运行内存 1G。程序中做了以下控制：

1. 影像可视化时只提取 3 个波段，不对完整高光谱数据做多份复制。
2. 光谱曲线绘制时，每类默认最多抽样 `2000` 个像素计算平均光谱，避免一次性复制大量像素数据。
3. 只保存最终 PNG 图片，不保存大型中间数组。

实测在当前 Salinas 数据上：

```text
T2/1.py 峰值内存约 147 MB
T2/2.py 峰值内存约 164 MB
```

因此程序运行内存明显低于 1G，满足题目限制。

## 七、需要注意的问题

1. `.mat` 文件不是只要存在就一定能可视化，必须包含三维高光谱影像数组。
2. 绘制地物光谱曲线需要 ground truth 标注文件，如果数据集没有标注文件，只能生成影像可视化图，不能按类别绘制光谱曲线。
3. 不同数据集的类别名称、变量名、波段数可能不同，因此代码虽然做了通用适配，但必要时仍可通过命令行参数手动指定变量名或波段。
4. 假彩色图像的颜色效果与所选波段有关，不同波段组合会得到不同视觉效果。
5. 对于特别大的数据集，应适当降低 `--max-pixels` 参数，例如：

```bash
python T2/2.py --max-pixels 500
```

## 八、总结

本题通过 Python 完成了高光谱遥感影像的读取、假彩色可视化和地物光谱曲线绘制。代码默认适配 Salinas 数据集，并扩展为可兼容 EHU 页面中多个常见 `.mat` 数据集的通用版本。程序运行内存约 160 MB，满足 1G 内存限制，输出结果符合题目要求。
