# Delivery_API_challenge

docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage

cd app
uvicorn main:app 
http://127.0.0.1:8000/docs#/
