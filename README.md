# Instructions

## Installation
To install everything that is required run the following command:
```bash
make install
```

## Running
First you must export your OpenAI API key, you can do this by running the command below:
```bash
export OPENAI_API_KEY=<your-api-key>
```

Next run the command:
```bash
make run
```

This will create a tmux session with mouse controll enabled. The left side is the chat interface while the right side is the approvals interface. When you send a message that requires tool calling the execution will stall. To approve or reject the tool use type `list` in the approvals interface this will show the approval request for the tool call. Next either type `accept` or `reject` followed by the approval request id (the UUID shown when the `list` command is run). Tab completion is available for autocompleting the approval request ids.

To stop the tmux session click `<Ctrl>-b` and then `: kill-session`
