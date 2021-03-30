FROM datascience-prd
EXPOSE 5000
ENTRYPOINT source /venv/bin/activate && python api.py