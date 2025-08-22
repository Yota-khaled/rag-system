from flask import Flask, render_template, request, jsonify
from rag_functions import read_pdf, split_text, create_chromadb, search_db, generate_answer, close_and_delete_db



app = Flask(__name__)

db_instance = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    global db_instance
    file = request.files.get("pdf")
    if file:
            if db_instance:
                close_and_delete_db()
                db_instance = None

            text = read_pdf(file)
            chunks = split_text(text)
            db_instance = create_chromadb(chunks)

            return jsonify({"status": "success", "message": "PDF processed successfully."})
    return jsonify({"status": "error", "message": "No file uploaded"}), 400

@app.route("/chat", methods=["POST"])
def chat():
    global db_instance
    user_message = request.json.get("message", "")

    if not db_instance:
        return jsonify({"reply": "Please upload a PDF first."})

    context = search_db(db_instance, user_message, k=3)

    bot_reply = generate_answer(context, user_message)

    if not bot_reply or "not possible to answer" in bot_reply.lower():
        bot_reply = "Sorry, I couldn't understand your question. Could you rephrase it?"


    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
