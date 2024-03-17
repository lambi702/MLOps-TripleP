FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN command -v pip3 && pip3 install --no-cache-dir -r requirements.txt || pip install --no-cache-dir -r requirements.txt

COPY test.py .

CMD ["python", "test.py"]
