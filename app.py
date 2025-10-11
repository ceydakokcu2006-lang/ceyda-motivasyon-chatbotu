import streamlit as st
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Arayüz Başlıkları ---
st.set_page_config(page_title="Motivasyon Chatbotu (RAG)", layout="wide")
st.title("Akbank GenAI Bootcamp: Motivasyon Chatbotu 💡")
st.markdown("Merhaba! Ben, yüklenen motivasyonel metinlere dayalı sorularınızı yanıtlamak için tasarlanmış bir RAG (Retrieval Augmented Generation) modeliyim. Lütfen sadece metinlerin içeriğiyle ilgili sorular sorun.")


# --- RAG Pipeline Tanımlama Fonksiyonu ---
@st.cache_resource
def setup_rag_pipeline():
    """
    RAG pipeline'ını kurar ve Vektör Veritabanını hazırlar.
    Bu fonksiyon, uygulamayı her başlattığınızda yalnızca bir kez çalışır.
    """
    # 1. Veri Yükleme (Dosyaları Streamlit ortamında varsayıyoruz)
    # NOT: Veri setini (motivasyon1-3.txt) GitHub'a yüklememiz gerekecek.
    
    # Hata: Colab'da yüklenen dosyaları buradan okuyamayız. 
    # Geçici olarak metinleri doğrudan buraya ekleyelim, 
    # aksi takdirde deploy zorlaşır. (Normalde dosyaları yüklememiz gerekir.)
    
    motivasyonel_metin = """
    Kendine inan, çünkü sen düşündüğünden daha güçlüsün. Bugün kötü olabilir ama yarın yeni bir başlangıç. Küçük adımlar büyük farklar yaratır.
    Vazgeçmek kolaydır ama devam etmek kazandırır. Her başarı, bir hayalle başlar. Bir nefes bile umut taşır.
    Üzüntüye de izin ver, hissetmek güçlendirir. Mutluluğu bulacak olan, sensin. İyileşmek için kötü anıları bavul gibi taşımayı bırakmalısın.
    """
    
    # TextLoader yerine doğrudan metin içeriğini kullanalım
    from langchain.schema import Document
    documents = [Document(page_content=motivasyonel_metin, metadata={"source": "motivasyon_metinleri"})]
    
    # 2. Parçalama
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # 3. Embedding ve Vektör Veritabanı Oluşturma
    # API key'in Streamlit Secrets veya OS Environment'tan geldiğini varsayıyoruz.
    if "GEMINI_API_KEY" not in os.environ:
        st.error("Lütfen Gemini API Anahtarınızı Streamlit'e ekleyin.")
        st.stop()
        
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding)
    
    # 4. Retriever ve Model Tanımlama
    retriever = vectorstore.as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    # 5. Prompt Şablonu
    template = """
    Sen bir motivasyon chatbotusun. Sadece verilen bağlamı (context) kullanarak, soruyu yanıtla. 
    Eğer bağlamda soruyla ilgili bilgi bulamıyorsan, kibarca "Bu bilgi elimdeki motivasyon metinlerinde bulunmamaktadır." diye cevap ver.
    Cevapları Türkçe ve motive edici bir dille ver.

    Bağlam: {context} 
    Soru: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    # 6. RAG Zinciri (Chain)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# RAG pipeline'ı kur
rag_chain = setup_rag_pipeline()


# --- Chatbot Arayüzü Mantığı ---

# Konuşma geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan input al
if prompt := st.chat_input("Motivasyonel metinlerle ilgili sorunuz nedir?"):
    # Kullanıcı mesajını geçmişe ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # LLM yanıtını al ve göster
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            # RAG zincirini çalıştır
            response = rag_chain.invoke(prompt)
            st.markdown(response)
            
    # Asistan yanıtını geçmişe ekle
    st.session_state.messages.append({"role": "assistant", "content": response})
