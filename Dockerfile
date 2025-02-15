FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN ls -l /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "producer.py"]