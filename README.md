# Chat Room Application 

**Author**: Gunjan Singh
**Date**: 9/23/2022

# Technologies used

 1. MongoDB
 2. Python Flask (REST API + jwt) with SocketIO (for websockets)
 3. React.js with SocketIO (for websockets)

# Steps to install
## Backend

 1. cd nimble-test-master/api
 2. pip install -r requirements.txt

## Frontend

 1. cd nimble-test-master/client
 2. npm install

## Database

 1. Install MongoDB from https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/ 
 2. Create a new connection and get the connection URL.
 3. Create .env file in nimble-test/api
 4. Save the connection URL in .env file as DATABASE_URL="< database url >"

# Steps to run
## Backend

 1. cd nimble-test-master/api
 2. python app.py
 
 ## Frontend
 
 1. cd nimble-test-master/client
 2. npm start
