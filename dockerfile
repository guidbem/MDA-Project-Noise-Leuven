FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ARG aws_key

ARG aws_secret_key

ENV AWS_ACCESS_KEY_ID=$aws_key

ENV AWS_SECRET_ACCESS_KEY=$aws_secret_key

RUN chmod +x install_config_awscli.sh

RUN ./install_config_awscli.sh

RUN aws s3 cp s3://mda-project-noise-leuven . --recursive

EXPOSE 8080

CMD python3 app.py
