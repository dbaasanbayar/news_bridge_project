# 1. Суурь үйлдлийн систем ба Питоны хувилбар
FROM python:3.11-slim

# 2. Ажлын хавтас үүсгэх (Контейнер дотор)
WORKDIR /app

# 3. Шаардлагатай сангуудын жагсаалтыг хуулах
COPY requirements.txt .

# 4. Сангуудыг суулгах
RUN pip install --no-cache-dir -r requirements.txt

# 5. Бүх кодоо контейнер руу хуулах
COPY . .

# 6. Өгөгдлийн сан хадгалах хавтас үүсгэх
RUN mkdir -p data logs

# 7. Програмыг ажиллуулах тушаал
CMD ["python", "main.py"]
