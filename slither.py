import json
import os
import subprocess
from utils import extract_contract_name, extract_solidity_version, set_solc_version, save_file

def run_slither_analysis(user_contract_code, output_dir):
    user_contract_name = extract_contract_name(user_contract_code)
    save_file(output_dir, f"{user_contract_name}.sol", user_contract_code)
    
    # Extract and set Solidity version
    solidity_version = extract_solidity_version(user_contract_code)
    if solidity_version:
        if not set_solc_version(solidity_version):
            return json.dumps({"error": f"Failed to set Solidity version {solidity_version}"}, indent=2)
    else:
        return json.dumps({"error": "Could not determine Solidity version from the contract"}, indent=2)

    slither_command = f"slither {user_contract_name}.sol --json {user_contract_name}Slither.json"
    try:
        full_command = f"cd {output_dir} && {slither_command}"
        if not full_command.endswith('&& cd ..'):
            full_command += ' && cd ..'
        result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Read Slither JSON output
        slither_json_path = os.path.join(output_dir, f"{user_contract_name}Slither.json")
        if os.path.exists(slither_json_path):
            with open(slither_json_path, 'r') as f:
                slither_output = json.load(f)
            return json.dumps(slither_output, indent=2)
        else:
            error_msg = {
                "error": "Slither analysis failed",
                "details": result.stdout,
                "command": full_command
            }
            return json.dumps(error_msg, indent=2)
    except Exception as e:
        error_msg = {
            "error": "Error running Slither",
            "details": str(e),
            "command": full_command
        }
        return json.dumps(error_msg, indent=2)