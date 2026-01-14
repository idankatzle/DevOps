###############################
# Stage 1: Build Dependencies
###############################
FROM quay.io/fedora/python-312:latest AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

###############################
# Stage 2: Production
###############################
# משתמשים באותו אימג' בסיס של פדורה כדי למנוע משיכה מ-Docker Hub
FROM quay.io/fedora/python-312:latest

# פדורה משתמשת ב-useradd ולא ב-adduser (כמו ב-Alpine)
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser

# העתקת החבילות מה-builder
COPY --from=builder /root/.local /home/appuser/.local
# העתקת הקוד (וודא שהקובץ נמצא ב-src)
COPY app.py .

ENV PATH="/home/appuser/.local/bin:${PATH}"

CMD ["python", "app.py"]
