# qa-chat-bot

Чат-бот для автоматизации технической поддержки

Репозиторий с экспериментами и наработками: <https://github.com/ath-elephants/research>

Развернуть в Docker на сервере можно с помощью следующего набора команд:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends git

git clone https://github.com/ath-elephants/qa-chat-bot.git
cd qa-chat-bot

chmod +x setup.sh
./setup.sh
```

Чтобы протестировать чат-бота локально, достаточно запустить следующие команды:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends git

git clone https://github.com/ath-elephants/qa-chat-bot.git
cd qa-chat-bot

python -m venv .venv
source .venv/bin/activate

pip install -r ./api/requirements-api.txt
pip install -r ./ui/requirements-ui.txt

curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma2:2b

uvicorn api.main:app --reload --host 95.161.221.20 --port 8000
streamlit run ui/app.py 
```

Используемый стек технологий:

- [RAG LangChain](https://python.langchain.com/v0.2/docs/introduction/)
- [LLM google/gemma-2-2b](https://huggingface.co/google/gemma-2-2b-it)
- [эмбединги ai-forever/ru-en-RoSBERTa](https://huggingface.co/ai-forever/ru-en-RoSBERTa)
- [backend FastAPI](https://fastapi.tiangolo.com/)
- [UI Streamlit](https://streamlit.io/)
- [Docker + docker compose](https://docs.docker.com/compose/)
