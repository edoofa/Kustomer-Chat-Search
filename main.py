import json
import os
import glob

def format_whatsapp_chat_to_html(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .message { padding: 10px; margin: 5px; border-radius: 8px; width: fit-content; width: 100%; }
            .student { background-color: white; align-self: flex-start; }
            .mentor { background-color: lightgreen; align-self: flex-end; text-align: right; }
            .container { display: flex; flex-direction: column; }
            .student-container { align-items: flex-start; }
            .mentor-container { align-items: flex-end; }
            .sender { font-weight: bold; }
            .datetime { font-size: small; }
        </style>
    </head>
    <body>
        <div class="container">
    """

    for line in lines:
        if '- Student:' in line:
            parts = line.split('- Student:', 1)
            datetime_info = parts[0].strip()
            message = parts[1].strip()
            html_content += f'<div class="student-container"><span class="datetime">{datetime_info}</span><br/><span class="sender">Student:</span><div class="message student">{message}</div></div>\n'
        elif '- Mentor:' in line:
            parts = line.split('- Mentor:', 1)
            datetime_info = parts[0].strip()
            message = parts[1].strip()
            html_content += f'<div class="mentor-container"><span class="datetime">{datetime_info}</span><br/><span class="sender">Mentor:</span><div class="message mentor">{message}</div></div>\n'

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)

def format_all_chats(input_folder='/chats', output_folder='/formatted_chats'):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # List all .txt files in the input folder
    input_files = glob.glob(os.path.join(input_folder, '*.txt'))
    
    for input_file in input_files:
        # Generating the output file path
        base_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, base_name.replace('.txt', '.html'))
        
        # Format each chat and save the output
        format_whatsapp_chat_to_html(input_file, output_file)

def generate_chat_name_list(output_folder, js_file_path):
    # List all HTML files in the formatted_chats directory
    chat_files = [f for f in os.listdir(output_folder) if f.endswith('.html')]

    # Generate JavaScript code with the list of chat files
    js_code = f"const chatFiles = {json.dumps(chat_files)};"

    # Write the JavaScript code to the file
    with open(js_file_path, 'w') as js_file:
        js_file.write(js_code)


if __name__ == '__main__':
    # Specify the paths to the input and output folders
    input_folder = 'chats'  # Adjust if the input folder containing all the chats are in a different path
    output_folder = 'formatted_chats'  # Adjust if output folder is in a different path
    js_file_path = 'web/chatList.js'

    # Call the function to process all chats
    format_all_chats(input_folder, output_folder)
    generate_chat_name_list(output_folder, js_file_path)

