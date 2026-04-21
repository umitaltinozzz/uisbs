# UİSBS — Ulusal İlaç Stok ve Bilgi Sistemi

> *Bu proje, babamın kanser tedavisi sırasında ilaç bulamama çaresizliğini yaşamamak için başladı.*

---

## Neden Bu Proje?

2024 yılında babam kanser tanısı aldı. Tedavi sürecinin en zorlu yanlarından biri, reçeteye yazılan bazı ilaçların şehrin hiçbir eczanesinde bulunamamasıydı. Saatlerce telefon edilerek, eczaneden eczaneye koşturularak geçen günler yaşandı.

O günlerde aklımda tek bir soru vardı: **Bu bilgi neden merkezi bir yerde yok?**

Bir eczanede ilaç varsa ve bir hasta bunu bilmiyorsa — bu bir veri sorunudur. Ve veri sorunlarının çözümü yazılımdır.

Bu motivasyonla UİSBS'yi geliştirmeye başladım.

---

## Proje Hakkında

**UİSBS (Ulusal İlaç Stok ve Bilgi Sistemi)**, Türkiye genelindeki eczanelerin ilaç stoklarını gerçek zamanlı olarak paylaştığı ve hastaların/vatandaşların yakınlarındaki eczanelerde ilaç arayabildiği merkezi bir platformdur.

### Toplanan Veriler

Bu projeyle birlikte kamuya açık kaynaklardan derlenen veriler:

- **90.000+** ilaç verisi (barkod, etken madde, kategori, üretici bilgileri)
- **40.000+** eczane verisi (il, ilçe, adres, telefon)

Örnek veri dosyası: [`ilce_eczaneler_20250528_001708.csv`](./ilce_eczaneler_20250528_001708.csv)

---

## Teknik Altyapı

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python / FastAPI |
| Frontend | TypeScript / React / Tailwind CSS |
| Veritabanı | PostgreSQL + PostGIS (coğrafi sorgular) |
| Kimlik Doğrulama | JWT + OAuth2 |
| Önbellek | Redis |
| Altyapı | Docker / Docker Compose |

### Özellikler

- Lokasyon bazlı ilaç arama (PostGIS ile mesafe hesabı)
- Eczane stok yönetimi
- Rol tabanlı yetkilendirme (vatandaş / eczane / yönetici)
- Tam audit log altyapısı
- OpenAPI / Swagger dökümantasyonu

---

## Neden Yarım Kaldı?

Bu sistemi **ülke genelinde** ve potansiyel olarak **AB ülkelerinde** yaygınlaştırmak için çok ciddi düzenleyici engeller olduğunu gördüm:

- **Sağlık Bakanlığı lisansı ve protokol gereklilikleri** — eczane stok verilerini merkezi olarak toplayan bir platform işletmek Türkiye'de Sağlık Bakanlığı izni gerektiriyor
- **KVKK / GDPR uyumu** — hasta ve eczane verilerinin işlenmesi için detaylı veri işleme anlaşmaları ve DPO atanması gerekiyor
- **Eczacılar Birliği onayı** — eczanelerin sisteme dahil olması için meslek kuruluşlarının onayı şart
- **İlaç takip sistemi entegrasyonu** — Türkiye'nin mevcut İTS (İlaç Takip Sistemi) ile entegrasyon zorunlu hale geliyor ve bu tamamen ayrı bir bürokratik süreç

Bu engellerin bireysel bir geliştirici olarak aşılabilir olmadığını görerek projeyi durdurdum. Sistemi tam anlamıyla işletmek, bir yazılım şirketinin değil; kamu kurumu işbirliğinin gerektirdiği bir yapı.

---

## Projeyi Çalıştırmak

```bash
# Depoyu klonlayın
git clone https://github.com/[kullanici-adi]/uisbs.git
cd uisbs

# Altyapıyı başlatın (PostgreSQL + Redis)
docker-compose up -d postgres redis

# Backend'i Docker ile başlatın
docker-compose up -d backend

# Frontend'i yerel olarak başlatın
cd frontend
npm install
npm start
```

**Erişim noktaları:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Dökümantasyonu: http://localhost:8000/docs

---

## Katkı

Bu proje aktif geliştirilmiyor. Ancak:

- Benzer bir sorunu çözmek isteyen biriyseniz,
- Bir sağlık kurumu veya bakanlıkla bağlantınız varsa,
- Ya da sadece bu konuyu konuşmak istiyorsanız —

İletişime geçebilirsiniz. Topladığım verileri ve teknik altyapıyı paylaşmaktan memnuniyet duyarım.

---

## Son Söz

Babam tedavisini tamamladı. Bu projeyi yarıda bıraktım ama o günlerde hissettiğim çaresizliği unutmadım.

Umarım bir gün — devlet eliyle ya da başka biri tarafından — bu sorun gerçekten çözülür. Ve hiçbir hasta, var olan bir ilacı bulamadığı için acı çekmek zorunda kalmaz.

---

*Lisans: MIT — Veriler ve kod serbestçe kullanılabilir.*
