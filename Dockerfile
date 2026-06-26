FROM python:3.14-slim

WORKDIR /app

# Install dependencies (system dependencies if needed, e.g. for whois)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn redis

COPY . .

# Expose port 5000
EXPOSE 5000

# Run the app using gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
