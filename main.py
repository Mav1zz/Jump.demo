# Code'un %65'i kendim %35'i ise Yapay Zeka ile yapıldı.
# (Matematik konularında yardım almuş olabilirim. sorgulama ._.)

# Oyun, zıplayarak platformlardan kaçmayı ve bonusları toplamayı amaçlıyor.
# hehe :D

import pygame
import sys
import time
import random

# Pygame'i başlat.
pygame.init()
pygame.mixer.init()

# Oyun ana ayarları.
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
WIDTH, HEIGHT = screen_size[0], screen_size[1]
screen = pygame.display.set_mode(screen_size)
icon = pygame.image.load("assets/sprites/game_icon.png")
pygame.display.set_caption('Jump.demo')
pygame.display.set_icon(icon)

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Ana menüdeki skin boyutları
menu_skin_size = (60, 60)  # Ana menüdeki skin boyutu
game_skin_size = (40, 40)  # Oyundaki skin boyutu

# Font oluştur
font = pygame.font.Font("assets/fonts/main.ttf", 28)
font_start = pygame.font.Font("assets/fonts/main.ttf", 56)

# Skin'leri yükle
skins = [
    pygame.transform.scale(pygame.image.load(f"assets/sprites/skins/skin{i}.png"), menu_skin_size) for i in range(1, 5)
]

# Oyundaki skin'leri yükle
game_skins = [
    pygame.transform.scale(pygame.image.load(f"assets/sprites/skins/skin{i}.png"), game_skin_size) for i in range(1, 5)
]

current_skin_index = 0  # Başlangıçta ilk skin
current_skin = game_skins[current_skin_index]

# Ses seviyesi
volume_level = 0.5  # Başlangıç ses seviyesi (0.0 ile 1.0 arasında)
volume_steps = 5  # Ses seviyesi kademeleri
volume_icon_y = -60  # Ses seviyesi ikonunun başlangıç y koordinatı
volume_icon_target_y = 10  # Ses seviyesi ikonunun hedef y koordinatı
volume_icon_speed = 5  # Ses seviyesi ikonunun kayma hızı
volume_icon_display_time = 2000  # Ses seviyesi ikonunun ekranda kalma süresi (milisaniye)
last_volume_change_time = 0  # Son ses değişikliği zamanı

# Ses seviyesi ikonlarını yükle
volume_icons = [
    pygame.image.load(f"assets/sprites/volume/volume_{i}.png") for i in range(volume_steps + 1)
]

# Ulti barı için değişkenler
ulti_level = 0 # şuanki ulti leveli (başlangıç)
ulti_max_level = 5 # Ultinin maksimum leveli (5)
ulti_active = False # ulti aktifmi ?
ulti_duration = 15000  # 15 saniye
ulti_start_time = 0 # ulti açıldımı kalan süre

# Ulti barı ikonlarını yükle
ulti_icons = [
    pygame.image.load(f"assets/sprites/ulti/frame{i}.png") for i in range(ulti_max_level + 1)
]

# Ses seviyesini güncelleme fonksiyonu
def update_volume(change):
    global volume_level, last_volume_change_time
    volume_level = max(0.0, min(1.0, volume_level + change / volume_steps))
    pygame.mixer.music.set_volume(volume_level)
    last_volume_change_time = pygame.time.get_ticks()

# Ses seviyesi ikonunu güncelleme fonksiyonu
def update_volume_icon():
    global volume_icon_y, last_volume_change_time
    current_time = pygame.time.get_ticks()
    if current_time - last_volume_change_time < volume_icon_display_time:
        volume_icon_y = min(volume_icon_y + volume_icon_speed, volume_icon_target_y)
    else:
        volume_icon_y = max(volume_icon_y - volume_icon_speed, -60)

def draw_volume_icon():
    update_volume_icon()
    volume_icon_index = int(volume_level * volume_steps)
    volume_icon_index = min(volume_icon_index, volume_steps)  # Sınırlandırma
    screen.blit(volume_icons[volume_icon_index], (10, volume_icon_y))

# Ulti barı güncelleme fonksiyonu
def update_ulti_bar():
    global ulti_level, ulti_active, ulti_start_time
    if ulti_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - ulti_start_time
        if elapsed_time >= ulti_duration:
            ulti_active = False
        else:
            remaining_time = (ulti_duration - elapsed_time) // 1000
            draw_text_with_outline(screen, f"Ultinin bitmesine: {remaining_time}", font, WIDTH - 490, 50, text_color=YELLOW, outline_color=BLACK, outline_thickness=2)

# Ulti barı çizme fonksiyonu
def draw_ulti_bar():
    ulti_icon_index = min(ulti_level, ulti_max_level)
    ulti_icon = pygame.transform.scale(ulti_icons[ulti_icon_index], (204, 46))  # Burada boyutu ayarlayabilirsiniz
    screen.blit(ulti_icon, (WIDTH - 220, 10))

# Outline Yazıyı çizme fonksiyonu
def draw_text_with_outline(surface, text, font, x, y, text_color, outline_color, outline_thickness):
    outline_text = font.render(text, True, outline_color)
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline_text, (x + dx, y + dy))
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (x, y))


# Ölme Ekranı Kodu.
def gameover():
    global score, volume_level, last_volume_change_time, volume_icon_y

    # Resmi yükle
    image = pygame.image.load("assets/sprites/gameover.png")  # Butonun resmi
    rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Butonun pozisyonu

    # Ana döngü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Space tuşuna basılma kontrolü
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                    update_volume(0.1)
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    update_volume(-0.1)

        # Ekranı temizle
        screen.fill(BLACK)

        # Butonu çiz
        screen.blit(image, rect)

        font = pygame.font.Font("assets/fonts/main.ttf", 28)
        draw_text_with_outline(screen, f"* Skorunuz: {score}", font, 10, 50, text_color=WHITE, outline_color=BLACK, outline_thickness=2)

        if running == False:
            sys.exit()

        # Ses seviyesi ikonunu güncelle ve çiz
        draw_volume_icon()

        # Ekranı güncelle
        pygame.display.flip()

    pygame.quit()

# Nasıl Oynanır Kodu.
def how_play():
    global volume_level, last_volume_change_time, volume_icon_y

    # Sesler
    pygame.mixer.music.load("assets/sounds/game.mp3")
    pygame.mixer.music.play(-1)

    # Resimleri yükle
    frame1 = pygame.image.load("assets/sprites/how_to_play/frame1.png")  # Frame 1 resmi
    frame2 = pygame.image.load("assets/sprites/how_to_play/frame2.png")  # Frame 2 resmi (ikinci sayfayı temsil ediyor)
    
    # Resimlerin pozisyonlarını ayarla
    rect1 = frame1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    rect2 = frame2.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Başlangıçta frame1 aktif
    current_frame = 1
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # ESC tuşu kontrolü
                if event.key == pygame.K_ESCAPE:
                    if current_frame == 1:
                        main_menu()  # Ana menüye dön
                    elif current_frame == 2:
                        current_frame = 1  # Frame1'e geri dön
                
                # Sağ ok tuşu kontrolü
                if event.key == pygame.K_RIGHT:
                    if current_frame == 1:
                        current_frame = 2  # Frame2'ye geç
                    elif current_frame == 2:
                        game()  # Oyunu başlat
                
                # Ses kontrolü için mevcut tuşlar
                if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                    update_volume(0.1)
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    update_volume(-0.1)

        # Ekranı temizle
        screen.fill(BLACK)

        # Aktif frame'e göre resmi çiz
        if current_frame == 1:
            screen.blit(frame1, rect1)
        elif current_frame == 2:
            screen.blit(frame2, rect2)

        # Ses seviyesi ikonunu çiz
        draw_volume_icon()

        # Ekranı güncelle
        pygame.display.flip()

    pygame.quit()


# Oyunun Ana Kodu.
def game():
    global score, ulti_level, ulti_active, ulti_start_time

    # Ulti seviyesini sıfırla
    ulti_level = 0
    ulti_active = False

    # Saat nesnesi
    clock = pygame.time.Clock()

    # Karakter
    player_width, player_height = 40, 40
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - 100
    player_speed_x = 0
    player_velocity_y = 0
    gravity = 0.5
    jump_strength = -15
    jump_count = 0  # Aynı platformda zıplama sayacı
    current_platform = None

    # Oyun verileri
    score = 0
    platform_spacing = 100
    platform_width = 100
    platform_types = ["spike", "normal", "bonus"]
    agirliklar = [0.1, 200, 0.001]  # Ağırlıklar, bonus platformları çok nadir çıkacak

    # Resimler.
    normal_texture = pygame.image.load("assets/sprites/normal_platform.png")
    spike_texture = pygame.image.load("assets/sprites/spike_platform.png")
    bonus_texture = pygame.image.load("assets/sprites/ulti_platform.png")
    background_texture = pygame.image.load("assets/sprites/game_Background.png")  # Arkaplan resmi

    # Resimleri ölçekleri.
    normal_texture = pygame.transform.scale(normal_texture, (platform_width, 10))
    spike_texture = pygame.transform.scale(spike_texture, (platform_width, 10))
    bonus_texture = pygame.transform.scale(bonus_texture, (platform_width, 10))
    background_texture = pygame.transform.scale(background_texture, (WIDTH, HEIGHT + 30))

    # Arkaplanın Yukarı Doğru haraket konumları.
    bg_y1 = 0
    bg_y2 = -HEIGHT

    # Platformlar
    platforms = [(WIDTH // 2 - platform_width // 2, HEIGHT - 40, platform_width, 10, "normal")]
    for i in range(1, 8):
        x = random.randint(0, WIDTH - platform_width)
        y = HEIGHT - 40 - (i * platform_spacing)
        platform_type = random.choices(platform_types, weights=agirliklar, k=1)[0]
        platforms.append((x, y, platform_width, 10, platform_type))

    # Oyuncuyu başlangıç platformunun üzerine yerleştir
    player_y = platforms[0][1] - player_height

    # Ana döngü
    running = True

    def countdown(screen, font, width, height):
        for i in range(3, 0, -1):
            for y in range(-300, 0, 10):  # Yukarıdan aşağı düşme efekti
                screen.fill((47, 125, 200))  # Ekranı temizle
                draw_text_with_outline(screen, str(i), font, width // 2 - 10, height // 2 - 20 + y, text_color=WHITE, outline_color=BLACK, outline_thickness=4)
                pygame.display.flip()
                time.sleep(0.01)
            
            time.sleep(0.5)  # Sayı düştükten sonra kısa bekleme süresi
        
        # "Başla!" animasyonu
        for alpha in range(0, 256, 10):  # 0'dan 255'e kadar artarak
            screen.fill((47, 125, 200))
            text_surface = font.render("GOO!", True, (255, 255, 255))
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.01)
        
        time.sleep(0.5)  # Kısa bir bekleme süresi

    countdown(screen, font_start, screen_size[0], screen_size[1])  # Geri sayımı çalıştır

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_0 and ulti_level == ulti_max_level:
                    ulti_active = True
                    ulti_start_time = pygame.time.get_ticks()
                    ulti_level = 0
                if event.key == pygame.K_F10:
                    ulti_level = 5
        
        # Tuş kontrolleri
        keys = pygame.key.get_pressed()
        player_speed_x = -8 if keys[pygame.K_LEFT] else 8 if keys[pygame.K_RIGHT] else 0

        # Fizik: yerçekimi ve yatay hız
        player_velocity_y += gravity
        player_x += player_speed_x
        player_y += player_velocity_y

        # Yanlardan ışınlanma
        if player_x < 0:
            player_x = WIDTH
        if player_x > WIDTH:
            player_x = 0

        # Karakterin platformlarla etkileşimi
        on_platform = False
        for platform in platforms:
            px, py, pw, ph, ptype = platform
            if (
                player_x + player_width > px
                and player_x < px + pw
                and player_y + player_height > py
                and player_y + player_height - player_velocity_y <= py
            ):
                if ptype == "spike" and not ulti_active:
                    gameover()
                elif ptype == "bonus":
                    ulti_level = min(ulti_level + 1, ulti_max_level)
                    on_platform = True
                    current_platform = platform
                    jump_count = 0
                    player_velocity_y = jump_strength
                    player_y = py - player_height
                    platforms.remove(platform)  # Bonus platformu zıplandıktan sonra yok et
                else:
                    on_platform = True
                    if current_platform == platform:
                        jump_count += 1
                        if jump_count >= 5:
                            gameover()
                    else:
                        current_platform = platform
                        jump_count = 0

                    player_velocity_y = jump_strength
                    player_y = py - player_height

                    if ptype == "bonus":
                        platforms.remove(platform)  # Bonus platformu zıplandıktan sonra yok et

        # Eğer platformda değilse, düşüş devam eder
        if not on_platform and player_velocity_y > 0:
            player_velocity_y += gravity

        # Puan sistemi ve hız artışı
        if player_y < HEIGHT // 2:
            score += 1
            move_y = abs(player_velocity_y)
            player_y += move_y

            # Arkaplanı hareket ettir
            bg_y1 += move_y
            bg_y2 += move_y

            # Arkaplan döngüsü
            if bg_y1 >= HEIGHT:
                bg_y1 = -HEIGHT
            if bg_y2 >= HEIGHT:
                bg_y2 = -HEIGHT

            # Platformları aşağı kaydır
            platforms = [(x, y + move_y, w, h, t) for x, y, w, h, t in platforms]

            # Platformları kontrol et ve eksikse yedek platform oluştur
            platforms = [p for p in platforms if p[1] < HEIGHT]
            while len(platforms) < 5:
                prev_x, prev_y, _, _, prev_type = platforms[-1]
                new_x = random.randint(max(0, prev_x - 100), min(WIDTH - platform_width, prev_x + 100))
                new_y = prev_y - platform_spacing

                mevcut_spike_var = any(p[4] == "spike" for p in platforms)
                new_type = "normal" if mevcut_spike_var else random.choice(platform_types)

                if new_type == "bonus":
                    new_x = WIDTH - new_x - platform_width  # Bonus platformları ters yönde doğar

                if prev_type == "spike":
                    new_x = prev_x + platform_width if new_x < prev_x else prev_x - platform_width

                # Platformların ekranın dışına taşmasını önle
                new_x = max(0, min(new_x, WIDTH - platform_width))

                platforms.append((new_x, new_y, platform_width, 10, new_type))

        # Düşme kontrolü
        if player_y > HEIGHT:
            if ulti_active:
                player_y = HEIGHT // 2
                player_velocity_y = jump_strength
            else:
                gameover()

        # Ekranı temizle
        screen.fill(WHITE)

        # Arkaplanı çiz
        screen.blit(background_texture, (0, bg_y1))
        screen.blit(background_texture, (0, bg_y2))

        # Platformları çiz
        for platform in platforms:
            x, y, w, h, ptype = platform
            texture = normal_texture if ptype == "normal" else spike_texture if ptype == "spike" else bonus_texture
            screen.blit(texture, (x, y))

        # Karakteri çiz
        screen.blit(current_skin, (player_x, player_y))

        draw_text_with_outline(screen, f"* Skor: {score}", font, 10, 10, text_color=WHITE, outline_color=BLACK, outline_thickness=2)

        # Ulti barı güncelle ve çiz
        update_ulti_bar()
        draw_ulti_bar()

        # Ekranı güncelle
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# EasterEggs
def secret_code():
    global volume_level, last_volume_change_time, volume_icon_y

    # Sesler ve resimler
    pygame.mixer.music.load("assets/sounds/secret.mp3")
    pygame.mixer.music.play(-1)

    # Resmi yükle
    image = pygame.image.load("assets/sprites/secret_c.png")  # Butonun resmi
    rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Butonun pozisyonu

    # Ana döngü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Space tuşuna basılma kontrolü
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                    update_volume(0.1)
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    update_volume(-0.1)

        # Ekranı temizle
        screen.fill(BLACK)

        # Butonu çiz
        screen.blit(image, rect)

        if running == False:
            sys.exit()

        # Ses seviyesi ikonunu güncelle ve çiz
        draw_volume_icon()

        # Ekranı güncelle
        pygame.display.flip()

    pygame.quit()

# Yapımcı kısmı
def credits():
    global score, volume_level, last_volume_change_time, volume_icon_y

    font = pygame.font.Font("assets/fonts/main.ttf", 18)

    # Sesler ve resimler
    pygame.mixer.music.load("assets/sounds/credits.mp3")
    pygame.mixer.music.play(-1)

    # Geri Button Resmini yükle
    button_image = pygame.image.load("assets/sprites/back.png")  # Butonun resmi
    button_rect = button_image.get_rect(center=(40, 40))  # Butonun pozisyonu

    # Metin
    text = "Indie Cross Theme - Slowed + Reverb"
    text_color = (255, 211, 173)  # Yazı rengi
    outline_color = (137, 86, 84)  # Dış çizgi rengi

    # Metin yüzeyi
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)
    text_width = text_surface.get_width()

    # Animasyon karelerini yükle
    frame1 = pygame.image.load("assets/sprites/credits/frame1.png").convert_alpha()
    frame2 = pygame.image.load("assets/sprites/credits/frame2.png").convert_alpha()
    frame3 = pygame.image.load("assets/sprites/credits/frame3.png").convert_alpha()
    frames = [frame1, frame2, frame3]

    # Animasyon değişkenleri
    current_frame = 0
    animation_speed = 0.2  # Saniye cinsinden kare değişim süresi
    last_animation_time = time.time()  # Son kare değişim zamanı

    # Saat
    clock = pygame.time.Clock()

    # Başlangıç pozisyonları
    x = 280 # Metin pencerenin sağ dışından başlayacak
    y = 365  # Metnin üst pozisyonu (alanın merkezine yakın)

    # Kayma hızı
    speed = 0.5

    # Belirli alan (kayma için)
    clip_rect = pygame.Rect(x, y - 10, 190, 40)  # (x, y, genişlik, yükseklik)
    # Görünmez tıklanabilir dikdörtgen

    invisible_rect = pygame.Rect(120, HEIGHT // 1.29, 60, 80)

    # Ana döngü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                    update_volume(0.1)
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    update_volume(-0.1)
            # Fare tıklaması
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_x, mouse_y):
                    main_menu()
                # Görünmez dikdörtgeni tıklanabilir yap
                if invisible_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:  # Sol fare tuşuna basıldıysa
                        secret_code()

        # Şimdiki zamanı al
        current_time = time.time()

        # Eğer animasyon zamanı geldiyse kareyi değiştir
        if current_time - last_animation_time > animation_speed:
            current_frame = (current_frame + 1) % len(frames)  # Bir sonraki kareye geç
            last_animation_time = current_time  # Zamanı güncelle

        # Animasyon karesini ekrana çiz
        screen.blit(frames[current_frame], (0, 0))

        # Dikdörtgen alanı çiz (alanı görselleştirmek için)
        pygame.draw.rect(screen, WHITE, clip_rect, 1)  # Kenarlıklı dikdörtgen

        # Çizim yapılacak alanı sınırla
        screen.set_clip(clip_rect)

        # Metne outline eklemek için çevresine farklı renkle çiz
        for offset in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(outline_surface, (x + offset[0], y + offset[1]))

        # Asıl metni merkezde çiz
        screen.blit(text_surface, (x, y))

        # Clip sınırını kaldır
        screen.set_clip(None)

        # Metin pozisyonunu güncelle
        x -= speed  # Sola doğru kaydır

        # Eğer metin ekranın tamamen dışına çıkarsa, başa döndür
        if x < clip_rect.x - text_width:
            x = clip_rect.x + clip_rect.width

        # Butonu çiz
        screen.blit(button_image, button_rect)

        # Ses seviyesi ikonunu güncelle ve çiz
        draw_volume_icon()

        if running == False:
            sys.exit()

        # Ekranı güncelle
        pygame.display.flip()

        # FPS sınırını belirle (sadece diğer işlemler için)
        clock.tick(60)

    # Pygame'i kapat
    pygame.quit()

def main_menu():
    global current_skin_index, current_skin, volume_level
    # Sesler ve resimler
    music2 = pygame.mixer.Sound("assets/sounds/intro.mp3")  # İkinci müzik (efekt veya ikinci müzik)
    music2.play(0)

    pygame.mixer.music.load("assets/sounds/main-menu.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume_level)

    # Menü resmi
    menu_image = pygame.transform.scale(pygame.image.load("assets/sprites/custom_select.png"), (450, 344))
    # Buton resimlerini yükle
    menu_close_image = pygame.transform.scale(pygame.image.load("assets/sprites/menu_close.png"), (56, 56))

    # Menü durumu
    menu_open = False
    menu_y = -422  # Menü başlangıç pozisyonu
    overlay_alpha = 0  # Karartma seviyesi (başlangıçta görünmez)

    # Arka plan resmi
    background = pygame.image.load("assets/sprites/Background.png").convert()
    background_width = background.get_width()
    scroll_x = 0

    # Diğer resimler ve müzikler
    credits_image = pygame.image.load("assets/sprites/credits.png")
    logo_image = pygame.image.load("assets/sprites/logo.png").convert_alpha()
    button1_frames = [pygame.image.load(f"assets/sprites/buttons/button1_frame{i}.png").convert_alpha() for i in range(1, 6)]
    button2_frames = [pygame.image.load(f"assets/sprites/buttons/button2_frame{i}.png").convert_alpha() for i in range(1, 6)]
    easter_egg_image = pygame.image.load("assets/sprites/easter-egg.png").convert_alpha()
    easter_egg_image2 = pygame.image.load("assets/sprites/easter-egg2.png").convert_alpha()
    easter_egg_sound = pygame.mixer.Sound("assets/sounds/easteregg1.mp3")
    easter_egg_sound2 = pygame.mixer.Sound("assets/sounds/easteregg2.mp3")
    skins_image = pygame.image.load("assets/sprites/custom.png")

    # Intro gif animasyonu
    intro_frames = [pygame.image.load(f"assets/sprites/intro/frame_{i}.png").convert_alpha() for i in range(1, 20 + 1)]
    intro_frame_index = 0
    intro_frame_duration = 0.1  # Her kare için süre (saniye)
    intro_start_time = time.time()
    intro_alpha = 255
    fade_out_speed = 1

    # Nesne konumları ve boyutları
    logo_rect = logo_image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    button1_rect = button1_frames[0].get_rect(topleft=(screen_size[0] // 2 - 110, 380))
    button2_rect = button2_frames[0].get_rect(topleft=(screen_size[0] // 2 - 110, 450))
    easter_egg_rect = easter_egg_image.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    easter_egg2_rect = easter_egg_image2.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
    easter_egg_button_rect = pygame.Rect(0, 0, 40, 40)  # Sağ üst köşede küçük bir buton
    easter_egg_button2_rect = pygame.Rect(screen_size[0] - 40, 0, 40, 40)  # Sağ üst köşede küçük bir buton
    skins_rect = skins_image.get_rect(center=(60, HEIGHT - 45))
    credits_rect = credits_image.get_rect(center=(WIDTH - 70, HEIGHT - 60))
    close_button_rect = pygame.Rect(screen_size[0] - 120, menu_y + 30, 100, 50)

    # Animasyon ve alfa değerleri
    button1_current_frame = 0
    button2_current_frame = 0
    button1_alpha = 0
    button2_alpha = 0
    easter_egg_alpha = 0
    easter_egg2_alpha = 255
    animation_speed = 0.3
    fade_in_speed = 1

    # Custom Buton Büyütme faktörleri
    scale_factor = 1.2
    current_scale = 1.0
    target_scale = 1.0
    scale_speed = 0.1  # Büyüme hızı
    scale2_factor = 1.1
    current2_scale = 1.0
    target2_scale = 1.0

    # Clock objeleri
    clock = pygame.time.Clock()

    # Buttonların Son animasyon zamanını kaydet
    last_animation_time = time.time()

    # Oyun döngüsü
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                action = key_actions.get(event.key)
                if action:
                    action()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button1_rect.collidepoint(event.pos):
                    how_play()
                elif credits_rect.collidepoint(mouse_x, mouse_y):
                    credits()
                elif button2_rect.collidepoint(event.pos):
                    sys.exit()
                elif easter_egg_button_rect.collidepoint(event.pos):
                    easter_egg_alpha = 255  # Easter egg'i göster
                    easter_egg_sound.play()
                elif easter_egg_button2_rect.collidepoint(event.pos):
                    easter_egg2_alpha = 255  # 2.ci Easter egg'i göster
                    easter_egg_sound2.play()
                elif skins_rect.collidepoint(event.pos):
                    menu_open = not menu_open  # Menü durumunu değiştir

                if menu_open:
                    # Skin seçimi
                    for i, skin in enumerate(skins):
                        skin_rect = skin.get_rect(center=(85 + i * 110, menu_y + 185))
                        if skin_rect.collidepoint(mouse_pos):
                            current_skin_index = i
                            current_skin = game_skins[current_skin_index]  # Seçilen skin'i güncelle
                    # Menü kapatma
                    if close_button_rect.collidepoint(mouse_pos):
                        menu_open = False

        # Menü animasyonu
        if menu_open:
            if menu_y < 0:
                menu_y += 10  # Menü aşağı kaydır
            if overlay_alpha < 150:
                overlay_alpha += 5  # Karartmayı artır
        else:
            if menu_y > -422:
                menu_y -= 10  # Menü yukarı kaydır
            if overlay_alpha > 0:
                overlay_alpha -= 5  # Karartmayı azalt

        # Fare pozisyonunu al
        mouse_pos = pygame.mouse.get_pos()

        # Resmin üzerine gelinip gelinmediğini kontrol et
        if skins_rect.collidepoint(mouse_pos):
            target_scale = scale_factor
        else:
            target_scale = 1.0

        # Mevcut ölçeği hedef ölçeğe doğru güncelle
        if current_scale < target_scale:
            current_scale += scale_speed
            if current_scale > target_scale:
                current_scale = target_scale
        elif current_scale > target_scale:
            current_scale -= scale_speed
            if current_scale < target_scale:
                current_scale = target_scale

        # Resmin üzerine gelinip gelinmediğini kontrol et
        if credits_rect.collidepoint(mouse_pos):
            target2_scale = scale2_factor
        else:
            target2_scale = 1.0

        # Mevcut ölçeği hedef ölçeğe doğru güncelle
        if current2_scale < target2_scale:
            current2_scale += scale_speed
            if current2_scale > target2_scale:
                current2_scale = target2_scale
        elif current2_scale > target2_scale:
            current2_scale -= scale_speed
            if current2_scale < target2_scale:
                current2_scale = target2_scale

        # Resmi ölçeklendir
        scaled_image = pygame.transform.scale(skins_image, (int(skins_image.get_width() * current_scale), int(skins_image.get_height() * current_scale)))
        scaled_rect = scaled_image.get_rect(center=skins_rect.center)

        scaled2_image = pygame.transform.scale(credits_image, (int(credits_image.get_width() * current2_scale), int(credits_image.get_height() * current2_scale)))
        scaled2_rect = scaled2_image.get_rect(center=credits_rect.center)

        # easter egg'in Alfa değerini azalt (butona basıldıktan sonra)
        if easter_egg_alpha > 0:
            easter_egg_alpha -= 5
        # easter egg'in Alfa değerini azalt (butona basıldıktan sonra)
        if easter_egg2_alpha > 0:
            easter_egg2_alpha -= 5

        # Easter egg butonu
        pygame.draw.rect(screen, WHITE, easter_egg_button_rect)

        # Kaydırma
        scroll_x -= 0.4  # Her döngüde soldan sağa hareket
        if scroll_x <= -background_width:
           scroll_x = 0  # Sonsuz kaydırma

        # Arka planı çiz
        screen.blit(background, (scroll_x, 0))
        screen.blit(background, (scroll_x + background_width, 0))

        screen.blit(scaled2_image, scaled2_rect)
        screen.blit(scaled_image, scaled_rect)

        # Logo ve easter egg resmi
        easter_egg_image.set_alpha(easter_egg_alpha)
        easter_egg_image2.set_alpha(easter_egg2_alpha)

        # Menü açma butonunu çiz (resim kullanarak)
        screen.blit(logo_image, logo_rect)

        # Karartmayı çiz
        if overlay_alpha > 0:
            overlay = pygame.Surface((screen_size[0], screen_size[1]))
            overlay.fill((70, 40, 70))
            overlay.set_alpha(overlay_alpha)
            screen.blit(overlay, (0, 0))

        # Menü alanını çiz
        if menu_y >= -422:
            # Menü resmi
            screen.blit(menu_image, (screen_size[0] // 7 - 50, menu_y - 100))

            # Skin seçim alanını çiz
            for i, skin in enumerate(skins):
                skin_rect = skin.get_rect(center=(85 + i * 110, menu_y + 185))
                screen.blit(skin, skin_rect)

                # Seçilen skin'in etrafına outline ekle
                if i == current_skin_index:
                    pygame.draw.rect(screen, (70, 40, 70), skin_rect.inflate(15, 15), 3, border_radius=10)

            # Menü kapatma butonunu çiz (resim kullanarak)
            close_button_rect = pygame.Rect(screen_size[0] - 120, menu_y + 30, 100, 50)
            screen.blit(menu_close_image, (close_button_rect.x + 15, close_button_rect.y))

        # Ses seviyesi ikonunu güncelle ve çiz
        draw_volume_icon()

        # Buton animasyonlarını belirli bir hızda döngüsel olarak değiştir.
        current_time = time.time()
        if current_time - last_animation_time > animation_speed:
            button1_current_frame = (button1_current_frame + 1) % len(button1_frames)
            button2_current_frame = (button2_current_frame + 1) % len(button2_frames)
            last_animation_time = current_time
        # Butonları ekrana çiz ve alfa değerlerini ayarla.
        button1_frame = button1_frames[button1_current_frame]
        button2_frame = button2_frames[button2_current_frame]
        # Başlat ile Çık tuşlarının belirme efekti.
        button1_alpha = min(255, button1_alpha + fade_in_speed)
        button2_alpha = min(255, button2_alpha + fade_in_speed)
        # Başlat ile Çık tuşlarının alpha değerlerini değiştir.
        button1_frame.set_alpha(button1_alpha)
        button2_frame.set_alpha(button2_alpha)

        # Başlat ile Çık tuşlarını çiz
        screen.blit(button1_frame, button1_rect)
        screen.blit(button2_frame, button2_rect)

        screen.blit(easter_egg_image, easter_egg_rect)
        screen.blit(easter_egg_image2, easter_egg2_rect)

        # Handle intro gif animation
        if current_time - intro_start_time < len(intro_frames) * intro_frame_duration:
            intro_frame_index = int((current_time - intro_start_time) / intro_frame_duration) % len(intro_frames)
            intro_image = intro_frames[intro_frame_index]
            screen.blit(intro_image, (0, 0))
        elif intro_alpha > 0:
            intro_alpha -= fade_out_speed
            intro_image = intro_frames[-1]
            intro_image.set_alpha(intro_alpha)
            screen.blit(intro_image, (0, 0))

        if running == False:
            sys.exit()

        # Ekranı günceller ve FPS ayarlar.
        pygame.display.flip()
        clock.tick(60)

key_actions = {
    pygame.K_PLUS: lambda: update_volume(0.1),
    pygame.K_KP_PLUS: lambda: update_volume(0.1),
    pygame.K_MINUS: lambda: update_volume(-0.1),
    pygame.K_KP_MINUS: lambda: update_volume(-0.1),
}

main_menu()
pygame.quit()