# model_interface.py

import panel as pn
import requests

def chat_callback(contents, user, instance):
    """Handle user input by sending it to the API and returning the response."""
    try:
        response = requests.post(
            "http://localhost:8000/query",
            json={"question": contents}
        )
        response.raise_for_status() 
        answer = response.json().get("response", "No response received.")
    except requests.RequestException as e:
        answer = f"Error: Could not connect to the API. {str(e)}"
    return answer

chat_interface = pn.chat.ChatInterface(
    callback=chat_callback,
    user="You",
    show_clear=False,
    show_undo=False,
    sizing_mode="stretch_both",
    avatar="👤",
    widgets=[pn.chat.ChatAreaInput(placeholder="Ask a question about the database...")],
)

layout = pn.Column(
    "# Database Query",
    chat_interface,
    sizing_mode="stretch_both"
)

def get_layout():
    """Return the layout for the database query interface."""
    return layout

if __name__ == "__main__":
    pn.serve(
        layout,
        show=True,
        title="Database Query Interface",
    )