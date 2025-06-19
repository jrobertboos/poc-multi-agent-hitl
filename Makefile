.PHONY: install run start-session tool-stack multi-agent-mcp quota-mcp stack hitl-server ui attach-session stop

SESSION_NAME = hitl

install:
	pip install -r requirements.txt

run: start-session tool-stack multi-agent-mcp quota-mcp stack hitl-server ui attach-session

start-session:
	tmux new-session -d -s $(SESSION_NAME) -n ui '\
	while ! nc -z localhost 8321; do sleep 1; done && \
	python chat.py'

tool-stack: start-session
	tmux new-window -t $(SESSION_NAME): -n tool-stack 'cd tool-stack && llama stack run run.yml --port 8003'

multi-agent-mcp: tool-stack
	tmux new-window -t $(SESSION_NAME): -n multi-agent-mcp '\
	while ! nc -z localhost 8003; do sleep 1; done && \
	cd servers/multi-agent && python server.py'

quota-mcp: start-session
	tmux new-window -t $(SESSION_NAME): -n quota-mcp 'cd servers/quota && FASTMCP_PORT=8001 python server.py'

stack: start-session multi-agent-mcp quota-mcp
	tmux new-window -t $(SESSION_NAME): -n stack '\
	while ! nc -z localhost 8000; do sleep 1; done && \
	while ! nc -z localhost 8001; do sleep 1; done && \
	cd stack && llama stack run run.yml'

hitl-server: start-session
	tmux new-window -t $(SESSION_NAME): -n hitl-server 'cd hitl-server && python server.py'

ui: stack hitl-server
	tmux split-window -h -t $(SESSION_NAME):ui 'python approvals.py'

attach-session:
	tmux set-option -t $(SESSION_NAME) mouse on
	tmux select-window -t $(SESSION_NAME):ui
	tmux attach-session -t $(SESSION_NAME)

stop:
	-tmux kill-session -t $(SESSION_NAME) 2>/dev/null || true
