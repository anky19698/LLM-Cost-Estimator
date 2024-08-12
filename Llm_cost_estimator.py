import tiktoken
import streamlit as st

def get_cost_per_token(cost_per_million):
    return cost_per_million/1000000

model_costs = {
    "GPT 3.5 Turbo": {
        "name": "gpt-3.5-turbo",
        "input_cost": get_cost_per_token(1.5),
        "output_cost": get_cost_per_token(2)
    } , 
    "GPT 4": {
        "name": "gpt-4",
        "input_cost": get_cost_per_token(30),
        "output_cost": get_cost_per_token(60)
    },
    "GPT 4 Turbo": {
        "name": "gpt-4-turbo",
        "input_cost": get_cost_per_token(10),
        "output_cost": get_cost_per_token(30)
    },
    "GPT 4o": {
        "name": "gpt-4-o",
        "input_cost": get_cost_per_token(5),
        "output_cost": get_cost_per_token(15)
    },
    "Gemini 1.0 Pro":{
        "name": "gemini-1.0-pro",
        "input_cost": get_cost_per_token(0.5),
        "output_cost": get_cost_per_token(1.5)
    },
    "Gemini 1.5 Pro":{
        "name": "gemini-1.5-pro",
        "input_cost": get_cost_per_token(4),
        "output_cost": get_cost_per_token(12)
    },
    "Gemini 1.5 Flash":{
        "name": "gemini-1.5-flash",
        "input_cost": get_cost_per_token(0.1),
        "output_cost": get_cost_per_token(0.4)
    }
}


# Funcion for Calculating Tokens
def calculate_tokens(text):
    # Using Same Tokenizer for All
    encoder = tiktoken.encoding_for_model(model_name="gpt-3.5-turbo")
    tokens = encoder.encode(text)
    return len(tokens)

# Function to Estimate Monthly Costs
def get_monthly_cost(tokens, token_type, model, requests_per_day):
    if token_type == 'input':
        # print(tokens, requests_per_day, model_costs[model]['input_cost'])
        cost = tokens * requests_per_day * model_costs[model]['input_cost']
    else:
        # print(tokens, requests_per_day,model_costs[model]['output_cost'])
        cost = tokens * requests_per_day * model_costs[model]['output_cost']
    return round(cost,2)


def main():
    # Streamlit Title
    st.title(":money_with_wings: LLM Cost Estimator:money_with_wings:")

    # Model Selection
    model = st.selectbox("Select Model", options=list(model_costs.keys()))
    model_name = model_costs[model]['name']


    input_col , output_col = st.columns(2)

    with input_col:
        # User Input
        default_input = "You are a AI Python Assistant, Your task is to Help User with Python Queries. Always Ask if User has any Queries"
        input_prompt = st.text_area("Enter your Input Prompt Here", height=200, value=default_input)

    with output_col:
        # Sample Output
        default_output = "Hi There, You can ask Any Queries related to Python."
        sample_output = st.text_area("Enter your Sample Output Here", height=200, value=default_output)

    # Request Per Day
    requests_per_day = st.number_input("Enter Requests Per Day", min_value=1, max_value=1000000, value=1000)

    # Custom CSS for button styling
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #173928; /* Dark green background */
            color: #98FB98; /* Light green text */
            border-radius: 5px;
            padding: 10px;
        }
        div.stButton > button:first-child:hover {
            background-color: #228B22; /* Slightly lighter green on hover */
            color: #E0FFE0; /* Lighter green text on hover */
        }
        </style>
        """, unsafe_allow_html=True)

    # Calculate Button
    if st.button("Calculate Monthly Costs"):
        if input_prompt and sample_output:

            # Get Token Count
            input_tokens = calculate_tokens(input_prompt)
            output_tokens = calculate_tokens(sample_output)
            # st.write(f'Token Count: {tokens}')
            

            # Get Monthly Costs
            input_cost = get_monthly_cost(tokens=input_tokens, token_type='input', model=model, requests_per_day=requests_per_day)
            output_cost = get_monthly_cost(tokens=output_tokens, token_type='output', model=model, requests_per_day=requests_per_day)

            # print(input_cost, output_cost)
            # st.write(f'Estimated Cost Per Month: ${cost}')

            # Hoverable Box
            st.markdown(
                """
                <style>
                .custom-box {
                    transition: all 0.1s ease;
                    border: 2px solid transparent;
                }

                .custom-box:hover {
                    transform: scale(1.1);
                    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.5); 
                }
                
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Create columns for each box
            col1, col2 = st.columns(2)
            
            # Display each field in an enclosed box
            with col1:
                # Token Box
                st.markdown(
                    f"""
                    <div class="custom-box" style='background-color: #003366; border-radius: 5px; padding: 10px; text-align: center;'>
                        <span style='color: #B3D9FF;'>Input Token Count:<br> <b style= 'font-size: 50px;'>{input_tokens}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                # Token Box
                st.markdown(
                    f"""
                    <div class="custom-box" style='background-color: #003366; border-radius: 5px; padding: 10px; text-align: center;'>
                        <span style='color: #B3D9FF;'>Output Token Count:<br> <b style= 'font-size: 50px;'>{output_tokens}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write("""


            """)
            
            # Create columns for each box
            col3, col4 = st.columns(2)
                
            with col3:
                # Cost Box

                st.markdown(
                    f"""
                    <div class="custom-box" style='background-color: #3E3C15; border-radius: 5px; padding: 10px; text-align: center;'>
                        <span style='color: #FFFFBC;'>Estimated Daily Costs:<br> <b style= 'font-size: 50px;'>${round(input_cost+output_cost, 2)}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with col4:
                # Cost Box

                st.markdown(
                    f"""
                    <div class="custom-box" style='background-color: #3E2327; border-radius: 5px; padding: 10px; text-align: center;'>
                        <span style='color: #FFDEDE;'>Estimated Monthly Costs:<br> <b style= 'font-size: 50px;'>${round((input_cost+output_cost)*30, 2)}</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        else:
            st.error("Please Enter the Input/Output Samples")

if __name__ == '__main__':
    main()