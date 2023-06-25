FROM sanicframework/sanic:3.9-latest

WORKDIR /sanic

COPY . .

RUN apk add --update make && apk add curl
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app/server.py"]