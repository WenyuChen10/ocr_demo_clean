\#OCR 憑證辨識專案



使用 \*\*PaddleOCR\*\* 開發的繁體中文 OCR 專案，能夠對圖片進行文字偵測與辨識。  

專案用於學習 OCR 技術，並作為面試展示作品，支援多張圖片辨識與座標輸出。



---



\## 系統需求



\- Python 3.8+

\- OpenCV (`opencv-python`)

\- PaddleOCR (`paddleocr`)

\- GPU (可選，程式可在 CPU 執行)

\- 作業系統：Windows



---



\## 安裝指令



```bash

\# 建議使用虛擬環境

python -m venv venv

source venv/bin/activate  # Linux / Mac

venv\\Scripts\\activate     # Windows



\# 安裝套件

pip install paddleocr opencv-python



專案結構

ocr\_demo\_clean/

├─ images/

│   └─ raw/

│       ├─ id1.png

│       ├─ id2.jpg

│       ├─ id3.png

│       ├─ id4.jpg

│       └─ id5.jpg

├─ ocr\_demo.py

└─ README.md



程式碼片段

from paddleocr import PaddleOCR

import cv2



\# 初始化 OCR（繁體中文）

ocr = PaddleOCR(use\_gpu=False, lang='chinese\_cht', show\_log=False)



\# 讀取圖片

img\_path = "images/raw/id1.png"

img = cv2.imread(img\_path)



\# 執行 OCR

result = ocr.ocr(img, cls=True)



\# 顯示結果

for line in result\[0]:

&nbsp;   box = line\[0]             # 文字框座標

&nbsp;   text = line\[1]\[0]         # 辨識文字

&nbsp;   score = line\[1]\[1]        # 信心分數

&nbsp;   print(f"{text} ({score:.2f})")

&nbsp;   print(f"box = {box}")

&nbsp;   print("-" \* 30)



程式執行步驟

1\.確認圖片放置於 images/raw/ 資料夾。

2\.在專案目錄下開啟終端機。

3\.執行程式：

python ocr\_demo.py

4\.程式會依序辨識圖片文字，並在終端機印出文字、信心分數與文字框座標。



注意事項

1\.PaddleOCR 可能會對相似字辨識有偏差，例如「臺」與「高」需根據實際字體微調。

2\.若圖片解析度太低，OCR 可能辨識錯誤，可嘗試提高圖片品質。

3\.專案可擴充多張圖片自動批次辨識，或結合 JSON / COCO 標註進行資料前處理。



可延伸功能

1\.批次辨識多張圖片並輸出 Excel / CSV。

2\.文字框座標可結合 OpenCV 做高亮標記或截圖。

3\.進行深度學習模型微調（fine-tuning）以改善特定字體辨識。

