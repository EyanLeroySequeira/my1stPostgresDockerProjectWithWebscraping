# FROM python:3.10.2-alpine3.15
# # Create directories
# RUN mkdir -p /root/workspace/src
# # Copy the script to the container
# COPY ./postedBy.py /root/workspace/src
# # Switch to the project directory
# WORKDIR /root/workspace/src
# # Install required packages
# RUN pip install --upgrade pip
# RUN pip install requests bs4 html5lib
# # RUN pip install psycopg2
# CMD ["postedBy.py"]
# # Set the entrypoint to the python script
# ENTRYPOINT ["python"]



FROM python:3.10.2-alpine3.15

# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./database.py /root/workspace/src
COPY ./postedBy.py /root/workspace/src
# Switch to project directory
WORKDIR /root/workspace/src

RUN pip install --upgrade pip
RUN pip install requests bs4 html5lib

# Install required packages
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies for psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# # Install Python packages
RUN pip install --no-cache-dir requests bs4 html5lib psycopg2-binary
# Set the command to run your script
CMD [ "database.py"]
ENTRYPOINT ["python"]