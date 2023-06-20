FROM python:3.7 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt
FROM python:3.7-slim
EXPOSE 5001
WORKDIR /src
COPY --from=builder /root/.local /root/.local
COPY ./src .
ENV PATH=/root/.local/bin:$PATH
WORKDIR /
ENV PYTHONPATH "${PYTHONPATH}:."
CMD [ "python", "src/app.py" ]