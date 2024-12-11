FROM python:3.11.10-bookworm
WORKDIR /usr/app
COPY ./ /usr/app
RUN pip3 install -r requirements.txt && \
    pip3 install --upgrade pip
CMD python3 .