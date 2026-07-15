# test.py
import numpy as np

def parse_data(filename):
    groups = []
    with open(filename, 'r') as f:
        T = int(f.readline().strip())
        for _ in range(T):
            N = int(f.readline().strip())
            line = f.readline().strip()
            # 模拟真实遥感数据读取，转为 float32
            data = np.array(line.split(), dtype=np.float32)
            groups.append(data)
    return groups

def traditional_variance(data_f32):
    """传统公式：Var = E(X^2) - (E(X))^2，全程使用 float32"""
    ex = np.mean(data_f32, dtype=np.float32)
    ex2 = np.mean(data_f32**2, dtype=np.float32)
    var = ex2 - ex**2
    return max(var, 0.0) # 防止出现负数方差显示NaN

def chan_variance(data_f32, num_chunks=10):
    """Chan 并行合并公式，模拟 T1 的分块流式处理"""
    n_total = len(data_f32)
    chunk_size = max(1, n_total // num_chunks)
    
    n_old = 0
    mean_old = np.float32(0.0)
    m2_old = np.float32(0.0)
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_chunks - 1 else n_total
        chunk = data_f32[start:end]
        
        n_b = len(chunk)
        # 模拟 T1 中的局部高精度计算
        mean_b = np.mean(chunk, dtype=np.float32)
        var_b = np.var(chunk, dtype=np.float32) 
        
        if n_old == 0:
            n_new = n_b
            mean_new = mean_b
            m2_new = np.float32(var_b * n_b)
        else:
            n_new = n_old + n_b
            delta = mean_b - mean_old
            # Chan 合并公式，保持 float32 运算以展示其抗大数相消能力
            mean_new = mean_old + delta * (np.float32(n_b) / np.float32(n_new))
            m2_new = m2_old + np.float32(var_b * n_b) + np.float32(delta**2) * np.float32(n_old * n_b) / np.float32(n_new)
            
        n_old = n_new
        mean_old = mean_new
        m2_old = m2_new
        
    return float(m2_old / np.float32(n_old))

def main():
    from pathlib import Path

    groups = parse_data("T1/test_data.txt")

    header = f"{'组号':<2} | {'真值 (float64)':<15} | {'传统公式 (float32)':<15} | {'Chan公式 (float32)':<15} | {'传统绝对误差':<15} | {'Chan绝对误差':<20}"
    separator = "-" * 120
    print(header)
    print(separator)

    lines = [header + "\n", separator + "\n"]
    for i, data_f32 in enumerate(groups):
        # 1. 计算高精度真值 (将 float32 提升为 float64 计算)
        true_var = np.var(data_f32.astype(np.float64), ddof=0)

        # 2. 传统公式计算 (float32)
        trad_var = traditional_variance(data_f32)

        # 3. Chan 公式计算 (float32)
        chan_var = chan_variance(data_f32, num_chunks=10)

        trad_err = abs(trad_var - true_var)
        chan_err = abs(chan_var - true_var)

        row = f"{i+1:<2} | {true_var:<15.10f} | {trad_var:<15.10f} | {chan_var:<15.10f} | {trad_err:<15.10f} | {chan_err:<20.10f}"
        print(row)
        lines.append(row + "\n")

    output_path = Path("T1/test_result.txt")
    output_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n结果已保存到 {output_path}")

if __name__ == "__main__":
    main()
