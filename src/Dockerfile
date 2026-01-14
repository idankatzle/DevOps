FROM quay.io/fedora/python-312:latest

USER root
WORKDIR /app

# התקנת דרישות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל הפרויקט (כולל תיקיות המפה)
COPY . .

# הגדרת הרשאות
RUN chown -R 1001:0 /app
USER 1001

CMD ["python", "app.py"]
