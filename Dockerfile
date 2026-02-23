FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn playwright pdfplumber pandas fpdf2 python-multipart

COPY . /app

RUN playwright install chromium

CMD ["uvicorn", "robo_buscador_oab:app", "--host", "0.0.0.0", "--port", "8000"]
