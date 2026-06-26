# Aegis - AI Phishing Detection System

## Clone the Repository

git clone https://github.com/arunmozhi-varman-05/Aegis.git
cd Aegis


## Create Virtual Environment

python -m venv venv

Activate environment

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate


## Install Dependencies

pip install -r requirements.txt


## Train the Model

python train_model.py


## Run the Application

python app.py

Project Structure

Aegis/
│
├── app.py                # Flask backend
├── train_model.py        # Model training
├── predict.py            # URL prediction
├── feature_extraction.py # Feature extraction
├── extension/            # Chrome extension
├── requirements.txt
└── README.md
