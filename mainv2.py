import json
import os
import glob

def format_chat_to_html_v2(chat_file_path, output_dir):
    with open(chat_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        base_filename = os.path.basename(chat_file_path).split('.')[0]
        print(base_filename)  # Debugging print statement

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Chat Export</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f0f0f0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 10px; width: 100%; box-shadow: 0 1px 0.5px rgba(0, 0, 0, 0.13); display: flex; justify-content: space-between; }
        .left { background-color: #fff; text-align: left; }
        .right { background-color: #dcf8c6; text-align: right; }
        .container { display: flex; flex-direction: column; }
        .sender { width: 100%; }
    </style>
</head>
<body>
    <div class="container">
"""

    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split(' - ', 1)
        if len(parts) < 2:
            continue
        timestamp, message_part = parts
        html_content += "<br>"  # Line break before each message
        if ':' in message_part:
            sender, message = message_part.split(':', 1)
        else:
            # Here, handle the case where there is no ':' in message_part
            sender = "Unknown"  # Or any default sender name you prefer
            message = message_part  # Treat the entire part as the message

        if base_filename in sender:
            html_content += f'<div class="message left"><div class="sender">{timestamp} - {sender}: {message}</div></div>\n'
        else:
            html_content += f'<div class="message right"><div class="sender">{timestamp} - {sender}: {message}</div></div>\n'

    html_content += "</div></body></html>"

    output_file_path = os.path.join(output_dir, os.path.basename(chat_file_path).replace('.txt', '.html'))
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)
    print(f"Generated HTML file: {output_file_path}")  # Debugging print statement

def generate_chat_name_list(output_folder, js_file_path):
    # List all HTML files in the formatted_chats directory
    chat_files = [f for f in os.listdir(output_folder) if f.endswith('.html')]

    # Generate JavaScript code with the list of chat files
    js_code = f"const chatFiles = {json.dumps(chat_files)};"

    # Write the JavaScript code to the file
    with open(js_file_path, 'w') as js_file:
        js_file.write(js_code)

# Main code
chats_dir = 'chats_newformat'  # Source path for the text files
formatted_chats_dir = 'formatted_chats_new'  # Destination path for the HTML files
js_file_path = 'web/chatList.js'
os.makedirs(formatted_chats_dir, exist_ok=True)

if not glob.glob(os.path.join(chats_dir, '*.txt')):
    print("No .txt files found in the 'chats' directory.")

for chat_file in glob.glob(os.path.join(chats_dir, '*.txt')):
    format_chat_to_html_v2(chat_file, formatted_chats_dir)

generate_chat_name_list(formatted_chats_dir, js_file_path)

print("Processing complete.")
