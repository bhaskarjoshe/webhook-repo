#python Base image
FROM python:3.11-slim

#working directory
WORKDIR /app

#dependency installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy project file
COPY . .

#flask port
EXPOSE 5000

#run flask
CMD ["flask", "run", "--host=0.0.0.0"]
