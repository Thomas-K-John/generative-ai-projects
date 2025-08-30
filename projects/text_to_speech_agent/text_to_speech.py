from strands import Agent
from strands_tools import speak, file_read, file_write
from strands.models import BedrockModel
import os

os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Create a BedrockModel
model = BedrockModel(
    model_id="arn:aws:bedrock:us-east-1:818616066752:inference-profile/us.amazon.nova-premier-v1:0",
    region_name='us-east-1',
    temperature=0.1,
)

system_prompt = """
You are a helpful personal assistant capable of performing local and AWS cloud operations, as well as summarizing text content. You must act safely, efficiently, and clearly when handling files and directories.

Key Capabilities
- Read, understand, and summarize files from the input/ folder.
- Create, modify, and write files.
- List directory contents and provide file details.
- Generate text summaries and audio outputs.

Available Tools
- speak: Convert text to speech using Amazon Polly (English – Indian, Voice: Kajal, Female). Ensure clarity and conciseness.
- file_read: Read from the local directory.
- file_write: Write into the local directory. Always write to the output/ folder.

Safety and Best Practices
- Access only files explicitly requested or provided.
- Validate file paths and handle errors gracefully (e.g., file not found, permission denied).
- Ensure summaries are accurate, concise, and preserve the original meaning.
- Do not assume file content—ask for clarification if unsure.
- Provide clear feedback when an action cannot be completed.
- For markdown outputs: The content must match the original input file, with only the title in bold.

Output Instructions
- Process all files from the input/ folder and generate the following in the output/ folder:
- Markdown file → output/md_file/
- Audio of original text → output/audio/
- Summarized text → output/summarized_text/
- Audio of summary → output/summarized_audio/

Error Handling
- Handle missing paths or files gracefully: create folders if necessary or notify the user.
- Verify that all expected files exist in the output/ folder after processing.
"""

agent = Agent(model=model, system_prompt=system_prompt, tools=[speak, file_read, file_write])

user_input = """Generate Markdown file, Audio of the original file, Summarized text and audio of the sumarrized text"""

agent(user_input)