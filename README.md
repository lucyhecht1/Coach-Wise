# CoachWise: Making Coaching Accessible
**CoachWise** is an AI-powered web application designed to assist basketball coaches in creating, refining, and visualizing custom basketball plays. The site offers two core functionalities: creating **offensive plays** and/or **inbounds plays**, both tailored to your team’s specific needs.


## Features
* **Team Setup:** Input player names, strengths, and weaknesses in addition to the other team's defensive settup.
* **Play Creation:** Generate AI-crafted offensive and inbounds plays that maximize said strengths and minimize said weaknesses.
* **Visualization:**  Draw plays on a basketball court canvas for better clarity.
* **Refinement:** Adjust plays dynamically, factoring in player performance (e.g., off shooting nights).
* **Download:** Export plays as a PDF, complete with diagrams and formatted details.

## Technologies Used
* Frontend: HTML, CSS, Javascript, jQuery, Bootstrap for responsive UI
* Backend: Flask (Python) for web framework, OpenAI API for generating plays
* Other tools: jsPDF for PDF generation, HTML5 Canvas for play drawing

## Installation
**Note:** You must have a valid OpenAI API key to run this program.

Clone this repository:
```
git clone https://github.com/your-username/Coach-Wise.git
```
Navigate to the project directory:
```
cd Coach-Wise
```
Install dependencies:
```
npm install
pip install flask
```
**Set up the Environment Variables**
Create a ``.env`` file in the project root directory to securely store your OpenAI API key. Add the following line to the ``.env`` file:
```
OPENAI_API_KEY="your-api-key"
```
**Run the server locally:**
```
python server.py
```
**Open the application in your browser:** 
```
http://127.0.0.1:5000
```

## Demo of all features:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Xi0elcormQA/0.jpg)](https://www.youtube.com/watch?v=Xi0elcormQA)



