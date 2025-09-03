import subprocess

# Brute-force range: adjust start, end as per expected key length (e.g., 4 digits means 0000 to 9999)
for key in range(0, 10000):
    str_key = str(key).zfill(4)  # pad to 4 digits
    # Run the binary .pyc with subprocess & provide the key as input
    process = subprocess.Popen(
        ['python3', 'chall1.pyc'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Send input and get output
    try:
        output, error = process.communicate(input=str_key+'\n', timeout=3)
        if "Flag:" in output:
            print(f"Key tried: {str_key}")
            print(output)
        # Look for the pattern that changes if found, e.g., 'Access denied!' or correct flag
        if "Access denied!" not in output:
            # Likely found the key if output is different
            print("Potential key found:", str_key)
            print("Output:\n", output)
            break
    except subprocess.TimeoutExpired:
        process.kill()