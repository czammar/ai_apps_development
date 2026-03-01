# ai_apps_development
A repository for the course "AI Applications Development"

# How to run examples?

1. Create a virtual environment

2. Install dependencies:
   
```
pip install fastapi uvicorn scikit-learn numpy pydantic
```

3. Running the app

```
uvicorn src.diabetes.diabetes_app:app --reload 
```