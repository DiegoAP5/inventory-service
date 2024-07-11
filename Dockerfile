FROM python:3.9 

ADD src/main.py .
RUN pip install -r src/requeriments.txt

CMD ["python", "./src/main.py"] 