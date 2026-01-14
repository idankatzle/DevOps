FROM quay.io/biocontainers/python:3.12--1

WORKDIR /app

# התקנת ספריות הכרחיות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת הכל (כולל תיקיות המפה)
COPY . .

# הרשאות משתמש
RUN useradd -m myuser && chown -R myuser /app
USER myuser

CMD ["python", "app.py"]
