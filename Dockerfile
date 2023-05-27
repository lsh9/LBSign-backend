FROM python:3.9
WORKDIR /lbsign

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "run:app", "-c", "./gunicorn.conf.py"]