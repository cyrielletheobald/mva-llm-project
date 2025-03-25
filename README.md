# mva-llm

Project for the LLM course by Cyrielle Théobald, Raphaël Faure and Victor Jéséquel

Here is the structure of the project : 
<pre>'''
.
├── data/                          # Input data and Chroma vector database
│   ├── chroma_db/                # Persistent Chroma database
│   ├── 9789240077263-...pdf      # Source PDF document
│   ├── dataset.xlsx              # Patient Data from the paper
│   ├── instructions.xlsx         # File with diseases descriptions for the "LLM alone" baseline
│
├── notebook/                     # Notebooks for experimentation
│   ├── __pycache__/             # Python cache
│   └── Archive/                 # Many samples from different prompts
│   └── experiment_comparison.ipynb # Main notebook for illustrating experimentation and evaluation
│
├── src/                          # Source code
│   ├── __init__.py              # Makes src a Python module
│   ├── config.py                # Configuration paths and system prompts
│   ├── dataprep.py              # Data loading and preprocessing
│   ├── inference.py             # Inference pipeline using vector DB or not. A lot of functions to use the baselines are here.
│   └── test.py                  # Test scripts got from the second baseline (in Python case)
│
├── article projet.pdf            # Project report or article
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── .gitignore                    # Files and folders to ignore in version control
'''</pre>
Based on the paper "Large Language Models for Interpretable Mental Health Diagnosis" from Brian Hyeongseok Kim, Chao Wang. 

Paper : http://arxiv.org/abs/2501.07653 
Title : LLM for interpretable mental health diagnosis (2025)
Abstract : 
We propose a clinical decision support system (CDSS) for mental health diagnosis that combines the strengths of large language models (LLMs) and constraint logic programming (CLP). Having a CDSS is important because of the high complexity of diagnostic manuals used by mental health professionals and the danger of diagnostic errors. Our CDSS is a software tool that uses an LLM to translate diagnostic manuals to a logic program and solves the program using an off-the-shelf CLP engine to query a patient's diagnosis based on the encoded rules and provided data. By giving domain experts the opportunity to inspect the LLM-generated logic program, and making modifications when needed, our CDSS ensures that the diagnosis is not only accurate but also interpretable. We experimentally compare it with two baseline approaches of using LLMs: diagnosing patients using the LLM-only approach, and using the LLM-generated logic program but without expert inspection. The results show that, while LLMs are extremely useful in generating candidate logic programs, these programs still require expert inspection and modification to guarantee faithfulness to the official diagnostic manuals. Additionally, ethical concerns arise from the direct use of patient data in LLMs, underscoring the need for a safer hybrid approach like our proposed method.


We have implemented the two baselines described in the article. All the functions are located in inference.py, and an illustration can be found in the notebook.

To extend the work presented in the article, we experimented with models using Chain of Thoughts, code-specialized models, and Retrieval-Augmented Generation (RAG). We also explored other logic programming languages.

We successfully reproduced the first baseline with similar results. However, we encountered significant reproducibility issues with the second baseline. Here are the main challenges we faced:

- Logic programming packages and languages are poorly handled by LLMs, resulting in numerous errors in the outputs.
- The inputs are very long with the prompts, and with current resources, LLMs struggle to avoid omissions and follow instructions accurately.
- The prompts required completion, making it difficult to achieve consistent results.

The qualitative impacts of our additions:

- The LLM expert did not have a positive impact.
- Chain of Thoughts negatively impacted the results. The models struggled to reason without omitting key details, and corrections often worsened the outcomes.
- RAG can be useful for automating processes that involve quoting symptoms.
- Code-oriented models did not significantly improve results, as the packages and languages are too obscure to be better handled by these models compared to others.

All in all, we believe that the approach presented in the paper is viable, but it does not fully address the challenges that make reproducing the results difficult. With more resources and time, several issues could have been avoided. One approach could involve fine-tuning the model to better align its outputs with the expected format. Additionally, a reinforcement learning (RL) approach such as GRPO, as discussed in class, could be highly effective in this context.
