FROM python:3

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN uname -a
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN source bin/activate
RUN pip install pip-tools
RUN pip install -r requirements.txt

CMD python dictio.py