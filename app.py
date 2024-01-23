from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import string
import streamlit as st

# Global variables
previous_prompts = []  # list of tuples (prompt, response)
previous_response = ""  # latest response

# Define model and model config
model = CTransformers(
    model="models/llama-2-7b-chat.ggmlv3.q8_0.bin?download=true",
    model_type="llama",
    config={"max_new_tokens": 512, "temperature": 0.7},
)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["input_prompt"],
    template="""Write code in Python that does the following:
{input_prompt}

**Note:** I won't generate harmful or inappropriate code. Please be respectful in your prompts.
""",
)


def generate_code(input_prompt):
    global previous_response

    # Modify previous response if requested
    if "modify the previous prompt" in input_prompt.lower():
        prompt = f"""
Modify the following code:
{previous_response}
{input_prompt}
        """
    else:
        # Start a new prompt
        prompt = prompt_template.format(input_prompt=input_prompt)

    # Generate code using Llama
    response = model.invoke(prompt)

    # Update previous response and prompt history
    previous_response = response
    previous_prompts.append((input_prompt, response))

    # Prepare code for terminal output
    if isinstance(response, str):
        # Single-line output
        code_to_run = f"\n{response}\n"
    else:
        # Multi-line output (assume list of lines)
        code_to_run = "\n".join([f"\n{line}" for line in response]) + "\n"

    return code_to_run


st.title("Copilot")
st.write(
    "Enter a coding prompt and I'll write Python code for it. I can even modify existing code based on your instructions!"
)

# Get user input for prompt
user_prompt = st.text_area("Coding Prompt:", value="", height=100)

# Add submit button and trigger code generation on click
if st.button("Generate Code"):
    if user_prompt:
        generated_code = generate_code(user_prompt)

        # Display generated code and run it in Python terminal
        with st.echo():
            st.code(generated_code, language="python")

            # Execute code within the terminal (optional)
            # st.session_state["code_output"] = st.experimental_get_query_params().get(
            #     "code_output", ""
            # )
            # if st.session_state["code_output"]:
            #     try:
            #         exec(generated_code, {}, {})
            #         st.write("Output:")
            #         st.write(st.session_state["code_output"])
            #     except Exception as e:
            #         st.error(f"Error running code: {e}")

    else:
        st.error("Please enter a coding prompt before clicking 'Generate Code'")

# Sidebar for previous prompts and responses
with st.sidebar:
    st.header("Previous Prompts and Responses")
    for prompt, response in previous_prompts:
        st.write(f"**Prompt:** {prompt}")
        st.code(response, language="python")

# Note about responsible use
st.write(
    "**Remember:** I'm still under development. Please use me responsibly and avoid prompts that are harmful or unethical."
)

