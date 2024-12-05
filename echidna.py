import re
import subprocess
from utils import extract_contract_name, save_file

def run_echidna_test(user_contract_code, echidna_test_response, output_dir):
    user_contract_code = user_contract_code.strip()
    user_contract_name = extract_contract_name(user_contract_code)

    # Extract code between solidity brackets
    echidna_match = re.search(r'```solidity\n(.*?)\n```', echidna_test_response, re.DOTALL)
    if echidna_match:
        test_code = echidna_match.group(1).strip()
        save_file(output_dir, f"{user_contract_name}.sol", user_contract_code)
        save_file(output_dir, f"{user_contract_name}EchidnaTest.sol", test_code)
    else:
        return "Error: No test code found in AI response."

    # Extract and save YAML
    yaml_match = re.search(r'```yaml\n(.*?)\n```', echidna_test_response, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1).strip()
        if yaml_content:
            save_file(output_dir, "echidna.yaml", yaml_content)

    # Extract Echidna command
    command_match = re.search(r'```bash\n(.*?)\n```', echidna_test_response, re.DOTALL)
    if command_match:
        echidna_command = command_match.group(1).strip()
    else:
        return "Error: No Echidna command found in AI response."

    # Run Echidna
    try:
        if echidna_command.startswith('echidna'):
            cmd_replaced = echidna_command.replace('[OriginalContractName]', user_contract_name)
            full_command = f"cd {output_dir} && {cmd_replaced}"
            if not cmd_replaced.endswith('&& cd ..'):
                full_command += ' && cd ..'
            result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return result.stdout
        else:
            return "Unsafe command detected. Aborting execution."
    except Exception as e:
        return f"Error running Echidna: {str(e)}"