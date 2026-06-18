# 高光谱遥感影像基础操作

本项目用于完成“高光谱遥感影像基础操作”题目，默认使用 EHU 页面中的 **Salinas scene** 数据集。

## 题目目标

需要完成两个输出：

1. 将高光谱遥感影像可视化为 PNG 图片。
2. 绘制影像中典型地物的光谱曲线，并保存为 PNG 图片。

对应输出文件：

```text
T2/1.png
T2/2.png
```

## 数据集下载

数据来源：

```text
https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes
```

进入页面后找到 **Salinas scene**，下载以下两个文件：

```text
Salinas_corrected.mat
Salinas_gt.mat
```

在项目根目录下新建 `data` 文件夹，并将下载好的文件放入其中：

```text
data/Salinas_corrected.mat
data/Salinas_gt.mat
```

说明：原始 `.mat` 数据文件较大，仓库中没有上传，需要按上述方式自行下载。

## 环境安装

建议使用虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

依赖包括：

```text
numpy
scipy
matplotlib
```

## 运行步骤

### 1. 生成高光谱影像可视化图

运行：

```bash
python T2/1.py
```

默认读取：

```text
data/Salinas_corrected.mat
```

默认输出：

```text
T2/1.png
```

### 2. 生成典型地物光谱曲线图

运行：

```bash
python T2/2.py
```

默认读取：

```text
data/Salinas_corrected.mat
data/Salinas_gt.mat
```

默认输出：

```text
T2/2.png
```

## 代码文件说明

```text
T2/1.py          读取高光谱影像，选取 3 个波段生成假彩色图
T2/2.py          根据 ground truth 标注提取典型地物，绘制平均光谱曲线
T2/hsi_utils.py  通用工具函数，用于识别 .mat 变量、读取数据和选择类别
requirements.txt Python 依赖列表
```

## 可选参数

手动指定 RGB 波段：

```bash
python T2/1.py --bands 57 27 17
```

手动指定要绘制的地物类别：

```bash
python T2/2.py --classes 1,6,8,10,15
```

降低光谱曲线计算时每类抽样像素数：

```bash
python T2/2.py --max-pixels 500
```

## 更换数据集

代码可以适配 EHU 页面中多数 `.mat + gt.mat` 格式的数据集。例如 Indian Pines：

```bash
python T2/1.py --input data/Indian_pines_corrected.mat --output T2/indian_pines_image.png
python T2/2.py --cube data/Indian_pines_corrected.mat --gt data/Indian_pines_gt.mat --output T2/indian_pines_spectra.png
```

如果自动识别变量失败，可以手动指定 `.mat` 文件中的变量名：

```bash
python T2/1.py --input data/example.mat --variable image_variable
python T2/2.py --cube data/example.mat --gt data/example_gt.mat --cube-variable image_variable --gt-variable gt_variable
```

注意：如果数据集没有 ground truth 标注文件，只能运行 `T2/1.py` 生成影像可视化图，不能按地物类别绘制光谱曲线。

## 运行内存与空间复杂度说明

题目要求注意 1G 运行内存限制。设高光谱影像尺寸为：

```text
H x W x B
```

其中 `H` 为图像高度，`W` 为图像宽度，`B` 为波段数。Salinas corrected 数据约为：

```text
512 x 217 x 204
```

因此主要内存来自读取后的高光谱三维数组，空间复杂度为：

```text
O(H * W * B)
```

本项目的低内存处理重点是控制“额外空间”，避免在读取原始数据后继续产生多个同样大小的三维副本。

### T2/1.py 的内存处理

`T2/1.py` 用于生成假彩色图。程序只从完整高光谱影像中取 3 个波段映射为 RGB，而不是把所有波段都转换成新的大数组。

额外空间主要包括：

```text
3 个单波段数组 + 1 个 RGB 图像数组
```

其额外空间复杂度约为：

```text
O(H * W)
```

这样做的原因是：题目只要求输出一张可视化 PNG，不需要对全部 `B` 个波段同时进行可视化处理，所以没有必要复制完整的 `H x W x B` 数据。

### T2/2.py 的内存处理

`T2/2.py` 用于绘制典型地物光谱曲线。若直接取出某一类别的全部像素光谱，数据量可能随类别像素数增大而明显增加。因此程序默认对每个类别最多抽样 `2000` 个像素，再计算平均光谱。

设绘制的类别数为 `K`，每类最多抽样像素数为 `S`，则额外空间复杂度约为：

```text
O(K * S * B)
```

默认情况下 `S = 2000`，远小于整幅影像的像素总数 `H * W`，因此可以避免为某些大类别一次性复制过多像素光谱。

如果运行环境更紧张，可以继续降低抽样数：

```bash
python T2/2.py --max-pixels 500
```

### 实测结果

在 Salinas 数据集上实测峰值内存约为：

```text
T2/1.py 约 147 MB
T2/2.py 约 164 MB
```

两者都明显低于 1G，因此满足题目的运行内存限制。
