# 第二题：高光谱遥感影像基础操作

## 题目要求

根据图片中的第二题，需要完成两件事：

1. 可视化给定高光谱影像，结果保存为 `png`。
2. 可视化给定高光谱影像中包含地物的光谱曲线，结果保存为 `png`。

题面给出的参考资料和数据下载链接是 EHU 的 Hyperspectral Remote Sensing Scenes 页面，数据集使用 Salinas scene。

## 你提供的 xlsx 是否有用

有用，但主要是辅助资料：

- `Spectral Python (SPy)` 文档适合学习高光谱数据读取和显示思想。
- GitHub 的 true color reproduction 项目适合参考假彩色/真彩色可视化思路。
- 视频适合补背景。

真正直接解题的数据仍建议使用题面指定的 Salinas 数据。

## 可参考的开源资料

- 题面指定数据集页面：EHU Hyperspectral Remote Sensing Scenes  
  `https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes`
- Spectral Python 文档：  
  `https://www.spectralpython.net/`
- Spectral Python 源码：  
  `https://github.com/spectralpython/spectral`
- SciPy `loadmat` 文档：  
  `https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html`
- Matplotlib `imsave` 文档：  
  `https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imsave.html`

## 需要下载的数据

从题面链接进入 EHU 页面，找到 `Salinas scene`，下载：

- `Salinas_corrected.mat`
- `Salinas_gt.mat`

放到本项目的 `data/` 目录：

```text
data/Salinas_corrected.mat
data/Salinas_gt.mat
```

## 安装依赖

建议创建虚拟环境后安装，避免污染系统 Python：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行方式

生成假彩色影像：

```bash
python T2/1.py
```

输出：

```text
T2/1.png
```

生成典型地物光谱曲线：

```bash
python T2/2.py
```

输出：

```text
T2/2.png
```

## 1G 内存限制说明

Salinas 数据规模相对小，`Salinas_corrected` 约为 `512 x 217 x 204`。即使读取为 `uint16`，原始数组约几十 MB，正常低于 1G。

代码里仍然做了低内存处理：

- `1.py` 只抽取 3 个波段生成 RGB，不复制完整三维数据做归一化。
- `2.py` 每类最多抽样 `2000` 个像素计算平均光谱，不把某一类所有像素一次性复制成大矩阵。
- 只保存最终 PNG，不保存中间大数组。

如果运行环境仍然紧张，可以降低抽样数：

```bash
python T2/2.py --max-pixels 500
```

## 可调参数

脚本默认会自动识别 `.mat` 里的三维影像变量，并自动选择 3 个波段映射为 R/G/B。也可以手动指定假彩色波段：

```bash
python T2/1.py --bands 57 27 17
```

选择要绘制光谱曲线的地物类别；如果不指定，脚本会自动选择样本数最多的 5 个非背景类别：

```bash
python T2/2.py --classes 1,6,8,10,15
```

如果换成 EHU 页面里的其他数据集，例如 Indian Pines：

```bash
python T2/1.py --input data/Indian_pines_corrected.mat --output T2/indian_pines_image.png
python T2/2.py --cube data/Indian_pines_corrected.mat --gt data/Indian_pines_gt.mat --output T2/indian_pines_spectra.png
```

如果自动识别变量失败，可以先查看报错中列出的变量名，然后手动指定：

```bash
python T2/1.py --input data/example.mat --variable variable_name
python T2/2.py --cube data/example.mat --gt data/example_gt.mat --cube-variable image_variable --gt-variable gt_variable
```

大多数带有 `影像 .mat + groundtruth .mat` 的 EHU 数据集都可以这样处理。没有地物标注的 Cuprite 只能运行 `T2/1.py` 做影像可视化，不能用 `T2/2.py` 画按类别划分的地物光谱曲线。
