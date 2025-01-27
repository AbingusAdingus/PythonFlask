from flask import Flask, request, jsonify
import os
import logging 
app = Flask(__name__)
if not app.debug:  # Only configure logging when not in debug mode
    logging.basicConfig(level=logging.INFO)  # Adjust level to INFO, DEBUG, etc.
    app.logger.setLevel(logging.INFO)
    
@app.route('/webhook/<endpoint>', methods=['POST'])
def dynamic_webhook(endpoint):
    print("Starting Now")
    print("Headers:", request.headers)  # Print request headers
    print("Raw Data:", request.data)    # Print raw payload
    
    # Safely attempt to parse JSON
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON in request")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        # Respond with "I love you" on JSON parse failure
        return jsonify({"response": "I love you"}), 200
    app.logger.info(f"Received data for {endpoint}: {data}")
    print(f"Received data for {endpoint}: {data}")
    # Respond with "I love you" for valid requests
    return jsonify({"response": "I love you"}), 200

if __name__ == '__main__':
    print("About to start")
    # Use the PORT environment variable if available, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
