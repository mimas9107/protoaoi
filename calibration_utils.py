# calibration_utils.py

import cv2
import numpy as np

def perform_calibration(camera_index=0, known_distance_mm=200.0):
    """
    執行相機校準程序，計算像素與毫米的比例。
    
    參數:
        camera_index (int): 要使用的相機索引 (e.g., 0, 1)。
        known_distance_mm (float): 校準板上兩個標記點之間的已知實際距離 (mm)。
        
    回傳:
        float: PIXEL_TO_MM_RATIO (如果成功), 否則回傳 None。
    """
    print("--- 啟動校準程序 ---")
    print(f"請將已知尺寸為 {known_distance_mm}mm 的校準物放置於檢測台上，並按 'c' 拍照。")
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("錯誤：無法開啟相機。請檢查索引或連接。")
        return None

    ratio = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("錯誤：無法從相機擷取畫面。")
                break
            
            # 顯示即時畫面
            cv2.putText(frame, "Place Calibration Target & Press 'C' to Capture", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow("Calibration View", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                # 捕獲校準圖像
                cal_image = frame.copy()
                cv2.destroyWindow("Calibration View")
                
                # --- 圖像處理：找到校準物邊緣 ---
                gray = cv2.cvtColor(cal_image, cv2.COLOR_BGR2GRAY)
                # 假設校準物是高對比度的，使用二值化找到邊緣
                _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                
                # 尋找輪廓
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if not contours:
                    print("警告：未找到任何輪廓。請檢查光線或閾值設置。")
                    break

                # 假設最大的輪廓是我們的校準物
                largest_contour = max(contours, key=cv2.contourArea)
                
                # 獲取校準物的外接矩形
                x, y, w_pixel, h_pixel = cv2.boundingRect(largest_contour)

                # 為了簡化，我們假設 w_pixel 就是對應 known_distance_mm 的像素距離
                # 實際應用中，您可能需要更精確的校準板（如棋盤格）和演算法
                known_pixel_distance = max(w_pixel, h_pixel) # 取長邊作為像素距離

                if known_pixel_distance > 0:
                    ratio = known_distance_mm / known_pixel_distance
                    print(f"校準成功! 已知像素距離: {known_pixel_distance} 像素")
                    print(f"計算得出的 PIXEL_TO_MM_RATIO: {ratio:.4f} mm/pixel")
                    break
                else:
                    print("警告：計算像素距離為 0。請重新嘗試。")
                    break
            
            elif key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        
    return ratio

if __name__ == '__main__':
    # 測試校準函數 (當單獨運行此文件時)
    # 請在執行前準備一個已知長度 200mm 的標準物。
    calibration_ratio = perform_calibration(known_distance_mm=200.0)
    print(f"最終校準結果：{calibration_ratio}")
