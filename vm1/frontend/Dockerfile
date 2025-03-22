FROM python:alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Expose port 9567 for the frontend service
EXPOSE 9567
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9567"]
