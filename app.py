from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os

# LOGIC 1: Define the Chat Prompt Template
# This template sets up the AI's role and the user's query format.
chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a helpful AI Assistant for a travel agency. Your job is to help users find flight, railway, or bus bookings from a source to a destination. Provide a detailed list of all available travel options in the form of a table, including trip cost, facilities, and other relevant details. List all available flights, railways, and buses."),
        ("human", "Book a trip from {source} to {destination} on {date} for {passengers} passenger(s). Do not ask for more information. Just provide a list of all available flights, railways, and buses.")
    ],
    partial_variables={"source": "DEL", "destination": "BLR", "passengers": 1}  # Default values for testing
)

# LOGIC 2: Initialize the Chat Model
# This is the AI model that will generate the travel recommendations.
chat_model = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("API_KEY"),
    model="gemini-2.0-flash-exp",
    temperature=1  # Controls the creativity of the responses
)

# LOGIC 3: Set up the Output Parser
parser = StrOutputParser()

# LOGIC 4: Create the Chain
# This combines the prompt template, chat model, and output parser into a single workflow.
chain = chat_prompt_template | chat_model | parser

# LOGIC 5: Streamlit User Interface
# This section creates a simple web interface for users to input their travel details.

# Set up the title of the web app
st.title(":airplane: AI-Powered Travel Planner")

# User inputs
source = st.text_input(label=":earth_asia: Source:", placeholder="Enter Your Source...")
destination = st.text_input(label=":earth_asia: Destination:", placeholder="Enter Your Destination...")
date = st.date_input(label=":calendar: Date:", value=None)

# Button to trigger the travel plan search
btn_click = st.button("Search for Available Trip Plans")

# If the button is clicked, process the user's input and display the results
if btn_click:
    # Prepare the raw input for the AI
    raw_input = {
        "source": source,
        "destination": destination,
        "date": date,
    }
    
    # Invoke the AI chain to get the travel recommendations
    travel_recommendations = chain.invoke(raw_input)
    
    st.write("### Here are your travel options:")
    st.write(Travel_recommendations)
