# -*- coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

# 移動平均線の計算(データ, 日数)
def move_average(data, day):
    return np.convolve(data, np.ones(day)/float(day), 'valid')

# ゴールデンクロスの座標取得
def golden_cross(f1, f2):
    pt = []
    df = f1 - f2
    i = 0
    # 短い方(f1)が長い方(f2)を上に突き抜けた時の座標取得
    for i in range( len(df)-1 ):            
        if(df[i] < 0 and df[i+1] > 0):
            pt.append([i, f1[i]])
            
    return np.array(pt)

# デッドクロスの座標取得    
def dead_cross(f1, f2):
    pt = []
    df = f1 - f2
    i = 0
    # 短い方(f1)が長い方(f2)を下に突き抜けた時の座標取得
    for i in range( len(df)-1 ):
        if(df[i] > 0 and df[i+1] < 0):
            pt.append([i, f1[i]])            
    return np.array(pt)

    
def main():
     # CSVのロード(2015年と2016年のデータ)
    data15 = np.genfromtxt("nikkei15.csv", delimiter=",", skip_header=1, dtype='float')
    data16 = np.genfromtxt("nikkei16.csv", delimiter=",", skip_header=1, dtype='float')
    # 5列目の終値だけを取り出し
    f15 = data15[:,4]
    f16 = data16[:,4]
    
    # 移動平均線(25日線)の計算
    day = 25    # 日数
    data = np.r_[f15[len(f15)-day+1:len(f15)], f16]    #　2015年の終値の一部と2016年の終値を結合
    ma_25d = move_average(data, day)

    # 移動平均線(75日線)の計算
    day = 75    # 日数
    data = np.r_[f15[len(f15)-day+1:len(f15)], f16]    #　2015年の終値の一部と2016年の終値を結合
    ma_75d = move_average(data, day)
    
    # ゴールデンクロスとデッドクロスの探索
    gc = golden_cross(ma_25d, ma_75d)
    dc = dead_cross(ma_25d, ma_75d)

    # グラフにプロット
    plt.plot(f16,  label="f")
    plt.plot(ma_25d, "--", color="r", label="MA 25d")
    plt.plot(ma_75d, "--", color="g", label="MA 75d")    
    plt.plot(gc[:,0],gc[:,1],"o", ms=10, label="Golden Cross")      
    plt.plot(dc[:,0],dc[:,1],"o", ms=10, label="Dead Cross")  
    #　ラベル軸
    plt.xlabel("Day")
    plt.ylabel("f")
    # 凡例
    plt.legend(bbox_to_anchor=(1.01,1), loc=2, borderaxespad=0)
    # グリッド
    plt.grid()
    # グラフ表示
    plt.show()

    
if __name__ == "__main__":
    main()
