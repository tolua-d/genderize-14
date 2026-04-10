# genderize-14

Gender Classification API

Overview:
This is a simple REST API that classifies a person's gender based on their name using genderize.io API.
It returns probability, sample size and a confidence level based on a specific rule and also handles 
invalid inputs and specific edge cases.

Tech Stack:
Python and Django 
https://api.genderized.io - external API

Endpoint:
GET /api/classify?name=<name>

Example Request:
GET /api/classify?name=cole

Successful Response:
{
    "status": "success",
    "data": {
        "name": "ajayi",
        "gender": "male",
        "probability": 0.65,
        "sample_size": 9655,
        "is_confident": false,
        "processed_at": "2026-04-10T18:36:15.640150Z"
    }
}

Run Locally
1. Clone repository: git clone https://github.com/tolua-d/genderize-14.git
2. Install dependecies: pip install -r requirements.txt
3. Set necessary environment variables:  SECRET_KEY
4. Run the server: python manage.py runserver

Author
Tolu Agbaje-Daniels