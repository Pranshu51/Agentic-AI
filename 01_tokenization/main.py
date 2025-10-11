#pip install tiktoken => it is made by openai it helps in tokenize nd detokenize the text
#to create requirements.txt file => pip freeze > requirements.txt

import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you?"
tokens = enc.encode(text)

#Tokens: [13225, 11, 1495, 553, 481, 30]
print("Tokens:", tokens)

#detokenize
decoded = enc.decode([13225, 11, 1495, 553, 481, 30])
print("Decoded:", decoded)