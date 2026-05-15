FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system kairon && adduser --system --ingroup kairon kairon

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh && chown -R kairon:kairon /app

USER kairon

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import json, urllib.request; data=json.loads(urllib.request.urlopen('http://localhost:5000/health', timeout=3).read().decode()); assert data['status'] == 'ok'"

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "run.py"]
