# **Boti-HotelBookingChat**  

## **Docker set up: (make sure to have your Docker engine working)** 
 ```bash
		docker-compose up --build 
		docker-compose up
```
Hint:  The rasa server takes a bit until is running, check the terminal  until you see the message „Rasa server is up and running.“

# **Without Docker:**

Make sure you have python 10. installed and follow the following commands:
 ```bash 
python -m pip install --upgrade pip
```
 ```bash 
pip install --no-cache-dir -r requirements.txt
```
        or
 ```bash 
pip install -r requirements.txt 
```
In three different terminals now run:
 
### First terminal: 
  ```bash
rasa run --enable-api --cors ’*‘
```
 This takes a moment
 ### Second terminal:
   ```bash
rasa run actions
```
 ### Third terminal:
   ```bash
cd frontend
   ```

 ```bash
uvicorn main:app --host 0.0.0.0 --port 8000
   ```

Open your browser and go to http://localhost:8000/






