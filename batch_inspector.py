import cv2
import numpy as np

# --- Step 1: 預設參數 (需要根據 Step 2 校準結果調整) ---
#PIXEL_TO_MM_RATIO = 5.0      # 假設 1mm 實際距離對應 5.0 像素
PIXEL_TO_MM_RATIO=0.072647
MIN_MM_SIZE = 40.0           # 最小合格尺寸 (mm)
MIN_PIXEL_SIZE = MIN_MM_SIZE * PIXEL_TO_MM_RATIO # 最小合格尺寸 (像素)
# 整個 5x5 檢測區域的預期起點和終點 (像素座標)，用於區域裁切
ROI_START = (100, 100)
ROI_END = (1200, 1200)

def detect_and_measure(image_path):
    """
    主要檢測函數：處理一張包含 5x5 布片的圖像。
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # 1. 圖像預處理：灰度化和裁切 ROI
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 裁切到感興趣區域 (Region of Interest, ROI)
    roi_img = gray[ROI_START[1]:ROI_END[1], ROI_START[0]:ROI_END[0]]

    # 2. 邊緣檢測 (利用背光優勢)
    # 由於是背光台，布片區域較暗，背景較亮。閾值處理 (Thresholding) 是最佳選擇。
    # 選擇一個閾值，將布片 (深色) 與背光 (淺色) 分開
    _, thresh = cv2.threshold(roi_img, 100, 255, cv2.THRESH_BINARY_INV)

    # cv2.THRESH_BINARY_INV：反轉，讓布片邊緣成為白色 (前景)

    # 3. 尋找輪廓 (Find Contours)
    # 尋找所有獨立布片的輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ng_count = 0
    
    # 在原始彩色圖上繪製結果 (用於視覺化調試)
    display_img = img.copy()

    for i, contour in enumerate(contours):
        # 4. 最小外接矩形 (Minimum Bounding Box)
        # 使用旋轉矩形可以更精確地測量物體的長寬，不受角度影響
        rect = cv2.minAreaRect(contour)
        (x, y), (w_pixel, h_pixel), angle = rect
        
        # 轉換為實際尺寸 (mm)
        w_mm = w_pixel / PIXEL_TO_MM_RATIO
        h_mm = h_pixel / PIXEL_TO_MM_RATIO

        # 5. 判斷合格/不合格
        is_ng = False

        # 檢查兩個尺寸中是否有任一尺寸低於 MIN_MM_SIZE
        if w_mm < MIN_MM_SIZE or h_mm < MIN_MM_SIZE:
            is_ng = True
            ng_count += 1
            box_color = (0, 0, 255)  # NG 品：紅色
        else:
            box_color = (0, 255, 0)  # 合格品：綠色

        # 6. 繪製結果與標註
        # 將旋轉矩形的四個點座標畫出來
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 為了能在原始圖上顯示，需要將座標平移回原始圖的 ROI 位置
        box[:, 0] += ROI_START[0]
        box[:, 1] += ROI_START[1]

        cv2.drawContours(display_img, [box], 0, box_color, 2)
        
        # 標註尺寸 (用於調試數據)
        text = f"W:{w_mm:.1f} H:{h_mm:.1f} {'NG' if is_ng else 'OK'}"
        cv2.putText(display_img, text, (int(x + ROI_START[0]) - 50, int(y + ROI_START[1]) - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
            
    # 7. 輸出結果
    print(f"Total pieces detected: {len(contours)}, NG count: {ng_count}")
    
    # 顯示檢測結果圖 (用於工程微調與觀察)
    cv2.imshow("Inspection Result", display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return ng_count

if __name__ == '__main__':
    # 範例調用 (假設您已經拍攝好一張測試圖)
    detect_and_measure("test_batch_image.jpg")
