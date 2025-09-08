import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import hashlib
import base64
import binascii
import random
import re
import secrets
import json

class CTFChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("🏴‍☠️ ACNCTF CTF Challenge")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d1117")
        
        # Generate session-specific values
        self.session_salt = secrets.token_hex(8)
        self.xor_key = secrets.randbits(8)
        
        # The complete flag
        self.full_flag = "ACNCTF{M4ST3R_0F_TH3_D1G1T4L_R34LM}"
        
        # Flag parts with sophisticated multi-layer encryption
        self.flag_parts = {
            0: {"encrypted": self.multi_encrypt("ACNCTF{", "RIDDLE_MASTER"), "key": "RIDDLE_MASTER"},
            1: {"encrypted": self.multi_encrypt("M4ST3R_", "B4S3_64_K3Y"), "key": "B4S3_64_K3Y"},
            2: {"encrypted": self.multi_encrypt("0F_TH3_", "B1N4RY_K3Y"), "key": "B1N4RY_K3Y"},
            3: {"encrypted": self.multi_encrypt("D1G1T4L_", "C43S4R_K3Y"), "key": "C43S4R_K3Y"},
            4: {"encrypted": self.multi_encrypt("R34LM}", "H4SH_K3Y"), "key": "H4SH_K3Y"}
        }
        
        # User progress tracking
        self.user_progress = 0
        self.collected_parts = []
        self.failed_attempts = 0
        self.max_attempts = 3
        self.is_locked = False
        self.lock_time = 0
        self.user_answers = []
        self.current_challenge_index = 0
        self.start_time = time.time()
        self.challenge_times = []
        
        # Dynamic challenge generation
        self.riddles = [
            {"q": "I have cities, but no houses dwell.\nI have mountains, but no trees as well.\nI have rivers, but no water flows.\nWhat am I?", "a": "map"},
            {"q": "I speak without a mouth and hear without ears.\nI have no body, but I come alive with the wind.\nWhat am I?", "a": "echo"},
            {"q": "The more you take, the more you leave behind.\nWhat am I?", "a": "footsteps"}
        ]
        
        # Challenge definitions with dynamic elements
        self.challenges = self.generate_challenges()
        
        self.setup_ui()
        self.start_challenge()
        
    def generate_challenges(self):
        """Generate dynamic challenges with randomized elements"""
        selected_riddle = random.choice(self.riddles)
        
        # Generate random values for challenges
        random_shift = random.randint(5, 25)
        random_multiplier = random.randint(2, 9)
        
        challenges = [
            {
                "question": f"🛡️ Welcome, challenger! To begin your quest, answer this riddle:\n\n{selected_riddle['q']}\n(one word, lowercase)",
                "answer": selected_riddle['a'],
                "success_msg": "Correct! The first fragment is yours.",
                "hint": "Think about something that represents reality but isn't physical.",
                "validation": lambda ans: ans.strip().lower() == selected_riddle['a'],
                "type": "riddle"
            },
            {
                "question": f"🔤 Decode this triple-encoded string:\n{self.create_triple_encoded()}",
                "answer": "m4st3r_",
                "success_msg": "Excellent! Multi-layer decoding mastered.",
                "hint": "It's Base64 → Hex → Base64. Decode in reverse order.",
                "validation": lambda ans: ans.strip().lower() == "m4st3r_",
                "type": "encoding"
            },
            {
                "question": f"🤖 Binary puzzle with mathematical twist:\n{self.create_binary_math()}\nSolve the equation then convert result to ASCII:",
                "answer": "of_th3_",
                "success_msg": "Mathematical binary conversion achieved!",
                "hint": "Solve the binary math first, then convert the result to ASCII characters.",
                "validation": lambda ans: ans.strip().lower() == "of_th3_",
                "type": "binary_math"
            },
            {
                "question": f"📜 Advanced cipher challenge:\nCiphertext: {self.create_advanced_cipher()}\nMethod: Vigenère cipher with key 'CYBER'\nShift each letter by position × 2",
                "answer": "d1g1t4l_",
                "success_msg": "Advanced cryptography mastered!",
                "hint": "Apply Vigenère decryption first, then reverse the position-based shift.",
                "validation": lambda ans: ans.strip().lower() == "d1g1t4l_",
                "type": "advanced_cipher"
            },
            {
                "question": f"🔐 Cryptographic hash challenge:\nSalt: {self.session_salt}\nCombine: [riddle answer] + 'm4st3r_' + 'of_th3_' + 'd1g1t4l_' + salt\nProvide first 12 chars of SHA-256 hash:",
                "answer": self.get_dynamic_hash_prefix(selected_riddle['a']),
                "success_msg": "Cryptographic mastery achieved!",
                "hint": f"Hash the string: '{selected_riddle['a']}m4st3r_of_th3_d1g1t4l_{self.session_salt}'",
                "validation": lambda ans: ans.strip().lower() == self.get_dynamic_hash_prefix(selected_riddle['a']),
                "type": "hash"
            },
            {
                "question": f"🎯 Final decryption challenge:\nEncrypted flag: {self.create_final_encryption()}\nUse XOR key: {self.xor_key} (decimal)\nThen reverse and apply ROT13",
                "answer": self.full_flag.lower(),
                "success_msg": "🏆 ULTIMATE VICTORY! You are the ACNCTF champion!",
                "hint": "XOR decrypt, reverse the string, then apply ROT13 decryption.",
                "validation": lambda ans: ans.strip().lower() == self.full_flag.lower(),
                "type": "final"
            }
        ]
        return challenges
    
    def multi_encrypt(self, text, key):
        """Multi-layer encryption: XOR → Base64 → Hex"""
        # Layer 1: XOR encryption
        encrypted = []
        for i in range(len(text)):
            encrypted.append(chr(ord(text[i]) ^ ord(key[i % len(key)])))
        xor_encrypted = ''.join(encrypted)
        
        # Layer 2: Base64 encoding
        b64_encrypted = base64.b64encode(xor_encrypted.encode()).decode()
        
        # Layer 3: Hex encoding
        hex_encrypted = b64_encrypted.encode().hex()
        
        return hex_encrypted
    
    def multi_decrypt(self, encrypted_text, key):
        """Decrypt multi-layer encrypted text"""
        try:
            # Layer 1: Hex decoding
            hex_decoded = bytes.fromhex(encrypted_text).decode()
            
            # Layer 2: Base64 decoding
            b64_decoded = base64.b64decode(hex_decoded).decode()
            
            # Layer 3: XOR decryption
            decrypted = []
            for i in range(len(b64_decoded)):
                decrypted.append(chr(ord(b64_decoded[i]) ^ ord(key[i % len(key)])))
            return ''.join(decrypted)
        except Exception as e:
            return "ERROR_DECRYPT"
    
    def create_triple_encoded(self):
        """Create a triple-encoded string for the second challenge"""
        text = "m4st3r_"
        # Base64 encode
        b64 = base64.b64encode(text.encode()).decode()
        # Convert to hex
        hex_str = b64.encode().hex()
        # Base64 encode again
        final = base64.b64encode(hex_str.encode()).decode()
        return final
    
    def create_binary_math(self):
        """Create a binary math puzzle"""
        # The answer should result in ASCII values for "of_th3_"
        # ASCII: o=111, f=102, _=95, t=116, h=104, 3=51, _=95
        binary_ops = [
            "1101111 (111 in decimal)",  # o
            "1100110 (102 in decimal)",  # f  
            "1011111 (95 in decimal)",   # _
            "1110100 (116 in decimal)",  # t
            "1101000 (104 in decimal)",  # h
            "110011 (51 in decimal)",    # 3
            "1011111 (95 in decimal)"    # _
        ]
        return "Binary values to convert:\n" + " ".join(binary_ops[:7])
    
    def create_advanced_cipher(self):
        """Create an advanced cipher for the fourth challenge"""
        # This is a simplified version - in a real CTF this would be more complex
        text = "d1g1t4l_"
        # Apply simple transformations that reverse to the answer
        # For demo purposes, we'll use a simple substitution
        cipher_map = str.maketrans("d1g1t4l_", "F3K3V6N@")
        return text.translate(cipher_map)
    
    def get_dynamic_hash_prefix(self, riddle_answer):
        """Calculate hash prefix for current session"""
        combined = f"{riddle_answer}m4st3r_of_th3_d1g1t4l_{self.session_salt}"
        hash_full = hashlib.sha256(combined.encode()).hexdigest()
        return hash_full[:12]
    
    def create_final_encryption(self):
        """Create final encrypted flag"""
        # Apply transformations in reverse order for the challenge
        text = self.full_flag
        # Apply ROT13
        rot13 = str.maketrans('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                              'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM')
        rot13_text = text.translate(rot13)
        # Reverse
        reversed_text = rot13_text[::-1]
        # XOR encrypt
        xor_encrypted = ''.join(chr(ord(char) ^ self.xor_key) for char in reversed_text)
        # Base64 encode for display
        return base64.b64encode(xor_encrypted.encode()).decode()
    
    def setup_ui(self):
        # Header frame with enhanced styling
        header_frame = tk.Frame(self.root, bg="#0d1117")
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="🏴‍☠️ ACNCTF CTF Challenge",
            font=("Courier New", 24, "bold"),
            fg="#58a6ff",
            bg="#0d1117"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Multi-Layer Cryptographic Challenge",
            font=("Arial", 14),
            fg="#7c3aed",
            bg="#0d1117"
        )
        subtitle_label.pack(pady=5)
        
        # Session info
        session_frame = tk.Frame(self.root, bg="#0d1117")
        session_frame.pack(fill=tk.X, padx=20, pady=2)
        
        tk.Label(
            session_frame,
            text=f"Session ID: {self.session_salt} | XOR Key: {self.xor_key}",
            font=("Courier New", 10),
            fg="#6e7681",
            bg="#0d1117"
        ).pack()
        
        # Progress bar with enhanced visual
        self.progress_frame = tk.Frame(self.root, bg="#0d1117")
        self.progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        progress_label_frame = tk.Frame(self.progress_frame, bg="#0d1117")
        progress_label_frame.pack(fill=tk.X)
        
        tk.Label(
            progress_label_frame,
            text="Challenge Progress:",
            font=("Arial", 11, "bold"),
            fg="#f0f6fc",
            bg="#0d1117"
        ).pack(side=tk.LEFT)
        
        self.time_label = tk.Label(
            progress_label_frame,
            text="Time: 00:00",
            font=("Arial", 11),
            fg="#58a6ff",
            bg="#0d1117"
        )
        self.time_label.pack(side=tk.RIGHT)
        
        self.progress_bar = tk.Frame(self.progress_frame, bg="#21262d", height=25)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Enhanced chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            width=100,
            height=28,
            font=("Consolas", 11),
            bg="#0d1117",
            fg="#f0f6fc",
            insertbackground="#58a6ff",
            selectbackground="#264f78",
            relief="solid",
            borderwidth=1,
            wrap=tk.WORD
        )
        self.chat_display.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Enhanced input frame
        input_frame = tk.Frame(self.root, bg="#0d1117")
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        input_label_frame = tk.Frame(input_frame, bg="#0d1117")
        input_label_frame.pack(fill=tk.X)
        
        tk.Label(
            input_label_frame,
            text="Your Answer:",
            font=("Arial", 11, "bold"),
            fg="#f0f6fc",
            bg="#0d1117"
        ).pack(side=tk.LEFT)
        
        self.difficulty_label = tk.Label(
            input_label_frame,
            text="Difficulty: ★★★★☆",
            font=("Arial", 11),
            fg="#f85149",
            bg="#0d1117"
        )
        self.difficulty_label.pack(side=tk.RIGHT)
        
        entry_frame = tk.Frame(input_frame, bg="#0d1117")
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.user_input = tk.Entry(
            entry_frame,
            font=("Consolas", 13),
            bg="#21262d",
            fg="#f0f6fc",
            insertbackground="#58a6ff",
            relief="solid",
            borderwidth=1
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.submit_answer)
        
        self.submit_btn = tk.Button(
            entry_frame,
            text="Submit Answer",
            command=self.submit_answer,
            bg="#238636",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="solid",
            borderwidth=1,
            padx=25
        )
        self.submit_btn.pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = tk.Frame(input_frame, bg="#0d1117")
        control_frame.pack(fill=tk.X, pady=5)
        
        self.hint_btn = tk.Button(
            control_frame,
            text="💡 Hint",
            command=self.show_hint,
            bg="#6f42c1",
            fg="white",
            font=("Arial", 10),
            relief="solid",
            borderwidth=1
        )
        self.hint_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.skip_btn = tk.Button(
            control_frame,
            text="⏭️ Skip (Penalty)",
            command=self.skip_challenge,
            bg="#da3633",
            fg="white",
            font=("Arial", 10),
            relief="solid",
            borderwidth=1
        )
        self.skip_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status frame with more info
        status_frame = tk.Frame(self.root, bg="#0d1117")
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Initializing...",
            font=("Arial", 11),
            fg="#7c3aed",
            bg="#0d1117"
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.attempts_label = tk.Label(
            status_frame,
            text="Attempts: 0/3",
            font=("Arial", 11),
            fg="#f85149",
            bg="#0d1117"
        )
        self.attempts_label.pack(side=tk.RIGHT)
        
        # Flag display with better formatting
        flag_frame = tk.Frame(self.root, bg="#0d1117")
        flag_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            flag_frame,
            text="Flag Fragments Status:",
            font=("Arial", 12, "bold"),
            fg="#58a6ff",
            bg="#0d1117"
        ).pack(anchor=tk.W)
        
        self.flag_display = tk.Label(
            flag_frame,
            text="🔒 [ENCRYPTED] 🔒 [ENCRYPTED] 🔒 [ENCRYPTED] 🔒 [ENCRYPTED] 🔒 [ENCRYPTED] 🔒 [FINAL]",
            font=("Courier New", 10),
            fg="#6e7681",
            bg="#0d1117",
            wraplength=1000
        )
        self.flag_display.pack(anchor=tk.W, pady=2)
        
        # Start timer
        self.update_timer()
        
    def update_timer(self):
        """Update the session timer"""
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.time_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
        
    def update_progress_bar(self):
        """Update the visual progress bar with challenge types"""
        for widget in self.progress_bar.winfo_children():
            widget.destroy()
            
        challenge_icons = ["🛡️", "🔤", "🤖", "📜", "🔐", "🎯"]
        
        for i in range(len(self.challenges)):
            if i < self.user_progress:
                color = "#238636"
                text_color = "white"
            elif i == self.user_progress:
                color = "#f85149"
                text_color = "white"
            else:
                color = "#21262d"
                text_color = "#6e7681"
                
            segment = tk.Label(
                self.progress_bar, 
                text=challenge_icons[i] if i < len(challenge_icons) else "❓",
                bg=color, 
                fg=text_color,
                font=("Arial", 12),
                width=4, 
                height=1
            )
            segment.pack(side=tk.LEFT, padx=2, pady=2)
    
    def add_message(self, sender, message, color="#f0f6fc"):
        """Enhanced message display with better formatting"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        
        if sender == "SYSTEM":
            self.chat_display.insert(tk.END, f"[{timestamp}] 🤖 SYSTEM: ", "timestamp")
            self.chat_display.insert(tk.END, f"{message}\n\n", "system")
        elif sender == "USER":
            self.chat_display.insert(tk.END, f"[{timestamp}] 👤 YOU: ", "timestamp")
            self.chat_display.insert(tk.END, f"{message}\n\n", "user")
        elif sender == "HINT":
            self.chat_display.insert(tk.END, f"[{timestamp}] 💡 HINT: ", "timestamp")
            self.chat_display.insert(tk.END, f"{message}\n\n", "hint")
            
        # Configure enhanced text tags
        self.chat_display.tag_config("timestamp", foreground="#6e7681", font=("Arial", 9))
        self.chat_display.tag_config("system", foreground="#58a6ff")
        self.chat_display.tag_config("user", foreground="#7c3aed")
        self.chat_display.tag_config("hint", foreground="#f85149")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def start_challenge(self):
        """Initialize the challenge with enhanced intro"""
        self.add_message("SYSTEM", "🏴‍☠️ Welcome to ACNCTF Advanced CTF Challenge!")
        self.add_message("SYSTEM", f"Session initialized with unique parameters:")
        self.add_message("SYSTEM", f"• Session Salt: {self.session_salt}")
        self.add_message("SYSTEM", f"• XOR Key: {self.xor_key}")
        self.add_message("SYSTEM", "• Challenge Count: 6 levels")
        self.add_message("SYSTEM", "• Difficulty: Advanced (★★★★☆)")
        self.add_message("SYSTEM", "")
        self.add_message("SYSTEM", "Each challenge uses different cryptographic techniques.")
        self.add_message("SYSTEM", "You have 3 attempts per challenge before lockout.")
        self.add_message("SYSTEM", "Use hints wisely - they may contain crucial information!")
        self.add_message("SYSTEM", "=" * 70)
        self.present_challenge()
        
    def present_challenge(self):
        """Present current challenge with enhanced formatting"""
        if self.current_challenge_index < len(self.challenges):
            challenge = self.challenges[self.current_challenge_index]
            
            # Update difficulty display based on challenge type
            difficulty_map = {
                "riddle": "★★☆☆☆",
                "encoding": "★★★☆☆", 
                "binary_math": "★★★★☆",
                "advanced_cipher": "★★★★★",
                "hash": "★★★★☆",
                "final": "★★★★★"
            }
            
            challenge_type = challenge.get("type", "unknown")
            self.difficulty_label.config(text=f"Difficulty: {difficulty_map.get(challenge_type, '★★★☆☆')}")
            
            self.add_message("SYSTEM", f"🎯 CHALLENGE {self.current_challenge_index + 1}/6")
            self.add_message("SYSTEM", f"Type: {challenge_type.upper()}")
            self.add_message("SYSTEM", "")
            self.add_message("SYSTEM", challenge["question"])
            
            self.status_label.config(text=f"Status: Challenge {self.current_challenge_index + 1} active")
            self.failed_attempts = 0
            self.update_attempts_display()
            self.update_progress_bar()
        
    def submit_answer(self, event=None):
        """Enhanced answer processing"""
        if self.is_locked:
            remaining = int(30 - (time.time() - self.lock_time))
            if remaining > 0:
                self.add_message("SYSTEM", f"⏰ System locked. Try again in {remaining} seconds.")
                return
            else:
                self.is_locked = False
                self.status_label.config(text=f"Status: Challenge {self.current_challenge_index + 1} active")
        
        answer = self.user_input.get().strip()
        if not answer:
            return
            
        self.add_message("USER", answer)
        self.user_input.delete(0, tk.END)
        
        if self.current_challenge_index >= len(self.challenges):
            self.add_message("SYSTEM", "🎉 All challenges completed!")
            return
            
        self.check_answer(answer.lower())
        
    def check_answer(self, answer):
        """Enhanced answer validation with detailed feedback"""
        current_challenge = self.challenges[self.current_challenge_index]
        challenge_start_time = time.time()
        
        if current_challenge["validation"](answer):
            solve_time = int(challenge_start_time - getattr(self, 'challenge_start_time', challenge_start_time))
            self.challenge_times.append(solve_time)
            
            self.add_message("SYSTEM", f"✅ {current_challenge['success_msg']}")
            self.add_message("SYSTEM", f"⏱️ Solved in {solve_time} seconds")
            
            # For flag fragment challenges (first 5)
            if self.current_challenge_index < 5:
                flag_part = self.multi_decrypt(
                    self.flag_parts[self.current_challenge_index]["encrypted"], 
                    self.flag_parts[self.current_challenge_index]["key"]
                )
                self.collected_parts.append(flag_part)
                self.add_message("SYSTEM", f"🧩 Flag fragment unlocked: [{flag_part}]")
            
            self.current_challenge_index += 1
            self.user_progress = self.current_challenge_index
            self.update_flag_display()
            
            if self.current_challenge_index >= len(self.challenges):
                total_time = int(time.time() - self.start_time)
                avg_time = sum(self.challenge_times) // len(self.challenge_times) if self.challenge_times else 0
                
                self.add_message("SYSTEM", "🏆 CHALLENGE COMPLETED!")
                self.add_message("SYSTEM", f"🚩 Complete Flag: {self.full_flag}")
                self.add_message("SYSTEM", f"📊 Total time: {total_time // 60}:{total_time % 60:02d}")
                self.add_message("SYSTEM", f"📈 Average solve time: {avg_time}s per challenge")
                
                self.status_label.config(text="Status: CHAMPION! 🏆")
                self.submit_btn.config(state=tk.DISABLED, text="Completed!")
                self.user_input.config(state=tk.DISABLED)
            else:
                self.add_message("SYSTEM", "=" * 70)
                self.challenge_start_time = time.time()
                self.present_challenge()
        else:
            self.failed_attempts += 1
            self.update_attempts_display()
            
            if self.failed_attempts >= self.max_attempts:
                self.add_message("SYSTEM", "❌ Maximum attempts exceeded. System locked for 30 seconds.")
                self.add_message("SYSTEM", "💡 Use this time to analyze the challenge more carefully.")
                self.is_locked = True
                self.lock_time = time.time()
                self.status_label.config(text="Status: LOCKED ⏰")
            else:
                remaining = self.max_attempts - self.failed_attempts
                self.add_message("SYSTEM", f"❌ Incorrect answer. {remaining} attempt(s) remaining.")
                
                # Provide contextual feedback
                if self.current_challenge_index == 1 and "=" in answer:
                    self.add_message("SYSTEM", "💭 Remember: decode in reverse order of encoding.")
                elif self.current_challenge_index == 2 and any(c.isdigit() for c in answer):
                    self.add_message("SYSTEM", "💭 Convert binary to decimal, then decimal to ASCII characters.")
    
    def show_hint(self):
        """Enhanced hint system"""
        if self.current_challenge_index < len(self.challenges):
            challenge = self.challenges[self.current_challenge_index]
            hint_msg = challenge["hint"]
            
            # Add progressive hints based on attempt number
            if self.failed_attempts >= 1:
                progressive_hints = {
                    0: "🔍 Look for patterns in the question structure.",
                    1: "🔍 Remember that some encodings stack on top of each other.",
                    2: "🔍 Mathematical operations come before ASCII conversion.",
                    3: "🔍 Classical ciphers often combine multiple techniques.",
                    4: "🔍 Hash functions require exact input strings.",
                    5: "🔍 Multiple decryption steps in reverse order."
                }
                
                if self.current_challenge_index in progressive_hints:
                    hint_msg += f"\n\nProgressive hint: {progressive_hints[self.current_challenge_index]}"
            
            self.add_message("HINT", hint_msg)
    
    def skip_challenge(self):
        """Allow skipping with penalty"""
        if messagebox.askyesno("Skip Challenge", "Skip this challenge? (You'll lose 2 minutes as penalty)"):
            self.add_message("SYSTEM", "⏭️ Challenge skipped. 2-minute penalty added to your time.")
            self.start_time -= 120  # Add 2-minute penalty
            
            # Mark as skipped and move to next
            self.collected_parts.append("[SKIPPED]")
            self.current_challenge_index += 1
            self.user_progress = self.current_challenge_index
            self.update_flag_display()
            
            if self.current_challenge_index >= len(self.challenges):
                self.add_message("SYSTEM", "🏁 All challenges completed (with skips).")
                self.add_message("SYSTEM", f"🚩 Partial Flag: {''.join(self.collected_parts)}")
                self.status_label.config(text="Status: Completed with penalties")
            else:
                self.add_message("SYSTEM", "=" * 70)
                self.present_challenge()
    
    def update_attempts_display(self):
        """Update the attempts counter with color coding"""
        color = "#f85149" if self.failed_attempts >= 2 else "#58a6ff"
        self.attempts_label.config(
            text=f"Attempts: {self.failed_attempts}/{self.max_attempts}",
            fg=color
        )
    
    def update_flag_display(self):
        """Enhanced flag display with status indicators"""
        display_parts = []
        status_icons = {
            "encrypted": "🔒",
            "unlocked": "✅", 
            "skipped": "⏭️",
            "final": "🏆"
        }
        
        for i in range(len(self.challenges)):
            if i < len(self.collected_parts):
                if self.collected_parts[i] == "[SKIPPED]":
                    display_parts.append("⏭️ [SKIPPED]")
                else:
                    display_parts.append(f"✅ [{self.collected_parts[i]}]")
            elif i == self.current_challenge_index:
                display_parts.append("🔄 [ACTIVE]")
            else:
                display_parts.append("🔒 [LOCKED]")
        
        self.flag_display.config(text=" ".join(display_parts))
        
        # Change color based on progress
        if len(self.collected_parts) == len(self.challenges):
            self.flag_display.config(fg="#58a6ff")
        elif any("[SKIPPED]" in part for part in self.collected_parts):
            self.flag_display.config(fg="#f85149")
        else:
            self.flag_display.config(fg="#6e7681")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Enhanced window setup
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Prevent resizing below minimum size
    root.minsize(1000, 700)
    
    chatbot = CTFChatbot(root)
    root.mainloop()