FROM LenaAi/python:latest

WORKDIR /Lena
RUN chmod 777 /Lena

RUN pip3 install -U pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

RUN git config --global user.email "soumodas4536@gmail.com"
RUN git config --global user.name "Sourayen"

COPY . .

CMD ["python3", "-m", "Lena"]
