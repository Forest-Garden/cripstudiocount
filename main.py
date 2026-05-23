import customtkinter as ctk
from tkinter import filedialog
import datetime
import json
import os

# 保存するファイルの名前
DATA_FILE = "data.json"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("イラスト継続トラッカー")
        self.geometry("400x300")

        # 1. 起動時にデータを読み込む
        self.streak_data = self.load_data()

        self.label_title = ctk.CTkLabel(self, text="今日のイラストをアップロードしよう！", font=("Meiryo", 16))
        self.label_title.pack(pady=20)

        # 2. 読み込んだ日数を画面に表示する
        current_streak = self.streak_data["streak_count"]
        self.label_streak = ctk.CTkLabel(self, text=f"🔥 連続日数: {current_streak} 日", font=("Meiryo", 24, "bold"))
        self.label_streak.pack(pady=20)

        self.btn_upload = ctk.CTkButton(self, text="画像を選択", command=self.upload_image)
        self.btn_upload.pack(pady=20)

    # --- データを読み込む関数 ---
    def load_data(self):
        if os.path.exists(DATA_FILE):
            # ファイルがあれば読み込む
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # ファイルがなければ初期データを返す（まだ1回もアップロードしていない状態）
            return {"last_upload_date": None, "streak_count": 0}

    # --- データを保存する関数 ---
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.streak_data, f, indent=4)

    # --- アップロードボタンが押された時の処理 ---
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="イラストを選択",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        if file_path:
            # TODO: ここに画像を専用フォルダにコピーする処理を後で書く

            # --- 日数の計算処理 ---
            today = datetime.date.today()
            today_str = str(today) # YYYY-MM-DDの文字列にする
            last_date_str = self.streak_data["last_upload_date"]

            if last_date_str == today_str:
                # 今日すでにアップロード済みの場合は日数を増やさない
                print("今日はすでにアップロード済みです！")
            else:
                if last_date_str:
                    # 前回のアップロード日を文字列から日付データに戻す
                    last_date = datetime.date.fromisoformat(last_date_str)
                    
                    # 今日の日付と前回の日付の差を計算する
                    if (today - last_date).days == 1:
                        # 差が1日（昨日アップロードしている）なら連続日数を+1
                        self.streak_data["streak_count"] += 1
                    else:
                        # 2日以上空いてしまったら1日にリセット
                        self.streak_data["streak_count"] = 1
                else:
                    # 初めてのアップロードの場合
                    self.streak_data["streak_count"] = 1
                
                # 最終アップロード日を今日に更新して保存
                self.streak_data["last_upload_date"] = today_str
                self.save_data()

            # 画面の表示を更新
            new_streak = self.streak_data["streak_count"]
            self.label_streak.configure(text=f"🔥 連続日数: {new_streak} 日")

if __name__ == "__main__":
    app = App()
    app.mainloop()