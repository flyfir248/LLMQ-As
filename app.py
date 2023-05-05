from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Step 1: Choose a pre-trained model architecture
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

# Step 3: Load the pre-trained model
try:
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
except OSError:
    print(f"Model not found locally. Downloading {model_name}...")
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Step 4: Define a tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

def clean_text(text):
    """
    Removes special characters from the given text
    """
    cleaned_text = ""
    for char in text:
        if char.isalnum() or char.isspace():
            cleaned_text += char
    return cleaned_text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        text = file.read().decode("utf-8")
        cleaned_text = clean_text(text)

        question = request.form["question"]

        inputs = tokenizer.encode_plus(question, cleaned_text, return_tensors="pt", max_length=512, truncation=True)

        outputs = model(**inputs)

        answer_start = outputs.start_logits.argmax(dim=-1).item()
        answer_end = outputs.end_logits.argmax(dim=-1).item()
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end+1]))

        return render_template("result.html", question=question, answer=answer)
    else:
        return render_template("question.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)