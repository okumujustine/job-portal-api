# run with guinocorn
# CMD gunicorn listings.wsgi:application --bind 0.0.0.0:8000

# build the docker image
# CMD docker build -t listings -f Dockerfile .


# running the docker container
# CMD docker run -it -p 80:8888 listings

# listing all the running containers
# CMD docker ps -a


# stopping the docker container (with container id or image)
# CMD docker stop 5966a461fa9d
# or
# CMD docker stop listings


# run
# CMD docker run -it -p 80:8888 listings
