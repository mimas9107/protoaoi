# 簡易的自動影像量測
## 為了快速解決人員工作量負擔

1. 硬體環境：
  - USB Camera 640x480 (VGA)
  - acer notebook   
2. 技術堆疊：
  - python 3.11 (venv environment)
  - opencv 4.12 (library installed by pip)
3. 環境架設：
  - tripod for camera
  - camera height=250mm
4. 流程解說：
  - Camera Calibration by standard sample. pixel_mm_ratio is needed for next process.
  - Let user press a key to scan the target sample.
  - get the sample size. => good / NG.
  - count the failure rate.

5. 測試結果：
    
6. 結論
   * Sample / Background contrast must be higher. Black background was recommended. 
   * Since the standard sample was getting shift out of the center of lens, the image will not be the actual rectangle.
   * Wrong image => wrong measure.  
   * Camera lens distortion is a big issue.
   * Ambient light is also a critical factor to the image grabing system.
   * Since the light can't lighten the measuring stage region, the image process will grab wrong rectangle. (minimum area rectangle algorithm) 
 
