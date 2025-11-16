# Constellate 🌟

## About
Constellate is a lightweight web app for machine learning communities to collaboratively curate and discuss research articles.

## Authors
OstarkovSN, Cursor ;)

## Key features
📌 Submit & Tag: Submit PDFs or arXiv links and add custom tags (e.g., "transformers," "LLMs").

🔗 Knowledge Graph: Explore papers as interconnected nodes where edges form automatically via shared tags and using LLM-created embeddings. Drag, zoom, and hover to see LLM-generated summaries.

👍 Community Curation: Vote on papers and assign presenters with one click; the graph dynamically highlights trending/assigned items.

🛠️ Full customization: Modular code for effortless tweaks, core LLM engine may be easilly changed (choose existing or create your own agent in `models/` dir), then modify `CONSTELLATE_DEFAULT_AGENT` env variable.

## Installation
1. Install [pixi](https://pixi.sh/dev/installation/)
2. Clone the repository
3. Use pixi to install dependencies:
   ```shell
   pixi install -e prod
   ```

 ## Run the app
 ```shell
pixi run start
```

## Collaboration
Feel free to suggest your ideas by creating issues on github

