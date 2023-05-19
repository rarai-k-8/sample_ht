from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("line-corporation/line-distilbert-base-japanese", trust_remote_code=True)
model = AutoModel.from_pretrained("line-corporation/line-distilbert-base-japanese")
# sentence = "LINE株式会社で[MASK]の研究・開発をしている。"
# print(model(**tokenizer(sentence, return_tensors="pt")))
def word2vec_BERT(word):
    output = model(**tokenizer(word, return_tensors="pt"))
    last_hidden_states = output.last_hidden_state
    last_hidden_states_np = last_hidden_states.detach().numpy()
    vector = last_hidden_states_np[0][1]
    return vector