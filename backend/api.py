import os

CODES_URI = "codes"

cmd = {
    'py': f'python3 {CODES_URI}/app.py',
}

def run(code):
    # Ensure the directory exists
    if not os.path.exists(CODES_URI):
        os.makedirs(CODES_URI)
    
    # Write the provided code to a Python file
    with open(f'{CODES_URI}/app.py', 'w') as file:
        file.write(code)
    
    # Execute the Python file and capture the output
    exit_code = os.system(f"{cmd['py']} > {CODES_URI}/out.txt 2> {CODES_URI}/err.txt")
    
    if exit_code != 0:
        with open(f"{CODES_URI}/err.txt") as err_file:
            return {"err": True, "msg": err_file.read()}
    else:
        with open(f"{CODES_URI}/out.txt") as out_file:
            return out_file.read()

