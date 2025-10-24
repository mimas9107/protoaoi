# batch_inspector.py

import cv2
import numpy as np

def inspect_batch(camera_index, pixel_to_mm_ratio, min_mm_size=49.0, threshold=128, aspect_ratio:float=1.0):
    """
    啟動批量檢測程序。
    
    參數:
        camera_index (int): 相機索引。
        pixel_to_mm_ratio (float): 校準後的像素/毫米比例 (mm/pixel)。
        min_mm_size (float): 最小合格尺寸 (mm)。
        
    回傳:
        tuple: (檢測總數, 不合格總數)
    """
    if pixel_to_mm_ratio is None or pixel_to_mm_ratio <= 0:
        print("錯誤：校準比例無效，無法進行檢測。")
        return 0, 0

    MIN_PIXEL_SIZE = min_mm_size / pixel_to_mm_ratio # 最小合格尺寸 (像素)
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("錯誤：無法開啟相機。請檢查索引或連接。")
        return 0, 0

    print("\n--- 啟動批量檢測程序 ---")
    print(f"最小合格尺寸 (mm): {min_mm_size:.1f} | 最小像素尺寸: {MIN_PIXEL_SIZE:.1f}")
    print("請放置布料，並按 's' 進行掃描，按 'q' 退出。")
    
    total_scanned = 0
    total_ng = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("錯誤：無法從相機擷取畫面。")
                break
            
            # 顯示即時畫面
            #cv2.putText(frame, "Place 5x5 Batch & Press 'S' to Scan", (10, 30), 
            #            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Inspection View, press s to scan. ", frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                scan_image = frame.copy()
                
                # --- 檢測核心邏輯 (與前次回答的邏輯相似) ---
                gray = cv2.cvtColor(scan_image, cv2.COLOR_BGR2GRAY)
                # 假設背光，布料為深色，背景為淺色
                _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY) 
                
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                batch_ng_count = 0
                
                for contour in contours:
                    # 最小外接矩形
                    rect = cv2.minAreaRect(contour)
                    (x, y), (w_pixel, h_pixel), angle = rect
                    
                    # 判斷合格/不合格 (使用像素尺寸進行快速判斷)
                    is_ng = False
                    # 檢查兩個方向的像素尺寸是否都小於最小合格像素尺寸
                    if w_pixel < MIN_PIXEL_SIZE or h_pixel < MIN_PIXEL_SIZE:
                        is_ng = True
                        batch_ng_count += 1
                        box_color = (0, 0, 255)  # NG 品：紅色
                    else:
                        box_color = (0, 255, 0)  # 合格品：綠色

                    # 繪製結果
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(scan_image, [box], 0, box_color, 1)
                    
                    # 轉換回 mm 進行標註 (用於偵錯和紀錄)
                    w_mm = w_pixel * pixel_to_mm_ratio
                    h_mm = h_pixel * pixel_to_mm_ratio
                    text = f"W:{w_mm:.2f} H:{h_mm:.2f}"
                    cv2.putText(scan_image, text, (int(x), int(y - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, box_color, 1)

                total_scanned += len(contours)
                total_ng += batch_ng_count
                
                print(f"--- 掃描結果：檢測 {len(contours)} 片, NG {batch_ng_count} 片 ---")
                
                # 顯示單次掃描結果
                cv2.imshow("Scan Result", scan_image)
                cv2.waitKey(2000) # 顯示 2 秒讓操作員確認

            elif key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        
    return total_scanned, total_ng
