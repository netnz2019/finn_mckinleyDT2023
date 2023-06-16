from flask import Flask, render_template    # Imports Flask Library

app = Flask(__name__) 

@app.route('/')    # Route to Homepage
def root():
  return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)