FROM python:3.10
WORKDIR /app
COPY requirements.txt app.py mot_metinleri.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
