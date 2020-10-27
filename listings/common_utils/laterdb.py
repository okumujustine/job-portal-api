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


# urlpatterns = [

# path('', schema_view.with_ui('swagger', cache_timeout=0),
#      name='schema-swagger-ui'),
# path('redoc/', schema_view.with_ui('redoc',
#                                    cache_timeout=0), name='schema-redoc'),
# path("", TemplateView.as_view(template_name='index.html')),
