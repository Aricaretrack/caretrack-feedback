from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        notestr_features = request.form.get("notestr_features")
        additional_features = request.form.get("additional_features")
        file = request.files.get("screenshot")
        if file and file.filename:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

        with open("feedback.txt", "a") as f:
            f.write(f"NotesTr Features: {notestr_features}\n")
            f.write(f"Additional Features: {additional_features}\n")
            if file and file.filename:
                f.write(f"Uploaded Screenshot: {file.filename}\n")
            f.write("\n")

        return redirect(url_for("index"))

    return """
    <html>
        <head>
            <title>CareTrack Feedback Portal</title>
        </head>
        <body>
            <h2>Provide Feedback on NotesTr & Features</h2>
            <form method="POST" enctype="multipart/form-data">
                <label>Describe NotesTr Features:</label><br>
                <textarea name="notestr_features" rows="4" cols="50"></textarea><br><br>
                <label>Additional Features You Want:</label><br>
                <textarea name="additional_features" rows="4" cols="50"></textarea><br><br>
                <label>Upload Screenshot (optional):</label><br>
                <input type="file" name="screenshot"><br><br>
                <input type="submit" value="Submit Feedback">
            </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
