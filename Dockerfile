FROM python:3.10

# Hugging Face highly recommends running as a non-root user with uid 1000
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/app"

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
