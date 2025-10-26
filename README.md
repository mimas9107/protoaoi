# 簡易自動影像量測  
## 目的  
以基本影像量測方式，減少人員手動作業負擔。

### 硬體  
1. USB 攝影機（640×480，VGA）  
2. Acer 筆電  

### 軟體  
- Python 3.11（虛擬環境）  
- OpenCV 4.12（以 pip 安裝）

### 環境設定  
1. 攝影機固定於腳架上  
2. 鏡頭高度：250 mm  

### 流程  
1. 使用標準樣品進行鏡頭校正，取得像素與實際毫米比例（pixel-to-mm ratio）  
2. 使用者按鍵拍攝測試樣品  
3. 量測樣品尺寸 → 判定為「合格 / 不合格」  
4. 統計不良率  

### 測試結果  
（待補資料）

### 結論  
1. 樣品與背景需有較高對比，建議使用黑色背景。  
2. 樣品若偏離鏡頭中心，影像會變形。  
3. 影像失真會導致量測誤差。  
4. 鏡頭畸變對準確度影響明顯。  
5. 周圍光線對影像擷取影響重大。  
6. 若光線無法照亮量測區域，會造成最小外接矩形演算法判斷錯誤。  


---

# Simple Auto Image Measurement  
## Purpose  
Reduce manual workload using basic vision measurement.

### Hardware
1. USB Camera (640×480, VGA)  
2. Acer notebook  

### Software
- Python 3.11 (venv)  
- OpenCV 4.12 (pip install)

### Setup
1. Camera on tripod  
2. Height = 250 mm  

### Process
1. Calibrate camera with standard sample → get pixel-to-mm ratio  
2. Press key to capture target sample  
3. Measure sample size → Pass / Fail  
4. Count failure rate  

### Result
(To be added)

### Conclusion
1. Higher contrast needed; black background recommended  
2. Sample shift from lens center causes shape distortion  
3. Wrong image → wrong measure  
4. Lens distortion is critical  
5. Ambient light strongly affects image grabbing  
6. Poor lighting causes wrong rectangle detection (min area rect algorithm)
