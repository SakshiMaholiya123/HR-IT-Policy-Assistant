import sys
import os


# -------------------------------------------------
# Add project root to Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(PROJECT_ROOT)


# -------------------------------------------------
# Imports
# -------------------------------------------------
import streamlit as st

from agents.policy_agent import policy_agent
from agents.dependencies import AgentDependencies

from tools.calculator_tool import LeaveNoticeCalculator
from tools.retriever_tool import PolicyRetrieverTool
from tools.date_tool import DateTool



# -------------------------------------------------
# Streamlit Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Nimbus HR & IT Policy Assistant",
    page_icon="🤖",
    layout="centered"
)



# -------------------------------------------------
# Load Agent
# -------------------------------------------------
@st.cache_resource
def load_agent():
    return policy_agent


agent = load_agent()



# -------------------------------------------------
# Load Agent Dependencies
# -------------------------------------------------
@st.cache_resource
def load_dependencies():

    retriever = PolicyRetrieverTool()

    calculator = LeaveNoticeCalculator()

    date_tool = DateTool()

    return AgentDependencies(
        retriever=retriever,
        calculator=calculator,
        date_tool=date_tool
    )

deps = load_dependencies()



# -------------------------------------------------
# Session Memory
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []



# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🤖 Nimbus HR & IT Policy Assistant")

st.write(
    """
    Ask questions related to:
    
    - HR Policies
    - Leave & Attendance
    - Remote Work
    - IT Security
    - Employee Benefits
    - Travel & Expense Policies
    """
)



# -------------------------------------------------
# Display Previous Messages
# -------------------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# -------------------------------------------------
# User Input
# -------------------------------------------------
user_query = st.chat_input(
    "Ask your policy related question..."
)



if user_query:


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    with st.chat_message("user"):
        st.markdown(user_query)



    with st.chat_message("assistant"):

        with st.spinner(
            "Searching policy documents..."
        ):

            try:

                result = agent.run_sync(
                    user_query,
                    deps=deps
                )


                answer = result.output


            except Exception as e:

                answer = (
                    "Sorry, I was unable to process "
                    "your request.\n\n"
                    f"Error: {str(e)}"
                )


            st.markdown(answer)



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )