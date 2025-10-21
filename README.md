# Akbank GenAI Bootcamp: Motivasyon Chatbotu Projesi

## Projenin Amacı
Bu proje, RAG (Retrieval Augmented Generation) mimarisine dayanan bir chatbot geliştirerek, yüklenen motivasyonel metinler üzerinde bir web arayüzü üzerinden sunmayı amaçlamaktadır. [cite_start]Proje, Akbank GenAI Bootcamp: Yeni Nesil Proje Kampı kapsamında geliştirilmiştir. [cite: 5]

## Veri Seti Hakkında Bilgi
Projede toplam 3 adet hazır motivasyonel metin dosyası kullanılmıştır. Metinler, kendine inanç, küçük adımlar, vazgeçmeme ve duygusal kabul gibi temaları içerir. [cite_start](Hazır veri setleri kullanmanızda hiçbir sakınca yoktur[cite: 20].)

## Kullanılan Yöntemler
Proje, temel olarak RAG (Retrieval Augmented Generation) mimarisi kullanılarak geliştirilmiştir. 
* [cite_start]**LLM (Generation Model):** Google'ın **Gemini API** kullanılarak LLM servisi sağlanmıştır. [cite: 45]
* [cite_start]**Embedding Model:** Google'a ait bir embedding modeli kullanılmıştır. [cite: 46]
* [cite_start]**Vektör Veritabanı (Vector Database):** **ChromaDB** veya **FAISS** gibi popüler bir vektör veritabanı kullanılmıştır. [cite: 46]
* [cite_start]**RAG Framework:** **LangChain** veya **Haystack** gibi bir RAG pipeline çatısı kullanılmıştır. [cite: 47]

## Elde Edilen Sonuçlar
Temel RAG akışı başarılı bir şekilde kurulmuştur. Chatbot, yüklenen motivasyonel metinlere dayanarak kullanıcı sorularına ilgili ve tutarlı yanıtlar verebilmektedir.

---

## Web Linki (Deploy Link)
**(UYARI: Bu kısım, projenizin web arayüzüne deploy edilmesi tamamlandıktan sonra güncellenecektir.)**
Web Uygulaması Linki: https://huggingface.co/spaces/ceyda18/motivasyon-chatbotu-ceyda
---

### 3 - Kodunuzun Çalışma Kılavuzu

Bu bölüm, projenin yerel geliştirme ortamında nasıl çalıştırılacağını açıklar:

1.  **Gerekli Kütüphanelerin Kurulumu (Virtual Environment):**
    Aşağıdaki komutlarla sanal ortam oluşturulur ve `requirements.txt` dosyası ile tüm bağımlılıklar kurulur:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```
2.  **API Anahtarının Tanımlanması:**
    Google Cloud Console'dan alınan API anahtarının (eğer kullanılıyorsa) ortam değişkeni olarak tanımlanması gerekir:
    ```bash
    export GOOGLE_API_KEY="SİZİN_ANAHTARINIZ"
    ```
3.  **Uygulamanın Başlatılması:**
    Streamlit uygulaması aşağıdaki komutla başlatılır:
    ```bash
    streamlit run app.py
    ```
                                                                                                                                                  
### 5 - Web Arayüzü & Product Kılavuzu

**Çalışma Akışı ve Test Senaryoları:**

Uygulama, Hugging Face deploy linki üzerinden açıldığında, kullanıcı aşağıdaki adımları izler:

1.  Arayüzde bulunan sohbet kutusuna motivasyon metinlerinin içeriğiyle ilgili bir soru sorar.
2.  RAG (Retrieval Augmented Generation) modeli, soruları metinler içinden en alakalı kaynaklarla (kaynak döküman parçaları) birleştirerek anlamlı ve ilgili bir cevap üretir.

**Örnek Test Soruları:**
* "Başarıya ulaşmak için hangi duygusal kabuller gereklidir?"
* "Kendi kendine şüphe ve suçluluk temaları nasıl ele alınır?"

                                                                                                                                                  
