# CTF Challenge Write-Up: Math or Brawn

## Challenge Overview
**Challenge Name:** Math or Brawn  
**Category:** Reverse Engineering  
**Difficulty:** Easy/Medium  
**Description:** The challenge involves a compiled Python bytecode file (`chall1_rev.pyc`) that requires a 4-digit PIN to unlock the flag. The solution can be approached either by reverse engineering the logic (Math) or by brute-forcing the PIN (Brawn).

## Analysis
The provided compiled bytecode (`chall1_rev.pyc`) is a Python3 compiled executable. When run, it prompts for a 4-digit key. If the correct key is entered, it prints the flag; otherwise, it outputs "Access denied!".

Since the key is a 4-digit number (0000 to 9999), there are only 10,000 possible combinations. This makes brute-forcing feasible.

## Solution Approaches

### Approach 1: Brawn (Brute-Force)
We can write a script that iterates through all possible 4-digit PINs (0000 to 9999) and tests each one against the compiled bytecode. The script uses `subprocess` to run the bytecode and provide the candidate PIN as input.

#### Brute-Force Script
```python
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
```

**How it works:**
1. The script loops through all numbers from 0 to 9999.
2. Each number is padded to 4 digits (e.g., 42 becomes "0042").
3. For each candidate PIN, it runs `chall1_rev.pyc` as a subprocess.
4. It sends the candidate PIN as input to the subprocess.
5. It checks the output for the flag pattern "ACNCTF{" or any non-denial message.
6. If found, it prints the key and the output (which contains the flag) and stops.

**Note:** The timeout is set to 3 seconds per key to prevent hanging. This is sufficient since the bytecode should run quickly.

### Approach 2: Math (Reverse Engineering)
Alternatively, we can reverse engineer the bytecode to understand the logic and derive the key without brute-forcing.

#### Steps for Reverse Engineering:
1. **Decompile the bytecode:** Use a tool like `uncompyle6` or `pycdc` to decompile `chall1_rev.pyc` back to Python source.
   - Example command: `uncompyle6 chall1_rev.pyc > decompiled.py`
2. **Analyze the decompiled code:** The source code will reveal how the input key is validated.
3. **Derive the key:** The validation logic might involve a simple check (e.g., comparing against a hardcoded value or a mathematical operation). Solve for the key.

However, since the brute-force approach is straightforward and efficient (only 10,000 attempts), it is the preferred method for this challenge.

## Execution
1. Save the brute-force script as `brute_force.py`.
2. Ensure `chall1_rev.pyc` is in the same directory.
3. Run the script: `python3 brute_force.py`
4. The script will iterate through all possible PINs until it finds the correct one.

**Expected Output:**
```
Tried key: 0000
Tried key: 0100
...
[SUCCESS] Key found: 1234
Output:
 Enter the key: ACNCTF{flag_here}
```

## Conclusion
The challenge demonstrates that sometimes brute-forcing is a viable solution when the key space is small. Alternatively, reverse engineering the bytecode can provide a more elegant solution. In this case, brute-forcing is efficient and requires minimal effort.
```cmd
C:\Users\Java\Downloads\ctf\for_git\chall1>python chall.pyc
==================================================
ADVANCED MATHEMATICAL CHALLENGE
==================================================
Enter the secret key to unlock the flag:
> 100c

Mathematical computation result: 774
Flag: ACNCTF{u_r_s0_5m4rt_w0w}
```

## Additional Notes
- If the bytecode requires a specific Python version, ensure you use the same version to avoid compatibility issues.
- The brute-force script includes progress reporting every 100 keys to monitor progress.
- Timeouts and error handling are included to handle unexpected behaviors.

This write-up covers both the "Brawn" (brute-force) and "Math" (reverse engineering) approaches, providing a comprehensive solution to the challenge.
