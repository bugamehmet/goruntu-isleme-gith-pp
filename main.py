from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os

def fotoğrafı_ikiliye_dönüştür(fotoğraf_yolu, eşik_değeri):
    fotoğraf = Image.open(fotoğraf_yolu)
    gri_tonlama = fotoğraf.convert("L")
    piksel_dizisi = np.array(gri_tonlama)
    ikili_dizi = (piksel_dizisi > eşik_değeri).astype(int)
    return ikili_dizi

def ikili_diziyi_resme_dönüştür(ikili_dizi):
    ikili_resim = Image.fromarray((ikili_dizi * 255).astype(np.uint8))
    return ikili_resim

def kaydet_ve_numaralandır(kaydedilecek_dizin, dosya_adı, uzantı=".png"):
    dosya_yolu = os.path.join(kaydedilecek_dizin, f"{dosya_adı}{uzantı}")
    sayac = 1
    while os.path.exists(dosya_yolu):
        dosya_yolu = os.path.join(kaydedilecek_dizin, f"{dosya_adı}_{sayac}{uzantı}")
        sayac += 1
    return dosya_yolu

def add_tv_noise(image, intensity=0.1):
    img_array = np.array(image)
    noise = np.random.normal(scale=intensity, size=img_array.shape).astype(np.uint8)
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    noisy_image = Image.fromarray(img_array)
    return noisy_image

def resmi_aydinlat(resim, kaydedilecek_dizin):
    enhancer = ImageEnhance.Brightness(resim)
    aydinlatilmis_resim = enhancer.enhance(2.5)
    aydinlatilmis_resim.show()
    kaydedilecek_resim_yolu = kaydet_ve_numaralandır(kaydedilecek_dizin, 'degisik')
    aydinlatilmis_resim.save(kaydedilecek_resim_yolu)

def pikselleri_belirgin_hale_getir(resim_yolu, boyut, kaydedilecek_dizin):
    resim = Image.open(resim_yolu)
    belirgin = resim.filter(ImageFilter.FIND_EDGES)
    belirgin.show()
    yeni_resim = resim.resize((boyut, boyut))
    yeni_resim.show()
    kaydedilecek_resim_yolu = kaydet_ve_numaralandır(kaydedilecek_dizin, 'yeni_resim')
    belirgin.save(kaydedilecek_resim_yolu)

# Kullanım
kaydedilecek_dizin = ""
fotoğraf_yolu = 'asilfotograf.jpeg'
eşik_değeri = 100

ikili_dizi = fotoğrafı_ikiliye_dönüştür(fotoğraf_yolu, eşik_değeri)
ikili_resim = ikili_diziyi_resme_dönüştür(ikili_dizi)

dosya_adı = "resim"
kaydedilecek_resim_yolu = kaydet_ve_numaralandır(kaydedilecek_dizin, dosya_adı)

fotoğraf = Image.open(fotoğraf_yolu)
noisy_img = add_tv_noise(fotoğraf, intensity=30.1)

ikili_resim.save(kaydedilecek_resim_yolu)
kaydet_ve_numaralandır(kaydedilecek_dizin, 'degisik')
resmi_aydinlat(noisy_img, kaydedilecek_dizin)

pikselleri_belirgin_hale_getir(fotoğraf_yolu, 20, kaydedilecek_dizin)
