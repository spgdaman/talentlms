FROM python:3.7

EXPOSE 9091

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD streamlit run --server.port 9091 app.py