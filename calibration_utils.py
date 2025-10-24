# calibration_utils.py (Ver. 1 - 修正二值化與旋轉矩形)

import cv2
import numpy as np

def perform_calibration(camera_index=0, known_distance_mm=200.0, threshold_value=128):
    """
    執行相機校準程序，使用最小旋轉矩形，以抵抗被測物旋轉。
    """
    print("--- 啟動校準程序 (Ver. 1) ---")
    print(f"**環境假定：淺色布片 (類膚色) + 黑色背景**")
    print(f"請將已知尺寸為 {known_distance_mm}mm 的校準物放置於檢測台上，並按 'c' 拍照。")
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("錯誤：無法開啟相機。請檢查索引或連接。")
        return None

    ratio = None
    aspect = None
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("錯誤：無法從相機擷取畫面。")
                break
            
            # ... (Step 0: 顯示即時畫面，省略以保持精簡) ...
            display_frame = frame.copy()
            cv2.putText(display_frame, "Press 'C' to Capture", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow("0. Calibration View (Real-time)", display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                cal_image = frame.copy()
                cv2.destroyWindow("0. Calibration View (Real-time)")
                
                # --- Step 1: 灰度化 ---
                gray = cv2.cvtColor(cal_image, cv2.COLOR_BGR2GRAY)
                cv2.imshow("1. Grayscale Image", gray)
                
                # --- Step 2: 二值化 (修正為適應淺色布片 + 黑色背景) ---
                
                # 假設淺色布片亮度高於背景。閾值可能需要依實際光線調整。
                
                #threshold_value = 128 # 黑色背景下，50 通常足夠區分淺色布片
                _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
                cv2.imshow("2. Threshold Image", thresh)
                
                # --- Step 3: 尋找輪廓 ---
                # 為了避免雜訊，先進行一次簡單的膨脹/腐蝕操作（可選）
                kernel = np.ones((3,3), np.uint8)
                thresh = cv2.dilate(thresh, kernel, iterations = 1) 
                
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if not contours:
                    print("警告：未找到任何輪廓。請檢查光線或閾值設置 (Threshold Value)。")
                    cv2.waitKey(0) 
                    continue 

                # 假設最大的輪廓是我們的校準物
                largest_contour = max(contours, key=cv2.contourArea)
                
                # --- Step 4: 最小外接旋轉矩形 (minAreaRect) ---
                # 這是解決旋轉失真的關鍵步驟
                rect = cv2.minAreaRect(largest_contour)
                (x, y), (w_pixel, h_pixel), angle = rect
                
                # 取旋轉矩形的長邊作為像素距離，因為校準物通常是矩形或正方形
                known_pixel_distance = max(w_pixel, h_pixel)
                
                # --- 繪製輪廓和測量標記 ---
                contour_img = cal_image.copy()
                cv2.drawContours(contour_img, [largest_contour], -1, (0, 255, 0), 3)

                # 繪製旋轉矩形
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(contour_img, [box], 0, (255, 0, 0), 2) # 藍色為測量框

                cv2.putText(contour_img, 
                            f"Pixel Dist (Max Side): {known_pixel_distance:.1f} px", 
                            (int(x) - 50, int(y) - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                
                cv2.imshow("3. Identified Contour & Measurement (Rotated Rect)", contour_img)
                
                # --- Step 5: 計算比例 ---
                if known_pixel_distance > 0:
                    ratio = known_distance_mm / known_pixel_distance
                    aspect = w_pixel/h_pixel
                    print(f"校準成功! 像素距離 (Max Side): {known_pixel_distance:.1f} 像素")
                    print(f"計算得出的 PIXEL_TO_MM_RATIO: {ratio:.4f} mm/pixel")
                    print(f"w/h aspect ratio= {aspect:.4f}")

                else:
                    print("警告：計算像素距離為 0。請重新嘗試。")
                    
                cv2.waitKey(0)
                
                if ratio is not None:
                    break 

            elif key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        
    return (ratio, aspect)
