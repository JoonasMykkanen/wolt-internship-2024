FROM python:3.9.6-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
