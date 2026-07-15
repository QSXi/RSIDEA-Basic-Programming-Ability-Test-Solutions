# generate_data.py
import numpy as np

def generate_data(filename="test_data.txt"):
    np.random.seed(42)
    
    T = 3
    with open(filename, 'w') as f:
        f.write(f"{T}\n")
        
        # 组1：base = 2^20 = 1048576.0。
        # 在 float32 中，此量级的精度(ULP)为 0.125，因此 0~1 的微小波动能被完整保留，真实方差约 0.083。
        # 但平方后数值达到 2^40 (约 1e12) 量级，float32 的 ULP 变为 131072。
        # 此时 E(X^2) 和 E(X)^2 将发生严重的大数相消，传统公式彻底失效。
        N1 = 100000
        base1 = 1048576.0
        # 以 float64 生成保证精度，写入文件
        data1 = np.full(N1, base1, dtype=np.float64) + np.random.uniform(0, 1, N1)
        f.write(f"{N1}\n")
        f.write(" ".join(map(str, data1)) + "\n")
        
        # 组2：base = 2^16 = 65536.0。
        # float32 ULP 为 0.0078，微小波动保留，真实方差约 0.083。
        # 平方后达 2^32，ULP 为 512。传统公式依然会失效。
        N2 = 200000
        base2 = 65536.0
        data2 = np.full(N2, base2, dtype=np.float64) + np.random.uniform(0, 1, N2)
        f.write(f"{N2}\n")
        f.write(" ".join(map(str, data2)) + "\n")
        
        # 组3：常规数据 (0~100)，用于证明在正常情况下两者都没问题
        N3 = 50000
        data3 = np.random.uniform(0, 100, N3)
        f.write(f"{N3}\n")
        f.write(" ".join(map(str, data3)) + "\n")
        
    print(f"测试数据已生成至 {filename}")

if __name__ == "__main__":
    generate_data("T1/test_data.txt")
