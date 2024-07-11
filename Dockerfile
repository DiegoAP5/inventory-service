FROM python:3.9 

ADD src/main.py .
RUN pip install -r Flask SQLAlchemy pymysql

CMD ["python", "./src/main.py"] 