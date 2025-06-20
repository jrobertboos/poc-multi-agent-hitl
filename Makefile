.PHONY: install run start-session tool-stack multi-agent-mcp quota-mcp stack hitl-server ui attach-session stop

SESSION_NAME = hitl

install:
	pip install -r requirements.txt
	pip install -e quota-limiter/
	pip install -e hitl-agent/

start-session:
	python chat.py

tool-stack:
	llama stack run tool-stack/run.yml --port 8003

multi-agent-mcp:
	python servers/multi-agent/server.py

quota-mcp: 
	FASTMCP_PORT=8001 python servers/quota/server.py

stack:
	llama stack run stack/run.yml

hitl-server:
	python hitl-server/server.py

ui:
	python approvals.py
