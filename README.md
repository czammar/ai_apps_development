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


```
uvicorn src.images_app.backend.main:app --reload 
streamlit run src/images_app/frontend/app.py 
```

# 4. Other Apps

```
uvicorn src.restaurant.main:app --reload
```