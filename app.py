from flask import Flask, render_template_string, request, session
from booking import BookingSystem
from faq import FAQHandler
from main import parse_date, parse_time, parse_intent
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

booking_system = BookingSystem()
faq_handler = FAQHandler(booking_system)


HELP_TEXT = """
How can I help you today?

  - Type "book" to schedule a two-hour appointment
  - Type "services" to see what services we offer
  - Type "locations" to see which areas we serve
  - Type "quit" to exit

You can also ask questions like:
  - "I need to book an appointment"
  - "What services do you offer?"
  - "Where are you located?"
"""

def handle_message(user_input: str) -> str:
    """Process user message and return response."""
    user_input = user_input.strip()
    if not user_input:
        return ""

    booking_state = session.get("booking_state")
    if booking_state:
        return handle_booking_flow(user_input, booking_state)

    intent = parse_intent(user_input)

    if intent == "book":
        session["booking_state"] = {"step": "name"}
        return "Let's book an appointment!\n\nWhat is your name?"
    elif intent == "locations":
        return faq_handler.get_locations_response()
    elif intent == "services":
        return faq_handler.get_services_response()
    elif intent == "help":
        return HELP_TEXT
    elif intent == "exit":
        return "Thank you for using our service. Goodbye! (Refresh to start over)"
    else:
        return "I'm not sure I understand. Type 'help' to see what I can do, or 'book' to schedule an appointment."


def handle_booking_flow(user_input: str, state: dict) -> str:
    """Handle multi-step booking flow."""
    step = state.get("step")
    services = booking_system.get_available_services()
    zones = booking_system.get_service_zones()

    if user_input.lower() in ["cancel", "quit", "exit"]:
        session.pop("booking_state", None)
        return "Booking cancelled.\n\n" + HELP_TEXT

    if step == "name":
        if not user_input:
            return "Name is required. What is your name?"
        state["customer_name"] = user_input
        state["step"] = "service"
        session["booking_state"] = state
        return f"Nice to meet you, {user_input}!\n\nAvailable services: {', '.join(s.title() for s in services)}\n\nWhat service do you need?"

    elif step == "service":
        service = user_input.lower()
        if service not in services:
            return f"Sorry, '{user_input}' is not a valid service.\n\nAvailable: {', '.join(s.title() for s in services)}"
        state["service"] = service
        state["step"] = "zip"
        session["booking_state"] = state
        return f"We serve: {', '.join(zones)}\n\nWhat is your zip code?"

    elif step == "zip":
        if user_input not in zones:
            return f"Sorry, we don't serve '{user_input}'.\n\nWe serve: {', '.join(zones)}"
        state["zip_code"] = user_input
        state["step"] = "date"
        session["booking_state"] = state
        return "What date would you like? (e.g., 2025-02-15 or Feb 15, 2025)"

    elif step == "date":
        date = parse_date(user_input)
        if date is None:
            return f"Could not parse '{user_input}'.\n\nPlease use a format like '2025-02-15' or 'February 15, 2025'."
        state["date"] = date
        state["step"] = "time"
        session["booking_state"] = state
        return "What time would you like? (e.g., 10:00 AM or 2pm)"

    elif step == "time":
        time = parse_time(user_input)
        if time is None:
            return f"Could not parse '{user_input}'.\n\nPlease use a format like '10:00 AM' or '2pm'."
        message = booking_system.book_appointment(
            customer_name=state["customer_name"],
            service=state["service"],
            zip_code=state["zip_code"],
            date=state["date"],
            time=time,
        )
        session.pop("booking_state", None)
        return message

    return "Something went wrong. Type 'book' to start over."


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CSR Chat Bot</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { text-align: center; color: #333; }
        #chat {
            background: white;
            border-radius: 10px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
            white-space: pre-wrap;
        }
        .user { background: #007bff; color: white; margin-left: auto; text-align: right; }
        .bot { background: #e9ecef; color: #333; }
        #input-form { display: flex; gap: 10px; }
        #user-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        #user-input:focus { border-color: #007bff; }
        button {
            padding: 12px 25px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>Customer Service Chat Bot</h1>
    <div id="chat"></div>
    <form id="input-form">
        <input type="text" id="user-input" placeholder="Type a message..." autocomplete="off">
        <button type="submit">Send</button>
    </form>
    <script>
        const chat = document.getElementById('chat');
        const form = document.getElementById('input-form');
        const input = document.getElementById('user-input');

        function addMessage(text, isUser) {
            const div = document.createElement('div');
            div.className = 'message ' + (isUser ? 'user' : 'bot');
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        addMessage(`Welcome to the Customer Service Chat Bot!

How can I help you today?
• Type "book" to schedule a two-hour appointment
• Type "services" to see what services we offer
• Type "locations" to see which areas we serve`, false);

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, true);
            input.value = '';
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            if (data.response) addMessage(data.response, false);
        });

        input.focus();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    session.clear()
    return render_template_string(HTML_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response = handle_message(user_message)
    return {"response": response}


if __name__ == "__main__":
    print("Starting web server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
