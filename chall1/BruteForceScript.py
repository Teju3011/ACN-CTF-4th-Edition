import subprocess

# Brute-force all 4-digit numbers (0000 to 9999)
for key in range(0, 10000):
    str_key = str(key).zfill(4)  # Pad to 4 digits (e.g., 42 becomes '0042')
    
    # Run the compiled bytecode
    process = subprocess.Popen(
        ['python3', 'chall1_rev.pyc'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send the candidate key as input
        output, error = process.communicate(input=str_key + '\n', timeout=3)
        
        # Check if we got the actual flag (not the denial message)
        if "ACNCTF{" in output:
            print(f"[SUCCESS] Key found: {str_key}")
            print("Output:\n", output)
            break
        elif "Access denied!" not in output:
            # If there's no denial, it might be a different message (e.g., flag)
            print(f"[POTENTIAL] Key: {str_key}")
            print("Output:\n", output)
            break
        
        # Optional: Print progress every 100 keys
        if key % 100 == 0:
            print(f"Tried key: {str_key}")
            
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"Timeout for key {str_key}")
        
    except Exception as e:
        print(f"Error for key {str_key}: {e}")

print("Brute-force completed.")