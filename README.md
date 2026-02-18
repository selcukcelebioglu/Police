# AI Trafik Polisi - Gerçek Operasyon Odaklı Ön İhlal Sistemi

Bu proje, vatandaşların yüklediği görsel/video içeriklerinden **ön trafik ihlal raporu** üretir, yasal beyanları toplar, raporu gerçek trafik polisi onayına gönderir ve bölge/araç/ihlâl istatistiklerini tutar.

> ⚖️ Sistem, idari-cezai sürecin yerini almaz; nihai karar yetkili trafik birimlerindedir. Bu nedenle mimari, insan denetimli "ön rapor + resmi onay" akışı üzerine kuruludur.

## Hedeflenen gerçek kullanım

- Vatandaş ihlal görselini/videosunu yükler.
- AI analiz katmanı ihlal türü, plaka ve araç modeli için ön tespit üretir.
- Sistem, güncel trafik mevzuatı referanslarıyla ön rapor çıkarır.
- Vatandaş TCKN, telefon, yasal onaylar ve bölge bilgisiyle raporu iletir.
- Admin paneline düşen kayıt, trafik polisi tarafından son kontrolden geçerek onay/reddedilir.
- Sistem; il/ilçe, ihlal tipi, araç modeli gibi boyutlarda istatistik üretir.

## Mimari

- **Backend:** FastAPI
- **Veri katmanı:** SQLAlchemy + SQLite (kolay başlangıç, üretimde PostgreSQL önerilir)
- **Analiz servisleri:** `app/services/analyzer.py` (şu an heuristik, üretimde CV/OCR model entegrasyonuna hazır)
- **Yasal referanslar:** `app/services/legal.py`
- **Lokasyon çözümleme:** manuel alanlar + header fallback (`X-City`, `X-District`)

## API uçları

- `POST /api/reports/analyze`
  - Görsel/video dosyasını alır, ön tespit döner.
- `POST /api/reports/submit`
  - TCKN + telefon + yasal onay + analiz çıktısıyla ön raporu kaydeder.
- `GET /api/admin/reports/pending`
  - Bekleyen ön raporları listeler.
- `POST /api/admin/reports/{id}/finalize`
  - Trafik birimi kararı (approved/rejected) ile raporu kapatır.
- `GET /api/stats/violations`
  - Şehir, ilçe, araç modeli ve ihlal türü kırılımında istatistik döner.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger:

- `http://127.0.0.1:8000/docs`

## Test

```bash
pytest -q
```

## Demo isimlendirme (yüksek doğruluk için)

Dosya adı şu formatta verilirse analiz daha doğru olur:

`34ABC123_ToyotaCorolla_redlight.jpg`

- `34ABC123` → plaka
- `ToyotaCorolla` → model
- `redlight` → ihlal etiketi

Desteklenen ihlal etiketleri:

- `redlight`
- `speeding`
- `wrong_parking`
- `lane_violation`
- `phone_use`
- `seatbelt`

## Üretim için bir sonraki adımlar

1. Gerçek ANPR (plaka tanıma) ve araç sınıflandırma modellerinin entegrasyonu
2. Video için frame-level olay tespiti + olay zaman damgası
3. KVKK uyumlu veri maskeleme, loglama, retention ve erişim denetimi
4. Kimlik doğrulama/rol yönetimi (vatandaş, operatör, amir)
5. PostgreSQL + message queue + object storage ile ölçeklendirme
