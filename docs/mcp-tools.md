# mcpwright — The 23 MCP tools

The Playwright MCP server exposes 23 tools. Here they are, grouped.

## Navigation

| Tool | What it does |
|---|---|
| `browser_navigate` | Open a URL |
| `browser_navigate_back` | Go back |
| `browser_close` | Close the browser |

## Page interaction

| Tool | What it does |
|---|---|
| `browser_click` | Click an element (by ref or selector) |
| `browser_hover` | Hover over an element |
| `browser_type` | Type into an input (real keyboard) |
| `browser_select_option` | Select a `<select>` option |
| `browser_drag` | Drag element A to element B |
| `browser_press_key` | Press a key (Enter, Tab, Escape, etc.) |

## Page state

| Tool | What it does |
|---|---|
| `browser_snapshot` | Get the page's accessibility tree (best for LLM context) |
| `browser_take_screenshot` | Save a PNG screenshot |
| `browser_evaluate` | Run arbitrary JavaScript in the page |
| `browser_get_console_logs` | Read browser console messages |

## Browser control

| Tool | What it does |
|---|---|
| `browser_resize` | Resize the browser window |
| `browser_handle_dialog` | Accept/dismiss alert/confirm/prompt dialogs |
| `browser_file_upload` | Upload a file via input |
| `browser_install` | Install the browser (if not yet installed) |

## Tabs

| Tool | What it does |
|---|---|
| `browser_tabs` | List / open / close / select tabs |
| `browser_tab_new` | Open a new tab |
| `browser_tab_select` | Switch to a tab |
| `browser_tab_close` | Close a tab |

## Wait / timing

| Tool | What it does |
|---|---|
| `browser_wait_for` | Wait for a time, a selector, or a JS condition |

## Tips

- **`browser_snapshot`** is your best friend. It returns a structured
  representation of the page (the accessibility tree) that's perfect for
  LLM context. Use it instead of screenshots whenever possible — it's
  faster and token-cheap.
- **`browser_evaluate`** is the escape hatch. If a tool doesn't exist for
  what you need, run JS. Returns the value of the last expression.
- **`browser_take_screenshot`** writes to the MCP server's working
  directory. If you need the path, parse it from the response.

## Calling any tool

The pattern is always:

```python
send({"jsonrpc": "2.0", "id": <N>, "method": "tools/call",
      "params": {"name": "<TOOL_NAME>",
                 "arguments": {<TOOL_SPECIFIC_ARGS>}}})
response = recv(<TIMEOUT>)
```

The response has the shape:

```json
{"jsonrpc": "2.0", "id": <N>, "result": {
    "content": [{"type": "text", "text": "..."}]
}}
```

`content[0].text` is always a human-readable string describing the
result. For tools that return rich data, you may need to parse it
(JSON, file path, etc).
