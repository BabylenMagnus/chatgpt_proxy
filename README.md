API Endpoint Compatibility ChatGPT API

## Using Docker
1. Run the following command:
   ```bash
   docker run -d --name chatgpt-proxy -p 9060:9000 evgeniy888/chatgpt-proxy:0.2
   ```
2. Done! You can now connect to your local server's API at:
   ```
   http://localhost:9060/v1
   ```
3. Using in practise
```python
from langchain_openai import ChatOpenAI

OPENAI_TOKEN = "your_token"
llm = ChatOpenAI(
    api_key=OPENAI_TOKEN, model="gpt-3.5-turbo", base_url="http://localhost:9060/v1"
)
llm.invoke("Расскажи анекдот про пиво за 200 рублей и Крым")
```

```python
import openai

openai.api_key = 'your_token'
openai.base_url = "http://localhost:9060/v1/"

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Расскажи анекдот про пиво за 200 рублей и Крым"},
    ],
)
```
