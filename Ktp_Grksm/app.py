from flask import Flask, render_template, request, redirect, url_for, flash

# Flask uygulamasını başlat
app = Flask(__name__)
app.secret_key = "secret_key"

# Kitap sınıfı: Kitap bilgilerini tutan sınıf
class Kitap:
    def __init__(self, ad, yazar, yayin_yili):
        self.ad = ad  # Kitap adı
        self.yazar = yazar  # Kitap yazarı
        self.yayin_yili = yayin_yili  # Kitabın yayın yılı

    def __str__(self):
        return f"Kitap: {self.ad}, Yazar: {self.yazar}, Yayın Yılı: {self.yayin_yili}"

# Kütüphane sınıfı: Kitap yönetim işlemlerini yapan sınıf
class Kutuphane:
    def __init__(self):
        self.kitaplar = []  # Kütüphanedeki kitapların listesi

    def kitap_ekle(self, kitap):
        for mevcut_kitap in self.kitaplar:
            if mevcut_kitap.ad == kitap.ad:
                return False
        self.kitaplar.insert(0, kitap)  # Kitap başa ekleniyor
        return True

    def kitap_sil(self, kitap_adi):
        for kitap in self.kitaplar:
            if kitap.ad == kitap_adi:
                self.kitaplar.remove(kitap)
                return True
        return False

    def isme_gore_arama(self, kitap_adi):
        for kitap in self.kitaplar:
            if kitap_adi.lower() in kitap.ad.lower() or kitap_adi.lower() in kitap.yazar.lower():
                return kitap
        return None

    def tum_kitaplari_listele(self):
        return self.kitaplar

# Kütüphane nesnesi
kutuphane = Kutuphane()

@app.route('/')
def index():
    kitaplar = kutuphane.tum_kitaplari_listele()
    return render_template('index.html', kitaplar=kitaplar)

@app.route('/ekle', methods=['POST'])
def ekle():
    ad = request.form['ad']
    yazar = request.form['yazar']
    yayin_yili = request.form['yayin_yili']

    if not ad or not yazar or not yayin_yili.isdigit():
        flash("Hata: Tüm alanları doğru şekilde doldurmalısınız!", "danger")
        return redirect(url_for('index'))

    yeni_kitap = Kitap(ad, yazar, yayin_yili)
    if kutuphane.kitap_ekle(yeni_kitap):
        flash(f"'{ad}' başarıyla eklendi!", "success")
    else:
        flash(f"'{ad}' zaten mevcut!", "danger")
    return redirect(url_for('index'))

@app.route('/sil/<string:kitap_adi>')
def sil(kitap_adi):
    if kutuphane.kitap_sil(kitap_adi):
        flash(f"'{kitap_adi}' başarıyla silindi!", "success")
    else:
        flash(f"'{kitap_adi}' bulunamadı!", "danger")
    return redirect(url_for('index'))

@app.route('/ara', methods=['POST'])
def ara():
    kitap_adi = request.form['arama']
    kitap = kutuphane.isme_gore_arama(kitap_adi)
    if kitap:
        return render_template('index.html', kitaplar=kutuphane.tum_kitaplari_listele(), aranan_kitap=kitap)
    else:
        flash(f"'{kitap_adi}' bulunamadı!", "danger")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
