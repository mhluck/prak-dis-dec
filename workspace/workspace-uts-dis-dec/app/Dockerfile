FROM docker.io/library/python:3.14-rc-slim
WORKDIR /app
COPY main.py /app/
RUN pip install "fastapi[standard]"
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]