import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# =======================================================
# ЗАДАЧА 2, 3 и 4: Класс Processor (логика обработки)
# =======================================================
class Processor:
    def __init__(self):
        self.original_img = None
        self.processed_img = None

    def load_image(self, filepath):
        # Загрузка изображения через OpenCV
        self.original_img = cv2.imread(filepath)
        return self.original_img is not None

    def process(self, saturation_threshold):
        if self.original_img is None:
            return None
        
        # Задача 2: Конвертация BGR в HSV
        hsv = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2HSV)
        
        # Задача 3: Разбиваем на каналы (H, S, V)
        h, s, v = cv2.split(hsv)
        
        # Применяем фильтр к каналу насыщенности (S). 
        # THRESH_TOZERO обнуляет значения ниже порога (делает их серыми)
        _, s_filtered = cv2.threshold(s, saturation_threshold, 255, cv2.THRESH_TOZERO)
        
        # Задача 4: Собираем каналы обратно и конвертируем в BGR
        hsv_merged = cv2.merge([h, s_filtered, v])
        self.processed_img = cv2.cvtColor(hsv_merged, cv2.COLOR_HSV2BGR)
        
        return self.processed_img

    def save_image(self, filepath):
        if self.processed_img is not None:
            # Сохранение результата (требование ко всем вариантам)
            cv2.imwrite(filepath, self.processed_img)
            return True
        return False


# =======================================================
# ЗАДАЧА 1: Класс App (GUI и взаимодействие с пользователем)
# =======================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__() # Инициализируем родительский класс окна
        self.title("Фильтрация насыщенности (HSV)")
        self.geometry("800x600")
        
        self.processor = Processor() # Создаем объект нашего обработчика
        
        self.setup_gui()
        
    def setup_gui(self):
        # Панель управления (сверху)
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Кнопки загрузки и сохранения
        btn_load = tk.Button(control_frame, text="Загрузить картинку", command=self.load_image)
        btn_load.pack(side=tk.LEFT, padx=5)
        
        btn_save = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5)
        
        tk.Label(control_frame, text="Мин. уровень насыщенности:").pack(side=tk.LEFT, padx=10)
        
        # Ползунок (Scale) для выбора порога (от 0 до 255)
        self.scale_var = tk.IntVar(value=100)
        self.scale = tk.Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL, 
                              variable=self.scale_var, command=self.on_scale_change)
        self.scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Создание вкладок (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab_orig = ttk.Frame(self.notebook)
        self.tab_proc = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_orig, text="Оригинал")
        self.notebook.add(self.tab_proc, text="Результат обработки")
        
        # Метки (Label) для отображения картинок на вкладках
        self.lbl_orig = tk.Label(self.tab_orig)
        self.lbl_orig.pack(fill=tk.BOTH, expand=True)
        
        self.lbl_proc = tk.Label(self.tab_proc)
        self.lbl_proc.pack(fill=tk.BOTH, expand=True)
        
    def load_image(self):
        # Диалог выбора файла
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if filepath:
            if self.processor.load_image(filepath):
                self.show_image(self.processor.original_img, self.lbl_orig)
                self.process_image() # Сразу обрабатываем по текущему ползунку
                
    def on_scale_change(self, val):
        # Этот метод срабатывает каждый раз при движении ползунка
        self.process_image()
        
    def process_image(self):
        if self.processor.original_img is not None:
            threshold = self.scale_var.get()
            res_img = self.processor.process(threshold)
            self.show_image(res_img, self.lbl_proc)
            
    def show_image(self, cv_img, label):
        # Чтобы показать картинку из OpenCV в Tkinter, её нужно конвертировать
        # из BGR (формат OpenCV) в RGB (формат PIL)
        img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Слегка уменьшаем картинку, чтобы она точно влезла в окно
        pil_img.thumbnail((750, 480))
        
        tk_img = ImageTk.PhotoImage(image=pil_img)
        label.config(image=tk_img)
        label.image = tk_img # Сохраняем ссылку в памяти
        
    def save_image(self):
        if self.processor.processed_img is not None:
            filepath = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                                    filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if filepath:
                self.processor.save_image(filepath)
                messagebox.showinfo("Успех", "Изображение успешно сохранено!")

# Точка входа в программу
if __name__ == "__main__":
    app = App()
    app.mainloop()