# TP04 Dockerfile — runs TP03 analysis and serves results via Flask (port 80)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools (one-line to avoid line-continuation issues on Windows)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc g++ && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Project files (analysis, data, figures, report)
COPY TP03_analysis.py /app/TP03_analysis.py
COPY TP03_sales_data.csv /app/TP03_sales_data.csv
COPY TP03_sales_data_clean.csv /app/TP03_sales_data_clean.csv
COPY customer_segments.csv /app/customer_segments.csv
COPY figures/ /app/figures/
COPY report/ /app/report/
COPY app.py /app/app.py

EXPOSE 80
CMD ["python", "app.py"]
