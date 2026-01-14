FROM python:3.9-slim
WORKDIR /app

# העתקת הדרישות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת האפליקציה
COPY app.py .

# כאן הטריק: אנחנו מעתיקים את התיקיות מהמיקום האמיתי שלהן
# אם ה-Build רץ מתוך תיקיית ה-root של הפרויקט
COPY templates/ ./templates/
COPY static/ ./static/

# בדיקה שהן באמת הועתקו בזמן הבנייה
RUN ls -d templates static && echo "SUCCESS: Map folders copied!"

CMD ["python", "app.py"]
