FROM python:3.10.6
WORKDIR /usr/src/app
COPY ./ ./
RUN pip install -r requirement.txt
ENTRYPOINT ["./entrypoint.sh"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001"]
