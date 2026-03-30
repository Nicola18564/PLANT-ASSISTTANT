FROM python:3.13-slim

WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir --upgrade pip
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["python", "-m", "baseline.run_baseline"]
