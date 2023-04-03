FROM python:3.11-slim
WORKDIR /code
COPY ./ /code/

ENV PORT=8000
EXPOSE $PORT
ENV PATH=/root/.local/bin:$PATH
RUN pip install --no-cache-dir --upgrade  -r /code/requirements.txt
RUN addgroup --system nonroot \
    && adduser --system nonroot
USER nonroot
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
