---
description: "Toggle Playwright MCP server on/off to save context tokens"
---

# Toggle Playwright MCP

Toggle the Playwright MCP server to save ~14k tokens when not needed.

## Action: $ARGUMENTS

If argument is "on" or "enable":
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

If argument is "off" or "disable":
```bash
claude mcp remove playwright
```

If no argument or "status":
```bash
claude mcp list
```

## Usage

- `/toggle-playwright on` - Enable Playwright MCP
- `/toggle-playwright off` - Disable Playwright MCP
- `/toggle-playwright` - Show current MCP status
