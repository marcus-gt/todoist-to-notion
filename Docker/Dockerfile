FROM python:3.7-alpine

WORKDIR /usr/src/app

# COPY . /app
COPY . ./

# WORKDIR /app

RUN pip install -r requirements.txt

# EXPOSE 8080

CMD python ./todist-fetcher-docker.py

#CMD ["test.py"]
#ENTRYPOINT ["python3"]




# docker build --tag todoist_push . 
# docker run --name todoist_push -p 8080:8080 todoist_push
# docker rm --force todoist_push 