FROM python:3.9-slim

WORKDIR /app

# Copy dependency file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire content of the src folder
# This includes app.py and any subfolders we put here
COPY . .

# Final check: list files during build to be sure
RUN ls -la

CMD ["python", "app.py"]
