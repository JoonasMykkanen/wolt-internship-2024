FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m user
USER user

CMD ["python3", "run.py"]

EXPOSE 8000