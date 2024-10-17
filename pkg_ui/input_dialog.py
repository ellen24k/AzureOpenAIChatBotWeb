import tkinter as tk

class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("음성인식 실패 시 직접 입력할 수 있습니다.")
        # 부모 창의 크기와 위치를 가져옴
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # InputDialog 창의 크기
        dialog_width = 300
        dialog_height = 100

        # 중앙에 위치하도록 좌표 계산
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)

        # 위치 설정
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        self.label = tk.Label(self, text="3글자를 입력하세요:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)

        self.button = tk.Button(self, text="OK", command=self.on_ok)
        self.button.pack(pady=5)

        self.result = None

    def on_ok(self):
        self.result = self.entry.get()
        self.grab_release()
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result