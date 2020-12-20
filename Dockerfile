FROM python:3

WORKDIR /

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN  python setup.py install

ENTRYPOINT [ "ffc"]