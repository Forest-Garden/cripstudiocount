import customtkinter as ctk
from tkinter import filedialog, messagebox
import datetime
import json
import os
import shutil
from PIL import Image
import winsound

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = "data.json"
SAVE_DIR = "Illustrations"
SOUND_FILE = os.path.join(BASE_DIR, "success.wav")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("イラスト継続トラッカー")
        self.geometry("500x600")

        self.streak_data = self.load_data()

        self.label_title = ctk.CTkLabel(self, text="今日のイラストをアップロードしよう！", font=("Meiryo", 16))
        self.label_title.pack(pady=10)

        current_streak = self.streak_data["streak_count"]
        self.label_streak = ctk.CTkLabel(self, text=f"🔥 連続日数: {current_streak} 日", font=("Meiryo", 24, "bold"))
        self.label_streak.pack(pady=10)

        self.btn_upload = ctk.CTkButton(self, text="画像を選択", command=self.upload_image)
        self.btn_upload.pack(pady=10)

        self.label_image = ctk.CTkLabel(self, text="ここにイラストが表示されます", width=300, height=300)
        self.label_image.pack(pady=20)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {"last_upload_date": None, "streak_count": 0}

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.streak_data, f, indent=4)

    # ====== 【変更】Windows標準機能を使った音声再生 ======
    def play_sound(self):
        if os.path.exists(SOUND_FILE):
            # SND_ASYNC をつけることで、音が鳴っている間も画面がフリーズしません
            winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            print(f"※{SOUND_FILE}が見つからないため、音は再生されません")

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="イラストを選択",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        if file_path:
            # 1. 画像の保存
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)

            original_filename = os.path.basename(file_path)
            now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{now_str}_{original_filename}"
            destination_path = os.path.join(SAVE_DIR, new_filename)
            shutil.copy2(file_path, destination_path)

            # 2. 画像の表示
            pil_image = Image.open(destination_path)
            pil_image.thumbnail((300, 300)) 
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
            self.label_image.configure(image=ctk_image, text="")
            
            # 3. 日数の計算
            today = datetime.date.today()
            today_str = str(today)
            last_date_str = self.streak_data["last_upload_date"]

            is_streak_updated = False

            if last_date_str == today_str:
                message = "今日の追加イラストを保存しました！\n"
            else:
                if last_date_str:
                    last_date = datetime.date.fromisoformat(last_date_str)
                    if (today - last_date).days == 1:
                        self.streak_data["streak_count"] += 1
                        message = "連続記録更新！素晴らしい！"
                    else:
                        self.streak_data["streak_count"] = 1
                        message = "新たな連続記録の始まりです！"
                else:
                    self.streak_data["streak_count"] = 1
                    message = "初回のアップロード完了！\n明日も頑張りましょう！"
                
                self.streak_data["last_upload_date"] = today_str
                self.save_data()
                is_streak_updated = True

            # 画面の表示更新
            new_streak = self.streak_data["streak_count"]
            self.label_streak.configure(text=f"🔥 連続日数: {new_streak} 日")

            # 4. 音の再生とメッセージの表示
            self.play_sound()
            
            if is_streak_updated:
                messagebox.showinfo("大成功！", message)
            else:
                messagebox.showinfo("保存完了", message)

if __name__ == "__main__":
    app = App()
    app.mainloop()