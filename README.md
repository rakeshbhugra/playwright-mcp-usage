# Playwright MCP Usage - Automated Job Application Bot

An automated job application system that uses Playwright MCP (Model Context Protocol) to apply for jobs on workday platforms. The bot can read your resume from a PDF file and automatically fill out job applications.

## Demo Video

[![Demo Video](https://img.shields.io/badge/▶️-Watch%20Demo%20Video-red?style=for-the-badge)](https://rakeshbhugra-website-assets.s3.ap-south-1.amazonaws.com/job-application-demo.mp4)

**[Click here to watch the demo video](https://rakeshbhugra-website-assets.s3.ap-south-1.amazonaws.com/job-application-demo.mp4)**

*Note: The video is sped up for demonstration purposes. The actual process takes longer as the bot carefully fills out each field.*

## Features

- 🤖 **Automated Job Applications**: Automatically searches and applies for jobs on NVIDIA's Workday platform
- 📄 **Resume PDF Reading**: Extracts information from your resume PDF to fill application forms
- 🎯 **Smart Job Matching**: Uses resume details to find and apply for relevant positions
- 🔧 **Manual Form Filling**: Fills each field individually for better accuracy
- 🔄 **Multi-tool Support**: Handles multiple browser actions in sequence

## Prerequisites

- Python 3.12+
- UV package manager
- Chrome browser (for Playwright automation)
- Environment variables for login credentials

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd playwright-mcp-usage
   ```

2. **Initialize the project with UV**
   ```bash
   uv sync
   ```
   
   Or if starting fresh:
   ```bash
   uv init
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   WORKDAY_EMAIL=your-email@example.com
   WORKDAY_PASS=your-password
   ```

4. **Add your resume**
   Place your resume PDF in the `data_files/resumes/` directory.

## Usage

Run the automated job application bot:

```bash
python -m main
```

The bot will:
1. Read your resume from the PDF file
2. Navigate to Google and search for NVIDIA jobs
3. Go to NVIDIA's Workday job portal
4. Login with your credentials
5. Search for jobs matching your resume
6. Apply for suitable positions by filling forms manually

## Project Structure

```
playwright-mcp-usage/
├── src/
│   ├── agent_graph/          # LangGraph workflow definition
│   │   ├── agent.py         # Main agent orchestrator
│   │   ├── graph.py         # Graph structure and routing
│   │   ├── state.py         # State management
│   │   └── nodes/           # Individual workflow nodes
│   └── utils/
│       ├── llm/             # LLM integration utilities
│       ├── read_resume.py   # PDF resume reader
│       └── get_prompt_with_resume_details.py
├── data_files/
│   └── resumes/             # Place your resume PDFs here
├── main.py                  # Entry point
└── pyproject.toml          # Dependencies
```

## Implementation Status

### ✅ Current Features
- Resume PDF reading and text extraction
- Automated browser navigation
- Job search and application form filling
- Multi-tool call handling
- Error recovery mechanisms

### 🚧 Pending Features
- **Human-in-the-loop interaction**: Currently, the bot runs autonomously without user intervention
- **Interactive job selection**: Allow users to review and approve job applications before submission
- **Application status tracking**: Monitor submitted applications
- **Multi-platform support**: Extend beyond NVIDIA Workday to other job platforms

## Technical Details

### Architecture
- **LangGraph**: State management and workflow orchestration
- **MCP (Model Context Protocol)**: Browser automation via Playwright
- **LiteLLM**: LLM integration for decision making
- **PyMuPDF/PyPDF2**: PDF text extraction

### Key Components
- **ReasoningNode**: Makes decisions about next actions
- **ToolUseNode**: Executes browser automation commands
- **State Management**: Tracks conversation history and tool calls

## Known Issues

- **Recursion Limits**: The current implementation may hit LangGraph recursion limits on complex workflows
- **No Human Oversight**: The bot applies for jobs automatically without user review
- **Single Platform**: Currently only supports NVIDIA Workday platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security Notes

- Never commit credentials to the repository
- Use environment variables for sensitive information
- Review all job applications before actual submission (when human-in-the-loop is implemented)

## License

[Add your license here]

## Disclaimer

This tool is for educational and automation purposes. Always review job applications before submission and ensure compliance with the terms of service of job platforms.