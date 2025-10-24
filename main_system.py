# main_system.py

from calibration_utils import perform_calibration
from batch_inspector_cam import inspect_batch
import cv2

# 系統配置參數
CAMERA_INDEX = 1      # 您的相機索引 (通常為 0)
KNOWN_CALIB_DISTANCE = 50.0 # 校準物上兩個點的已知距離 (mm)
MIN_PRODUCT_SIZE = 48.0      # 產品最小合格尺寸 (mm)
THRESHOLD=192
THRESHOLD_MODE=cv2.THRESH_BINARY


if __name__ == '__main__':
    # 步驟 1: 執行標準校準
    pixel_ratio, aspect = perform_calibration(
        camera_index=CAMERA_INDEX, 
        known_distance_mm=KNOWN_CALIB_DISTANCE,
        threshold_value=THRESHOLD
    )
    
    if pixel_ratio is None:
        print("\n系統啟動失敗：校準失敗。請檢查相機和校準物。")
    else:
        print("\n*** 校準完成，開始啟動批量檢測系統 ***")
        
        # 步驟 2: 執行批量檢測
        total, ng = inspect_batch(
            camera_index=CAMERA_INDEX,
            pixel_to_mm_ratio=pixel_ratio,
            min_mm_size=MIN_PRODUCT_SIZE,
            threshold=THRESHOLD

        )
        
        print("\n--- 系統運行結束 ---")
        print(f"總共檢測布料：{total} 片")
        print(f"總共不合格布料：{ng} 片")
        print(f"不合格率：{ng/total*100:.2f}%" if total > 0 else "N/A")
