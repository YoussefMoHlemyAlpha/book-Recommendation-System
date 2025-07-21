import streamlit as st
import pickle
import base64


st.set_page_config(page_title="Book Recommender", layout="wide")

# Function to set local background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set background image
add_bg_from_local("book6.jpg")

# Load  Data
data = pickle.load(open("data.pkl", "rb"))  
similarity = pickle.load(open("similarity.pkl", "rb"))  

# Recommendation function
def recommend(book):
    index = data[data['Title'] == book].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommended_books = []
    recommended_images = []
    
    for i in distances[1:6]:  # Top 5 similar books
        recommended_books.append(data.iloc[i[0]]['Title'])
        recommended_images.append(data.iloc[i[0]]['Image'])
    
    return recommended_books, recommended_images

# Streamlit UI
st.title("📚 Book Recommendation System")

book_list = data['Title'].values
selected_book = st.selectbox("Select a book", book_list)

if st.button("Show Recommendations"):
    names, images = recommend(selected_book)
    
    # Display recommendations in a row
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(images[i], width=150)
            st.caption(names[i])
