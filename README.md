
## Blog app backend with fastapi

### Blog CRUD with JWT authentication
- Python 3.8 or higher required


  
## How to run server on local machine

- Clone the repository
```bash
  git clone https://github.com/sangrampattnaik/blogapibackend.git
```
- Create virtual environment and Install depedancies
```
    virtualenv venv
    pip install -r requirements.txt
```
- Runserver
```
uvicorn main:app --reload
or
python3 main.py
```
## Usage
#### Follow swagger documention
- swagger docs - localhost:8000/swagger
- redoc docs - localhost:8000/redoc
- Deployed on aws served by supervisor and nginx 
    - Public DNS https://ec2-13-126-40-21.ap-south-1.compute.amazonaws.com/
    - Swagger Docs http://ec2-13-126-40-21.ap-south-1.compute.amazonaws.com/swagger
    - Redoc Docs http://ec2-13-126-40-21.ap-south-1.compute.amazonaws.com/redoc

  
## Author

 - [Sanngram Pattnaik](https://github.com/sangrampattnaik)

  