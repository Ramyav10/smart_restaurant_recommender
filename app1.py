import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import bcrypt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Load Datasets
df = pd.read_csv("encoded_dataset1.csv")
raw_df = pd.read_csv("cleaned_dataset12.csv")

#  Styling with Background 
st.set_page_config(page_title=" Restaurant Recommender", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://wallpapercave.com/wp/wp1874169.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)

#  Load or Save Users to users.json 
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Password Hashing 
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Initialize State 
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def navigate(to):
    st.session_state.page = to

# Page: Welcome
 
def welcome_page():
    st.markdown("""
    <style>
    /* Style the h1 title */
    h1 {
        color: white !important;
        text-align: center;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
    }

    /* Target the paragraph from st.markdown (subtitle) */
    p {
        font-size: 24px !important;
        color: white !important;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
    }

    /* Keep buttons red and centered */
    .stButton > button {
        background-color: crimson;
        color: white;
        border-radius: 8px;
        width: 150px;
        margin: 10px auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title("Welcome to the Restaurant Recommendation Platform")
    st.markdown("Get delicious suggestions based on your preferences!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            navigate("register")
    with col2:
        if st.button("Login"):
            navigate("login")


# Login Pagedef register_page():
def register_page():
    st.markdown("""
    <style>
    /* Headings */
    h1, h2, h3 {
        color: white !important;
        text-align: center !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    }

    /* Paragraphs like "Already have an account" */
    p, .markdown-text-container p {
        color: white !important;
        text-align: center !important;
        font-size: 16px;
        margin-top: 20px;
    }

    /* Crimson buttons */
    .stButton > button {
        background-color: crimson !important;
        color: white !important;
        border-radius: 8px;
        width: 150px;
        margin: 10px auto;
        display: block;
        font-weight: bold;
    }

    /* Label styling */
    label {
        color: white !important;
        font-size: 20px !important;
        font-weight: 600;
        text-align: center !important;
        display: block;
    }

    /* Center the input boxes */
    .stTextInput > div > div {
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;

    }
    </style>
    """, unsafe_allow_html=True)

    st.header("Create an Account")

    col_center = st.columns(3)[1]  # center column in a 3-column layout

    with col_center:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Submit"):
            if not email or not password:
                st.warning("Please fill in all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif email in st.session_state.users:
                st.error("User already exists. Please login.")
            else:
                st.session_state.users[email] = hash_password(password)
                save_users(st.session_state.users)
                st.success("Registration successful! You can now log in.")
                navigate("login")

        if st.button("⬅️ Back"):
            navigate("welcome")

    st.markdown("Already have an account? [Login here](#)", unsafe_allow_html=True)
# login page
def login_page():
    st.markdown("""
    <style>
    /* Center and style the title */
    h1, h2, h3 {
        color: white !important;
        text-align: center !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
    }

    /* Input field labels */
    label {
        color: white !important;
        font-size: 20px !important;
        font-weight: 600;
        text-align: center !important;
        display: block;
    }
    
    
    /* Center input boxes horizontally */
   .stTextInput {
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 10px;
    }

    /* Set consistent input width */
    .stTextInput > div {
        width: 60% !important;
        max-width: 400px !important;
    }
    

    /* Ensure typed input is left-aligned */
    input {
        text-align: left !important;
    }

    /* Crimson buttons */
    .stButton > button {
        background-color: crimson !important;
        color: white !important;
        border-radius: 8px;
        width: 150px;
        margin: 10px auto;
        display: block;
        font-weight: bold;
    }

    /* Center and style paragraph text (e.g., register link) */
    p, .markdown-text-container p {
        color: white !important;
        text-align: center !important;
        font-size: 16px !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centered input fields
    st.title("Login")
    col1, col2, col3 = st.columns([1, 2, 1])  # Center the form visually
    with col2:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
   

    # Improved login logic
    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        elif email not in st.session_state.users:
            st.error("User not found. Please register.")
        elif verify_password(password, st.session_state.users[email]):
            st.success("Login successful!")
            st.session_state.logged_in = True
            navigate("recommendation")
        else:
            st.error("Incorrect password.")

    if st.button("Back to Welcome"):
        navigate("welcome")

    st.markdown("Don't have an account? [Register here](#)", unsafe_allow_html=True)

# Recommendation Page
def recommendation_page():
    st.markdown("""
<style>
/* Headings */
h1, h2 {
    color: white !important;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
}

/* All visible form labels: selectboxes, multiselects, sliders */
label {
    color: white !important;
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* Slider ticks and values */
div[data-baseweb="slider"] span {
    color: white !important;
    font-size: 16px !important;
}

/* Any paragraph content or fallback messages */
.stMarkdown p, .stWarning p, div[data-testid="stMarkdownContainer"] p {
    color: white !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)
    st.title("Smart Restaurant Recommender")

    #  Normalize data
    raw_df["City"] = raw_df["City"].astype(str).str.strip().str.title()
    raw_df["Cuisines"] = raw_df["Cuisines"].astype(str).str.strip().str.title()

    # Extract clean cuisine options from full strings
    cuisines = sorted(raw_df["Cuisines"].dropna().unique())
    cities = sorted(raw_df["City"].dropna().unique())

    # User Inputs
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("Choose City", cities)
        selected_cuisines = st.multiselect("Select Cuisines", cuisines, default=cuisines[:1])
    with col2:
        max_cost = st.slider("Max Budget (₹)", 100, 5000, 1500, step=100)
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.5, step=0.1)

   

    # Flatten cuisine strings into keywords
    cuisine_keywords = []
    for group in selected_cuisines:
        cuisine_keywords.extend([c.strip() for c in group.split(",")])

    # Apply full filters using partial keyword match
    filtered = raw_df[
        (raw_df["City"] == city) &
        (raw_df["Cuisines"].apply(lambda x: any(cuisine.lower() in x.lower() for cuisine in cuisine_keywords))) &
        (raw_df["Average Cost for two"] <= max_cost) &
        (raw_df["Aggregate rating"] >= min_rating)
    ]


    if filtered.empty:
        st.warning("No matches found. Try adjusting filters.")
        return
    
    # Feature matrix
    def build_features(data):
        ohe = OneHotEncoder()
        cuisine_ohe = ohe.fit_transform(data[["Cuisines"]]).toarray()
        scaler = MinMaxScaler()
        nums = scaler.fit_transform(data[["Average Cost for two", "Aggregate rating", "Votes"]])
        return np.hstack((cuisine_ohe, nums))

    features = build_features(raw_df)
    similarity = cosine_similarity(features)

    # Recommendations from filtered group only
    def get_recommendations(index, k=5):
        scores = list(enumerate(similarity[index]))
        top = sorted(scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in top[1:]]

        recommended = raw_df.iloc[top_indices]
        

        # Keep same city and cuisine keyword relevance
        return recommended[
            (recommended["City"] == raw_df.loc[index, "City"]) &
            (recommended["Cuisines"].apply(lambda x: any(kw.lower() in x.lower() for kw in cuisine_keywords)))
        ].head(k)
        index = filtered.index[0]
        results = get_recommendations(index)
        st.write("Matching restaurants:", results.shape[0])

    # Get and show results
    index = filtered.index[0]
    results = get_recommendations(index)

    if results.empty:
        st.warning("No similar results found.")
    else:
        for _, row in results.iterrows():
           st.markdown(f"<h3 style='color: crimson;'>🍴 {row['Restaurant Name']}</h3>", unsafe_allow_html=True)
           st.markdown(
    f"<p style='color: gainsboro; font-size: 15px;'>"
    f" {row['Locality']}, {row['City']} |  {row['Cuisines']} |  ₹{row['Average Cost for two']} |  {row['Aggregate rating']}"
    f"</p>",
    unsafe_allow_html=True
)
            
           st.markdown("---")
# --- Router ---
page = st.session_state.page
if page == "welcome":
    welcome_page()
elif page == "register":
    register_page()
elif page == "login":
    login_page()
elif page == "recommendation" and st.session_state.logged_in:
    recommendation_page()
else:
    welcome_page()