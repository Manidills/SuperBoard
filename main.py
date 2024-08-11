import streamlit as st

from eas import eas
from home import home
from page import page

# Set page configuration
st.set_page_config(
    page_title="L2 Analytics",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app generates scripts for data clean rooms!"
    }
)

# Sidebar settings
st.sidebar.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFjb2UzaWFwMnZqZWE1b2N3Yjc5OTltYzdxM2h5YXY2MWd6MXBxbyZlcD12MV9pbnRlcm5naWZfYnlfaWQmY3Q9cw/UAragLbg9oKRfZLThq/giphy.webp", use_column_width=True)
st.sidebar.title("Superhack Health Dashboard")

# Add icons to each action
actions = {
    "Home": ("🏠", page),
    "Analytics": ("📊", home),
    "Protocols": ("🔗", eas),
    # "Bridge Visualization": ("🌉", Bridge),
    # "Contracts": ("📜", explorer)
}

# Create a radio button with icons
action = st.sidebar.radio("Choose an action:", list(actions.keys()), format_func=lambda x: f"{actions[x][0]} {x}")

# Main function to handle different actions
def main():
    actions[action][1]()

if __name__ == "__main__":
    main()
