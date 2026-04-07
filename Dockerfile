FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH="/app"

CMD ["python", "scripts/run_inference.py"]
