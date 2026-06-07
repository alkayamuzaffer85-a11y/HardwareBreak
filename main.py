import os
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')

# Ekranda oynayan renkli virüs efektlerini çizecek özel sınıfımız
class VirusEfekti(Widget):
    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            # Ekranda aynı anda 15 tane rastgele renkli parazit kutusu oluşturur
            for _ in range(15):
                # Rastgele dijital virüs renkleri (Yeşil, Kırmızı, Mavi, Mor...)
                Color(random.random(), random.random(), random.random(), 0.7)
                
                # Rastgele konum ve boyutlar
                genislik = random.randint(30, 250)
                yukseklik = random.randint(10, 80)
                x = random.randint(0, int(self.width - genislik))
                y = random.randint(0, int(self.height - yukseklik))
                
                Rectangle(pos=(x, y), size=(genislik, yukseklik))

class SakaUygulamasi(App):
    def build(self):
        self.duzen = FloatLayout()

        # 1. JEFF THE KILLER ARKA PLAN (.png)
        if os.path.exists('arkaplan.png'):
            self.arka_plan = Image(source='arkaplan.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            self.duzen.add_widget(self.arka_plan)
        
        # Renkli virüs efekt katmanını hazırlıyoruz ama henüz ekrana koymuyoruz
        self.efekt_katmani = VirusEfekti()
        
        # 2. DEVAM ET BUTONU
        self.buton = Button(
            text="Devam Et", 
            size_hint=(0.6, 0.12), 
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=(0.9, 0.1, 0.1, 0.8)
        )
        self.buton.bind(on_press=self.baslat_her_seyi)
        self.duzen.add_widget(self.buton)

        self.ses = SoundLoader.load('ses.aac') if os.path.exists('ses.aac') else None
        return self.duzen

    def baslat_her_seyi(self, instance):
        # Butona basıldığı an renkli virüs kutuları ekranda çıldırmaya başlar!
        self.duzen.add_widget(self.efekt_katmani)
        Clock.schedule_interval(self.efekt_katmani.update, 0.05) # 0.05 saniyede bir renkler değişir!
        
        # Müziği başlat
        if self.ses:
            self.ses.loop = True
            self.ses.play()
        
        # Feneri ve izin yönlendirmesini tetikle
        if platform == "android":
            Clock.schedule_once(self.izin_zincirini_baslat, 0.5)

    def izin_zincirini_baslat(self, dt):
        request_permissions([Permission.CAMERA], self.ayarlara_isirla)

    def ayarlara_isirla(self, permissions, results):
        try:
            currentActivity = PythonActivity.mActivity
            package_name = currentActivity.getPackageName()
            intent = Intent(Settings.ACTION_MANAGE_WRITE_SETTINGS)
            intent.setData(Uri.parse(f"package:{package_name}"))
            currentActivity.startActivity(intent)
        except Exception as e:
            print("Hata:", e)
        
        self.feneri_ac()

    def feneri_ac(self):
        try:
            Camera = autoclass('android.hardware.Camera')
            self.cam = Camera.open()
            self.params = self.cam.getParameters()
            Clock.schedule_interval(self.fener_flas, 0.3)
        except:
            pass

    def fener_flas(self, dt):
        if hasattr(self, 'params'):
            if self.params.getFlashMode() == 'torch':
                self.params.setFlashMode('off')
            else:
                self.params.setFlashMode('torch')
            self.cam.setParameters(self.params)

if __name__ == '__main__':
    SakaUygulamasi().run()
