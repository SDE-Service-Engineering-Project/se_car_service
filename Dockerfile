FROM python:3.11-alpine as runtime-image
WORKDIR /code
COPY ./ /code/
RUN pip install --no-cache-dir --user --upgrade -r /code/requirements.txt
ENV PORT=8000
EXPOSE $PORT
ENV PATH=/root/.local/bin:$PATH
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
