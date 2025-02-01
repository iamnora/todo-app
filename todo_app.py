import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import sys
import os
import random
import math

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Sevimli To-Do List ✨")
        self.root.geometry("600x700")
        # Pembe gradient arka plan
        self.root.configure(bg="#ffd1dc")  # Açık pembe

        # Veritabanı bağlantısı
        self.conn = sqlite3.connect('todo.db')
        self.create_table()

        # Canvas oluştur - gradient efekti için
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)
        
        # Gradient arka plan oluştur
        self.create_gradient("#ffb6c1", "#ffd1dc")  # Koyu pembeden açık pembeye

        # Bulutlar ve ışıltılar için listeler
        self.clouds = []
        self.sparkles = []
        
        # Bulutları oluştur - sayıyı ve konumları güncelle
        for _ in range(5):  # 3'ten 5'e çıkardık
            x = random.randint(-100, 600)  # Başlangıç pozisyonlarını genişlettik
            y = random.randint(20, 200)    # Daha geniş dikey dağılım
            self.create_cloud(x, y)

        # Işıltıları oluştur - sayıyı ve dağılımı artıralım
        for _ in range(30):  # 15'ten 30'a çıkardık
            x = random.randint(0, 600)
            y = random.randint(0, 700)
            self.create_sparkle(x, y)
            
        # Yıldızları ekle
        self.stars = []
        for _ in range(20):
            x = random.randint(0, 600)
            y = random.randint(0, 700)
            self.create_star(x, y)

        # Ana container - pembe tonlarında
        self.main_frame = ttk.Frame(root, style="Card.TFrame")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Stil tanımlamaları
        style = ttk.Style()
        style.configure("Card.TFrame", 
                       background="#ffffff",
                       borderwidth=2,
                       relief="solid")
        style.configure("Modern.TEntry", 
                       padding=15,
                       fieldbackground="#fff5f7",
                       borderwidth=0)

        # Container için arka plan ve gölge efekti
        container_frame = tk.Frame(
            self.main_frame,
            bg="white",
            padx=30,
            pady=30,
            highlightbackground="#ffb6c1",
            highlightthickness=1
        )
        container_frame.pack(padx=20, pady=20)
        
        # Container'a hafif gölge efekti
        self.add_shadow(container_frame)
        
        # Başlık
        title_frame = tk.Frame(container_frame, bg="white")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="✨ Yapılacaklar Listem ✨",
            font=("Helvetica", 24, "bold"),
            fg="#ff69b4",  # Canlı pembe
            bg="white"
        )
        title_label.pack()

        # Giriş alanı
        self.input_frame = tk.Frame(container_frame, bg="white")
        self.input_frame.pack(fill=tk.X, pady=20)

        self.task_entry = tk.Entry(
            self.input_frame,
            font=("Helvetica", 14),
            bg="#fff5f7",  # Çok açık pembe
            fg="#333333",
            relief=tk.FLAT,
            insertbackground="#ff69b4"
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Entry altındaki çizgi
        self.canvas.create_line(
            self.task_entry.winfo_x(),
            self.task_entry.winfo_y() + self.task_entry.winfo_height(),
            self.task_entry.winfo_x() + self.task_entry.winfo_width(),
            self.task_entry.winfo_y() + self.task_entry.winfo_height(),
            fill="#ff69b4",
            width=2
        )

        self.add_button = tk.Button(
            self.input_frame,
            text="Ekle 🌸",
            command=self.add_task,
            font=("Helvetica", 12),
            bg="#ff69b4",  # Canlı pembe
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.add_button.pack(side=tk.RIGHT)

        # Görev listesi
        self.task_frame = tk.Frame(container_frame, bg="white")
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Görev listesi
        self.task_listbox = tk.Listbox(
            self.task_frame,
            font=("Helvetica", 12),
            selectmode=tk.SINGLE,
            bg="white",
            fg="#333333",
            selectbackground="#e2b6ff",  # Açık mor seçim
            selectforeground="#333333",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#ffb6c1",
            yscrollcommand=self.scrollbar.set
        )
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Butonlar
        self.button_frame = tk.Frame(container_frame, bg="white")
        self.button_frame.pack(fill=tk.X, pady=20)

        button_style = {
            "font": ("Helvetica", 12),
            "bg": "#ff69b4",  # Canlı pembe
            "fg": "white",
            "relief": tk.FLAT,
            "padx": 15,
            "pady": 8,
            "cursor": "hand2"
        }

        self.complete_button = tk.Button(
            self.button_frame,
            text="Tamamlandı ✓",
            command=self.toggle_complete,
            **button_style
        )
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(
            self.button_frame,
            text="Sil 🗑️",
            command=self.delete_task,
            **button_style
        )
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Enter tuşu ile görev ekleme
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        # Animasyonları başlat
        self.animate_clouds()
        self.animate_sparkles()
        self.animate_stars()  # Yeni animasyon

        # Görevleri yükle
        self.load_tasks()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        for task in cursor.fetchall():
            prefix = "✓ " if task[2] else "□ "
            self.task_listbox.insert(tk.END, prefix + task[1])

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO tasks (text) VALUES (?)', (task_text,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()

    def toggle_complete(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task_text = self.task_listbox.get(index)[2:]  # Remove prefix
            cursor = self.conn.cursor()
            cursor.execute('SELECT completed FROM tasks WHERE text = ?', (task_text,))
            current_status = cursor.fetchone()[0]
            cursor.execute('UPDATE tasks SET completed = ? WHERE text = ?',
                         (not current_status, task_text))
            self.conn.commit()
            self.load_tasks()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task_text = self.task_listbox.get(index)[2:]  # Remove prefix
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE text = ?', (task_text,))
            self.conn.commit()
            self.load_tasks()

    def create_cloud(self, x, y):
        cloud = {
            'x': x,
            'y': y,
            'shapes': []
        }
        
        # Bulut şeklini daha belirgin yap
        cloud_color = "#ff69b4"  # Canlı pembe bulutlar
        sizes = [(40, 30), (50, 40), (45, 35)]
        
        for i, (width, height) in enumerate(sizes):
            shape = self.canvas.create_oval(
                x + i*25, y,
                x + width + i*25, y + height,
                fill=cloud_color,
                outline=cloud_color,
                width=2
            )
            cloud['shapes'].append(shape)
        
        # Ekstra detay için küçük daireler
        for i in range(2):
            small_shape = self.canvas.create_oval(
                x + 15 + i*30, y - 10,
                x + 35 + i*30, y + 15,
                fill=cloud_color,
                outline=cloud_color,
                width=2
            )
            cloud['shapes'].append(small_shape)
        
        self.clouds.append(cloud)

    def create_star(self, x, y):
        size = random.uniform(5, 15)
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            r = size if i % 2 == 0 else size * 0.4
            points.extend([
                x + r * math.cos(angle),
                y + r * math.sin(angle)
            ])
        
        star = {
            'x': x,
            'y': y,
            'angle': random.uniform(0, 2*math.pi),
            'scale': random.uniform(0.5, 1.0),
            'speed': random.uniform(0.01, 0.03),
            'size': size,
            'shape': self.canvas.create_polygon(
                points,
                fill="#ff69b4",  # Pembe yıldızlar
                outline="",
                smooth=True
            )
        }
        self.stars.append(star)

    def create_sparkle(self, x, y):
        sparkle = {
            'x': x,
            'y': y,
            'angle': random.uniform(0, 2*math.pi),
            'scale': random.uniform(0.5, 1.0),
            'speed': random.uniform(0.02, 0.05),
            'color': random.choice(["#ff69b4", "#ff8da1", "#ffb6c1"])  # Pembe tonları
        }
        
        size = random.uniform(3, 8)  # Farklı boyutlarda ışıltılar
        points = [
            x, y-size,
            x+size, y,
            x, y+size,
            x-size, y
        ]
        
        shape = self.canvas.create_polygon(
            points,
            fill=sparkle['color'],
            outline=""
        )
        
        sparkle['shape'] = shape
        self.sparkles.append(sparkle)

    def animate_clouds(self):
        for cloud in self.clouds:
            # Daha yavaş hareket
            cloud['x'] += 0.5
            if cloud['x'] > 700:  # Ekran dışına çıkınca
                cloud['x'] = -150  # Daha soldan başlat
                cloud['y'] = random.randint(20, 200)  # Yeni rastgele yükseklik
            
            for shape in cloud['shapes']:
                self.canvas.move(shape, 0.5, 0)  # Daha yavaş hareket
        
        self.root.after(40, self.animate_clouds)  # Daha sık güncelleme

    def animate_sparkles(self):
        for sparkle in self.sparkles:
            sparkle['angle'] += sparkle['speed']
            scale = abs(math.sin(sparkle['angle'])) * sparkle['scale']
            
            size = 5 * scale
            points = [
                sparkle['x'], sparkle['y']-size,
                sparkle['x']+size, sparkle['y'],
                sparkle['x'], sparkle['y']+size,
                sparkle['x']-size, sparkle['y']
            ]
            
            self.canvas.coords(sparkle['shape'], points)
            
            # Renk geçişi efekti
            brightness = 155 + int(100 * scale)
            self.canvas.itemconfig(
                sparkle['shape'],
                fill=sparkle['color']
            )
        
        self.root.after(40, self.animate_sparkles)  # Biraz daha hızlı animasyon

    def animate_stars(self):
        for star in self.stars:
            star['angle'] += star['speed']
            scale = abs(math.sin(star['angle'])) * star['scale']
            
            points = []
            for i in range(10):
                angle = i * math.pi / 5 + star['angle']
                r = star['size'] * scale if i % 2 == 0 else star['size'] * 0.4 * scale
                points.extend([
                    star['x'] + r * math.cos(angle),
                    star['y'] + r * math.sin(angle)
                ])
            
            self.canvas.coords(star['shape'], points)
            
            # Parlaklık efekti
            brightness = 155 + int(100 * scale)
            self.canvas.itemconfig(
                star['shape'],
                fill=f"#{brightness:02x}{int(brightness*0.4):02x}{int(brightness*0.7):02x}"
            )
        
        self.root.after(40, self.animate_stars)

    def create_gradient(self, color1, color2):
        """Gradient arka plan oluştur"""
        height = 700
        width = 600
        
        for i in range(height):
            # Renk interpolasyonu
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            ratio = i / height
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def add_shadow(self, widget):
        """Widget'a gölge efekti ekle"""
        shadow = tk.Frame(widget.master)
        shadow.configure(bg='#e0e0e0')  # Gölge rengi
        shadow.place(x=widget.winfo_x()+2, y=widget.winfo_y()+2, 
                    width=widget.winfo_width(), height=widget.winfo_height())
        widget.lift()  # Widget'ı gölgenin üzerine getir

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop() 