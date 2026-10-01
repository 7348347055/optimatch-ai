# OptiMatch AI
An AI-powered employability platform designed to bridge the gap between candidate qualifications and automated screening mechanisms (ATS).

## Architecture
Built locally using Streamlit for the frontend UI and a LangGraph multi-agent architecture (Profiler Agent, Benchmark Agent, Optimizer Agent) powered by LangChain and Google Generative AI.

## How to Run Locally
1. `python -m venv venv`
2. Activate the environment.
3. `pip install -r requirements.txt`
4. Add a `.env` file with `GOOGLE_API_KEY=your_api_key`
5. Run `streamlit run app.py`