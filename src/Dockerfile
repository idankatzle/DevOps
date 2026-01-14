FROM quay.io/prometheus/busybox:latest

# אנחנו משתמשים בגישה של "העתקה בלבד" כדי לעקוף את Kaniko
FROM python:3.9-slim

WORKDIR /app

# העתקה של הכל - זה יחזיר את המפה
COPY . .

# התקנה בסיסית
RUN pip install --no-cache-dir -r requirements.txt

# פקודת הרצה
CMD ["python", "app.py"]
