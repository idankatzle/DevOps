FROM registry.access.redhat.com/ubi9/python-312:latest

# מתעלמים מהקבצים שגורמים לשגיאת ההרשאות ב-OpenShift
LABEL io.kaniko.ignore-path="/usr/bin/newgidmap /usr/bin/newuidmap /usr/sbin/suexec"

USER root
WORKDIR /app

# העתקת הכל (חובה בשביל המפה!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN chown -R 1001:0 /app
USER 1001

CMD ["python", "app.py"]
