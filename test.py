from flask import Flask, render_template_string

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Webcam Frame Analyzer + TTS + Timestamp</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">

  <style>
    body {
      background: linear-gradient(to right, #141e30, #243b55);
      color: #f1f1f1;
      padding: 30px;
      font-family: 'Segoe UI', sans-serif;
    }

    h2 {
      font-weight: bold;
      margin-bottom: 30px;
    }

    video {
      border: 6px solid white;
      border-radius: 10px;
      box-shadow: 0 0 20px #000;
    }

    #output {
      margin-top: 20px;
      padding: 15px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      font-size: 18px;
      color: #ffeb3b;
      font-weight: bold;
    }

    .spinner {
      border: 4px solid rgba(255, 255, 255, 0.1);
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border-left-color: #fff;
      animation: spin 1s linear infinite;
      margin: 20px auto;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>

  <script src="https://js.puter.com/v2/"></script>
</head>

<body>
  <div class="container text-center">
    <h2 class="text-warning">Live Webcam Frame Analyzer with AI & Voice</h2>

    <video id="camera" width="640" height="480" autoplay></video>
    <canvas id="canvas" width="640" height="480" style="display: none;"></canvas>

    <br>
    <button id="analyzeBtn" class="btn btn-light mt-4">🔍 Analyze Frame</button>

    <div id="output" class="mt-4"></div>
  </div>

  <script>
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const output = document.getElementById('output');
    const analyzeBtn = document.getElementById('analyzeBtn');

    function showSpinner() {
      output.innerHTML = '<div class="spinner"></div>';
    }

    function hideSpinner() {
      output.innerHTML = '';
    }

    function speakText(text) {
      const speech = new SpeechSynthesisUtterance(text);
      speech.lang = 'en-US';
      window.speechSynthesis.speak(speech);
    }

    analyzeBtn.onclick = () => {
      showSpinner();
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Add timestamp on canvas
      ctx.fillStyle = "white";
      ctx.font = "20px Arial";
      const now = new Date().toLocaleString();
      ctx.fillText(now, 10, 30);

      const imageData = canvas.toDataURL('image/png');

      puter.ai.chat("Describe this webcam frame", imageData)
        .then(response => {
          hideSpinner();
          const description = '🧠 AI Description: ' + response;
          output.innerText = description;
          speakText(response);
        })
        .catch(error => {
          hideSpinner();
          output.innerText = 'Error: Unable to get AI description.';
          console.error(error);
        });
    };

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        output.innerText = "Webcam access failed.";
        console.error(err);
      });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8082)
