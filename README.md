# **Pelican Eats**

This Capstone Project serves as a culmination of technical skills my group members and I have obtained during our respective degrees in the computing department.  
**Pelican Eats** is a food delivery application that was initially targeted toward the students(commuters and hall residents) and staff of the UWI Mona Campus. 
It has now become more wide scale and there is room for improvement. 

___
## Flask API Setup details

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/Scripts/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app run
```

## vueJS Setup inside venv virtual environment

#### This cretates the package.json file.
```sh
npm init -y 
```

#### This creates the node_modules directory
```sh
npm install vue@3
```

#### Additional cli tools
```sh
npm install -g @vue/cli
```

#### Start Vite server
```sh
npm run dev
```


## Docker Setup

#### Login to your docker if you are not already logged in
````sh
docker login -u <username>
````

#### Pull code from docker

````sh
docker pull prxnce14/my-web-app-backend:v0.1.0
````

````sh
docker pull prxnce14/my-web-app-frontend:v0.1.0
````

#### Running containers using docker-compose 

Add these files to the directory your running from
docker-compose.yml, .env

##### Configuring the .env file

Please refer to the .env.sample file and input your own secret keys and postgres information

##### Run container

````sh
docker-compose up -d
````

##### Drop container 
````sh
docker-compose down
````


#### Running containers using docker run 

Add this file to the directory you're running from

.env 


##### Run container - Backend, Frontend

````sh
docker run -d --restart always -p 7000:7000 --env-file .env --name pelicanEATS-backend -v data_volume:/var/lib/psql prxnce14/my-web-app-backend:v0.1.0
````


````sh
docker run -d --restart always -p 5173:5173 --env-file .env --name pelicanEATS-frontend prxnce14/my-web-app-frontend:v0.1.0
````













