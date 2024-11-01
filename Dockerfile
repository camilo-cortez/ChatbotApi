FROM python:3.9

EXPOSE 5008

WORKDIR /chatbot

COPY . /chatbot/

RUN pip install pipenv && pipenv install

ENV PYTHONPATH /chatbot

ENTRYPOINT ["pipenv", "run", "python", "./src/main.py"]
