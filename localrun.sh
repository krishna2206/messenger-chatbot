if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
  uvicorn app:webserver --host $APP_HOST --port $APP_PORT
fi
