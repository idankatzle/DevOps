FROM registry.access.redhat.com/ubi9/python-312:latest

# חזרה למשתמש שורש רק בשביל ההתקנה וההעתקה
USER root

WORKDIR /app

# העתקת דרישות והתקנה
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת הכל (זה מה שיחזיר את המפה!)
COPY . .

# הגדרת הרשאות למשתמש ברירת המחדל של OpenShift (1001)
RUN chown -R 1001:0 /app
USER 1001

CMD ["python", "app.py"]
