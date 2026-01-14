FROM python:3.12-slim

WORKDIR /app

# התקנת דרישות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הפרויקט (כולל תיקיות המפה templates ו-static)
COPY . .

# הגדרת משתמש לא-שורש למניעת שגיאות אבטחה
RUN useradd -m myuser && chown -R myuser /app
USER myuser

CMD ["python", "app.py"]
