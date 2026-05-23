import customtkinter as ctk
from tkinter import filedialog
import datetime

# 基本的な見た目の設定
ctk.set_appearance_mode("System")  # OSの設定に合わせる（Dark/Light）
ctk.set_default_color_theme("blue")  # テーマカラー

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定
        self.title("イラスト継続トラッカー")
        self.geometry("400x300")

        # タイトルラベル
        self.label_title = ctk.CTkLabel(self, text="今日のイラストをアップロードしよう！", font=("Meiryo", 16))
        self.label_title.pack(pady=20)

        # 連続日数の表示（今は仮で0日）
        self.label_streak = ctk.CTkLabel(self, text="🔥 連続日数: 0 日", font=("Meiryo", 24, "bold"))
        self.label_streak.pack(pady=20)

        # アップロードボタン
        self.btn_upload = ctk.CTkButton(self, text="画像を選択", command=self.upload_image)
        self.btn_upload.pack(pady=20)

    def upload_image(self):
        # ファイル選択ダイアログを開く
        file_path = filedialog.askopenfilename(
            title="イラストを選択",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        # 画像が選択された場合の処理
        if file_path:
            print(f"選択されたファイル: {file_path}")
            
            # TODO: ここに「画像を保存フォルダにコピーする」処理を追加する
            # TODO: ここに「日付をチェックして連続日数を増やす」処理を追加する
            
            # 動作確認のため、仮で表示を1日に更新してみる
            self.label_streak.configure(text="🔥 連続日数: 1 日 (アップロード成功!)")

if __name__ == "__main__":
    app = App()
    app.mainloop()