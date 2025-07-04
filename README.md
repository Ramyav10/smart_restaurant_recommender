# Smart Restaurant Recommendation System

A personalized restaurant recommendation platform developed using **Python, **Streamlit, and **machine learning*. This interactive application allows users to discover restaurants tailored to their preferences, including location, cuisine, budget, and ratings.

This project was built as part of an internship submission to demonstrate my skills in data preprocessing, recommendation systems, web app development, and user authentication.

---

## Overview

This web-based app recommends restaurants by analyzing:

- *City* and *cuisine* preferences
- *Maximum cost* (budget) and *minimum rating*
- Historical popularity metrics (votes, ratings)

The application includes user authentication and a visually styled interface for a smooth user experience.

---

##  Features

- *User Authentication*  
  Secure registration and login using password hashing (bcrypt)

- *ML-Powered Recommendation Engine*  
  Uses *Cosine Similarity* on preprocessed and encoded features

- *Real-Time Filtering*  
  Filter by city, cuisine, cost, and rating thresholds

- *Interactive Web App*  
  Built with *Streamlit*, styled with custom CSS and background

---

##  How It Works

1. *User Input*: City, cuisines, cost, and rating preferences
2. *Filtering*: Raw dataset filtered based on input constraints
3. *Feature Matching*: Cosine similarity computed on pre-encoded features
4. *Results*: Most relevant restaurants are displayed with name, locality, cuisine, cost, and rating

---

##  Getting Started

### Step 1: Install Dependencies

pip install -r requirements.txt

---

### Step 2: Run the App

streamlit run app1.py

> Users can register or log in from the app interface. Passwords are securely stored using bcrypt.




---

### Technologies Used

Python

Streamlit – for interactive UI

pandas, numpy, scikit-learn – for data processing and feature engineering

bcrypt – for secure password storage

cosine_similarity – for computing restaurant similarity



