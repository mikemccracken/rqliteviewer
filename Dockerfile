FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip git
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN git clone https://github.com/rqlite/pyrqlite.git
RUN pip install ./pyrqlite
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]