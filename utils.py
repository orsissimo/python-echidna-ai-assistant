import os
import re
import subprocess
import anthropic

def load_prompt(filename):
    with open(f'prompts/{filename}', 'r', encoding='utf-8') as f:
        return f.read()

def extract_contract_name(user_contract_code):
    contract_matches = re.finditer(r'contract\s+(\w+)', user_contract_code)
    matches_list = list(contract_matches)
    return matches_list[-1].group(1) if matches_list else "Contract"

def extract_solidity_version(contract_code):
    pragma_pattern = r'pragma solidity (\^|>=|<=|>|<)?(0\.[0-9]+\.[0-9]+);'
    match = re.search(pragma_pattern, contract_code)
    if match:
        version = match.group(2)
        return version
    return None

def set_solc_version(version):
    try:
        result = subprocess.run(['solc-select', 'versions'], capture_output=True, text=True)
        if version not in result.stdout:
            subprocess.run(['solc-select', 'install', version], check=True)
        
        subprocess.run(['solc-select', 'use', version], check=True)
        os.environ['SOLC_VERSION'] = version
    except subprocess.CalledProcessError as e:
        print(f"Error setting Solidity version: {e}")
        return False
    return True

def save_file(output_dir, filename, content):
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"File saved to {file_path}")

def parse_input(user_input):
    user_contract_code = user_input.strip()
    if not user_contract_code:
        raise ValueError("No contract code provided.")
    return user_contract_code

def call_claude(client, system_prompt, user_content, max_tokens=8192, temperature=0.5):
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )
        return response.content[0].text
    except anthropic.InternalServerError as e:
        return f"Error: {e}"