from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Function to scrape phone numbers
def scrape_phone_numbers(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve the website"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Improved regex
        phone_numbers = re.findall(r'\+?[\d\s()-]{7,15}', soup.get_text())
        
        if phone_numbers:
            return list(set(phone_numbers))  # Remove duplicates
        else:
            return "No phone numbers found"
    except Exception as e:
        return f"An error occurred while scraping: {e}"
        
# Route to display the form and handle form submissions
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the URL entered by the user
        url = request.form.get("url")
        if url:
            phone_numbers = scrape_phone_numbers(url)
            return render_template("index.html", phone_numbers=phone_numbers, url=url)
        else:
            return render_template("index.html", error="Please provide a valid website link.")
    return render_template("index.html")

# Additional route for "Automate Call" functionality
@app.route("/automate_call", methods=["POST"])
def automate_call():
    try:
        data = request.get_json()
        phone_numbers = data.get("phone_numbers", [])
        
        # Simulate call automation response
        results = [{"number": num, "status": "Call scheduled"} for num in phone_numbers]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Failed to automate calls: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")  # Allows access in environments like Codespaces
