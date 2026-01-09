from paddleocr import PaddleOCR
import cv2
import os
import csv

# 專有名詞修正字典
FIX_DICT = {
    "國立高雄師範大學": "國立臺灣師範大學",
}

# 輸出資料夾
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def visualize_and_fix(img, result):
    ocr_texts = []
    for line in result[0]:
        box = line[0]              # 文字框座標
        text = line[1][0]          # 辨識文字
        score = line[1][1]         # 信心分數

        # 專有名詞修正
        if text in FIX_DICT:
            text = FIX_DICT[text]

        # 存結果
        ocr_texts.append([text, score, box])

        # 畫文字框
        pts = [tuple(map(int, point)) for point in box]
        for i in range(4):
            cv2.line(img, pts[i], pts[(i+1)%4], (0,255,0), 2)

        # 標示文字
        cv2.putText(img, text, (pts[0][0], pts[0][1]-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    return img, ocr_texts

def main():
    # 初始化 OCR（CPU）
    ocr = PaddleOCR(
        use_gpu=False,
        lang='chinese_cht',  # 繁體中文
        show_log=False
    )

    # 批次圖片
    images = ["images/raw/id1.png",
              "images/raw/id2.jpg",
              "images/raw/id3.png",
              "images/raw/id4.jpg",
              "images/raw/id5.jpg"]

    all_results = []  # 總表資料

    for img_path in images:
        img_name = os.path.basename(img_path)
        img = cv2.imread(img_path)
        if img is None:
            print(f"讀不到圖片：{img_path}")
            continue

        result = ocr.ocr(img, cls=True)

        # 可視化並修正文字
        img_vis, ocr_texts = visualize_and_fix(img, result)

        # 存圖片
        out_img_path = os.path.join(OUTPUT_DIR, f"vis_{img_name}")
        cv2.imwrite(out_img_path, img_vis)

        # 存單張 CSV
        out_csv_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(img_name)[0]}.csv")
        with open(out_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Image", "Text", "Score", "Box"])
            for row in ocr_texts:
                writer.writerow([img_name] + row)

        # 加入總表
        for row in ocr_texts:
            all_results.append([img_name] + row)

        print(f"完成：{img_name} -> {out_img_path}, {out_csv_path}")

    # 存總表 CSV
    all_csv_path = os.path.join(OUTPUT_DIR, "all_results.csv")
    with open(all_csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Image", "Text", "Score", "Box"])
        writer.writerows(all_results)

    print(f"總表已存：{all_csv_path}")

if __name__ == "__main__":
    main()
