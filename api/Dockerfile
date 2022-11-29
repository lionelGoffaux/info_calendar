FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "gunicorn", "-w", "3", "main:app", "--bind", "0.0.0.0:8000" ]