import streamlit as st

# Function to display a team member
def display_team_member(name, role, bio, fun_fact, image_path):
    col1, col2 = st.columns([1, 3])  # Create two columns for layout

    with col1:
        st.image(image_path, width=150)  # Display the team member's image

    with col2:
        st.markdown(f"### {name}")
        st.markdown(f"**{role}**")
        st.write(bio)
        st.markdown(f"💡 *{fun_fact}*")

# Meet the Team Section
st.markdown("## 👥 Meet the Team")
st.markdown("Our team brings together expertise in machine learning, financial analytics, business strategy, and web development.")

# Team Members
team_members = [
    ("Leonardo V. Kietzell", "🚀 Lead Business Strategist", 
        "🇩🇪 Leonardo is from Germany and brings **years of consulting and business strategy insights** to the project. 📊 His expertise in **decision-making & market analysis** helped shape the vision of our trading system.",
        "🏃‍♂️ He is currently training for the **Tokyo Marathon**! 🎌", "data/Leonardo.jpeg"),

    ("Gizela Thomas", "💻 Streamlit Developer", 
        "🇺🇸 Gizela is from the USA and has **experience in consulting** but primarily works in the **health sector**. 🏥 She was responsible for building the **Streamlit interface**, ensuring a smooth and user-friendly experience.",
        "📰 She has been on the **front page of Yahoo News**! 🌟", "data/gizela.jpeg"),

    ("Nitin Jangir", "🤖 Machine Learning Engineer", 
        "🇮🇳 Nitin is from India and is using his **master’s degree** to strengthen his technical skills. 🎓 He worked on **building predictive analytics models** and wants to pursue a career in **data engineering**. 📊",
        "🍳 Since moving to Spain, he started **eating eggs for the first time** despite being a lifelong vegetarian! 🥚", "data/nitin.jpeg"),

    ("Santiago Ruiz Hernández", "📌 Project Point Lead", 
        "🇪🇸 Santiago is from Valencia, Spain, and worked on **various aspects of the project**, acting as a key **point lead** to keep everything running smoothly. 🔄 His contributions touched on multiple areas of **EDA, strategy, and technical implementation**.",
        "🎾 He **loves playing tennis** and is a **natural redhead**! 🔥", "data/santi.jpg"),

    ("Santiago Botero", "📈 EDA & Financial Insights", 
        "🇨🇴 Santiago is from Colombia, has a **finance background**, and is currently pursuing a **dual MBA**. 🎓 He was responsible for **exploratory data analysis (EDA)**, ensuring the financial data was properly analyzed and interpreted. 📉",
        "🌍 He speaks **four languages fluently**! 🗣️🌎", "data/santiago.jpeg")
]

# ✅ Display each team member
for member in team_members:
    display_team_member(*member)
