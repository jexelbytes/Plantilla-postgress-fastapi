FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src /code/
EXPOSE 80
CMD ["python", "main.py"]