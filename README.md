# AI Trafik Polisi - Ön İhlal Raporlama Sistemi

Bu proje, vatandaşların yüklediği görsel/video içeriklerinden **trafik ihlali ön raporu** üretmek için tasarlanmış bir FastAPI servisidir.

> Not: Bu sürüm üretim mimarisine uygun bir temel sağlar. Gerçek cezai süreçte nihai karar yetkili trafik birimlerindedir.

## Özellikler

- Görsel/video yükleme ile AI tabanlı ön analiz
- Yüklenen içeriğe göre ön ihlal raporu oluşturma
- Araç plaka/model tespiti (demo ortamında dosya adı + metadata + örnek çıkarım)
- Vatandaş beyanı + zorunlu yasal onaylarla rapor gönderimi
- İl/ilçe otomatik (header bazlı) veya manuel kayıt
- Admin paneli için bekleyen raporları listeleme / sonuçlandırma API'leri
- Bölge, araç modeli ve ihlal türü istatistikleri

## Hızlı Başlangıç

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API dokümantasyonu:

- Swagger UI: `http://127.0.0.1:8000/docs`

## Örnek Kullanım Akışı

1. Vatandaş medya dosyasını yükler: `POST /api/reports/analyze`
2. Sistem ön analiz döndürür (ihlal türü, güven skoru, plaka/model tahmini)
3. Vatandaş yasal onaylar + TCKN + telefon + bölge bilgisiyle gönderir: `POST /api/reports/submit`
4. Admin bekleyen raporları inceler: `GET /api/admin/reports/pending`
5. Admin raporu sonuca bağlar: `POST /api/admin/reports/{id}/finalize`
6. İstatistikler: `GET /api/stats/violations`

## Demo tespit formatı (opsiyonel)

Daha doğru demo tespiti için dosya adında aşağıdaki formatı kullanabilirsiniz:

`34ABC123_ToyotaCorolla_redlight.jpg`

- `34ABC123` → plaka
- `ToyotaCorolla` → model
- `redlight` → ihlal etiketi

Bu format zorunlu değildir; sistem yine de temel ön analiz üretir.
