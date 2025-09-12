echo [$(date)]: "START"
echo [$(date)]: "creating env with python version 3.8"
conda create --prefix ./RAGenv python==3.8 -y
echo [$(date)]: "activating the environment"
source activate ./RAGenv
echo [$(date)]: "installing the dev requirements"
pip install -r requirements.txt
echo [$(date)]: "NOW RUNNIG app.py"
uvicorn app:app --reload
echo [$(date)]: "ALL COMMANDS COMPLETED!!!"