import hashlib
import random
import sys

# Fix Windows terminal crashes caused by emojis and special characters
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def clear_screen():
    print("\n" + "=" * 60 + "\n")

def print_database(db_data, recovered):
    """Displays the leaked database records."""
    print("\n" + "=" * 85)
    print("  STOLEN DATABASE LEAK (FastHash Inc)")
    print("=" * 85)
    print(f"  {'USERNAME':<10} | {'STORED HASH VALUE':<64} | {'STATUS'}")
    print("-" * 85)
    for user, info in db_data.items():
        status = "[COMPROMISED]" if user in recovered else ""
        print(f"  {user:<10} | {info['hash']:<64} | {status}")
    print("-" * 85)

def print_wordlist(candidate_wordlist):
    """Displays the candidate password wordlist."""
    print("\n--- CANDIDATE PASSWORD WORDLIST ---")
    print(", ".join(candidate_wordlist))
    print("-" * 35)

def print_rainbow_table(precomputed_table):
    """Displays the precomputed rainbow lookup table grouped by algorithm."""
    print("\n" + "=" * 85)
    print("  PRECOMPUTED RAINBOW LOOKUP TABLE (Grouped by Algorithm)")
    print("=" * 85)
    print(f"{'ALGO':<12} | {'HASH VALUE':<64} | {'PLAINTEXT'}")
    print("-" * 85)
    
    for display_name, rows in precomputed_table:
        for h_val, pwd in rows:
            print(f"{display_name:<12} | {h_val:<64} | {pwd}")
        print("-" * 85)
        
    print("=" * 85)

def print_instructions():
    """Displays the game instructions and available commands."""
    print("\n" + "=" * 85)
    print("  HOW TO PLAY")
    print("=" * 85)
    print("  1. Inspect the STOLEN DATABASE LEAK above. Each user's password has been")
    print("     hashed using MD5 (32 chars), SHA-1 (40 chars), or SHA-256 / SHA3-256 (64 chars).")
    print("  2. Uncover each user's plaintext password using two methods:")
    print("     * Rainbow Table Lookup: Match a user's hash in the STOLEN DATABASE LEAK")
    print("       against the PRECOMPUTED RAINBOW LOOKUP TABLE above to find its plaintext.")
    print("     * Active Hashing: Type 'hash <algo> <word>' (e.g., hash md5 password123)")
    print("       to manually generate a hash and compare it against the database.")
    print("  3. Watch for Equality Leaks! Because no salts were used, users with the")
    print("     same password and algorithm will have identical hashes.")
    print("  4. Submit cracked passwords by typing 'username:password' (e.g., alice:password123).")
    print("     Compromise all 10 user accounts to complete the level!")
    print("\n[Available Commands]")
    print("  * hash <algo> <word> -> Test a word (algos: md5, sha1, sha256, sha3_256)")
    print("  * username:password  -> Submit a crack attempt (e.g., alice:password123)")
    print("  * db                 -> Re-display the leaked database records")
    print("  * words              -> Re-display the candidate password wordlist")
    print("  * table              -> Re-display the precomputed rainbow lookup table")
    print("  * help               -> Re-display these instructions")
    print("  * quit               -> Exit the game")
    print("=" * 85)

def print_answer_key(users, targets, db_data):
    """Displays the instructor answer key directly in the terminal for debugging."""
    print("\n" + "=" * 95)
    print("  [DEBUG] INSTRUCTOR ANSWER SHEET")
    print("=" * 95)
    print(f"  {'USER':<8} | {'PLAINTEXT':<12} | {'ALGO':<9} | {'COPY-PASTE INPUT':<20} | {'HASH (FIRST 24 CHARS)'}")
    print("-" * 95)
    for u in users:
        submission = f"{u}:{targets[u]}"
        short_hash = db_data[u]['hash'][:24] + "..."
        print(f"  {u:<8} | {targets[u]:<12} | {db_data[u]['algo']:<9} | {submission:<20} | {short_hash}")
    print("-" * 95)
    print("  Tip: Type 'solve' at the prompt to auto-complete the level.")
    print("=" * 95)

def run_level_2():
    print("=" * 60)
    print("  MODULE 1: CRACK THE LEAK - LEVEL 2")
    print("  Topic: Unsalted Fast Hashes & Grouped Rainbow Tables")
    print("=" * 60)
    print("\nScenario: 'FastHash Inc' leaked a database of 10 user accounts.")
    print("Different hashing algorithms were used (MD5, SHA-1, SHA-256, SHA3-256)")
    print("with no salts. You can use the grouped rainbow table or active hashing!")
    
    # 10 Passwords (with intentional duplicates for equality leaks)
    passwords = [
        "password123", "admin123", "letmein", "sunshine", "iloveyou", 
        "secret", "password123", "dragon", "football", "letmein"
    ]
    
    users = ["alice", "bob", "charlie", "diana", "evan", "frank", "grace", "hank", "irene", "jack"]
    algorithms = ["md5", "sha1", "sha256", "sha3_256"]
    
    # Randomize password and algorithm assignments
    shuffled_passwords = passwords.copy()
    random.shuffle(shuffled_passwords)
    
    db_data = {}
    targets = {}
    
    for i, user in enumerate(users):
        pwd = shuffled_passwords[i]
        algo = random.choice(algorithms)
        
        if algo == "md5":
            h = hashlib.md5(pwd.encode()).hexdigest()
        elif algo == "sha1":
            h = hashlib.sha1(pwd.encode()).hexdigest()
        elif algo == "sha256":
            h = hashlib.sha256(pwd.encode()).hexdigest()
        elif algo == "sha3_256":
            h = hashlib.sha3_256(pwd.encode()).hexdigest()
            
        db_data[user] = {"hash": h, "algo": algo}
        targets[user] = pwd

    candidate_wordlist = [
        "password123", "admin123", "letmein", "sunshine", "iloveyou", 
        "secret", "monkey", "dragon", "football", "baseball", "123456"
    ]

    # Precompute rainbow table order once so it stays consistent during the session
    algo_groups = [("MD5", "md5"), ("SHA-1", "sha1"), ("SHA-256", "sha256"), ("SHA3-256", "sha3_256")]
    precomputed_table = []
    for display_name, algo_key in algo_groups:
        group_words = candidate_wordlist.copy()
        random.shuffle(group_words)
        rows = []
        for pwd in group_words:
            if algo_key == "md5":
                h_val = hashlib.md5(pwd.encode()).hexdigest()
            elif algo_key == "sha1":
                h_val = hashlib.sha1(pwd.encode()).hexdigest()
            elif algo_key == "sha256":
                h_val = hashlib.sha256(pwd.encode()).hexdigest()
            elif algo_key == "sha3_256":
                h_val = hashlib.sha3_256(pwd.encode()).hexdigest()
            rows.append((h_val, pwd))
        precomputed_table.append((display_name, rows))

    # Save detailed answer key with copy-paste strings to local file for the instructor
    try:
        with open("answer_key_level2.txt", "w", encoding="utf-8") as f:
            f.write("=== LEVEL 2 INSTRUCTOR ANSWER KEY ===\n\n")
            f.write(f"{'USER':<10} | {'PASSWORD':<14} | {'ALGO':<10} | {'SUBMISSION':<22} | {'HASH'}\n")
            f.write("-" * 125 + "\n")
            for u in users:
                sub = f"{u}:{targets[u]}"
                f.write(f"{u:<10} | {targets[u]:<14} | {db_data[u]['algo']:<10} | {sub:<22} | {db_data[u]['hash']}\n")
            f.write("\n=== QUICK COPY-PASTE SUBMISSIONS ===\n")
            for u in users:
                f.write(f"{u}:{targets[u]}\n")
    except Exception as e:
        print(f"[!] Note: Could not save local answer key ({e})")
    
    recovered = {}

    # Automatically display the database, wordlist, rainbow table, and instructions
    print_database(db_data, recovered)
    print_wordlist(candidate_wordlist)
    print_rainbow_table(precomputed_table)
    print_instructions()
    
    while len(recovered) < len(targets):
        user_input = input("\n[FastHash_DB] > ").strip()
        lower_input = user_input.lower()
        
        if lower_input == 'quit':
            sys.exit(0)
            
        elif lower_input in ['db', 'leak', 'database']:
            print_database(db_data, recovered)
            continue

        elif lower_input == 'words':
            print_wordlist(candidate_wordlist)
            continue
            
        elif lower_input == 'table':
            print_rainbow_table(precomputed_table)
            continue

        elif lower_input == 'help':
            print_instructions()
            continue

        # Hidden debug command to view answers in-terminal
        elif lower_input in ['answers', 'key', 'debug']:
            print_answer_key(users, targets, db_data)
            continue

        # Hidden debug command to immediately finish the level
        elif lower_input == 'solve':
            print("\n[*] [DEBUG] Auto-solving all remaining accounts...")
            for u in users:
                if u not in recovered:
                    recovered[u] = targets[u]
                    print(f"[+] Compromised {u} ({u}:{targets[u]} - {db_data[u]['algo'].upper()})")
            continue
            
        # Allow students to generate hashes manually to test guesses
        elif lower_input.startswith("hash "):
            parts = user_input.split()
            if len(parts) >= 3:
                algo_choice = parts[1].lower()
                word_choice = " ".join(parts[2:])
                
                try:
                    if algo_choice == "md5":
                        res = hashlib.md5(word_choice.encode()).hexdigest()
                    elif algo_choice in ["sha1", "sha-1"]:
                        res = hashlib.sha1(word_choice.encode()).hexdigest()
                    elif algo_choice in ["sha256", "sha-256", "sha2"]:
                        res = hashlib.sha256(word_choice.encode()).hexdigest()
                    elif algo_choice in ["sha3", "sha3_256", "sha3-256"]:
                        res = hashlib.sha3_256(word_choice.encode()).hexdigest()
                    else:
                        print("[X] Unknown algorithm. Choose from: md5, sha1, sha256, sha3_256")
                        continue
                    
                    print(f"[*] [{algo_choice.upper()}] Hash of '{word_choice}':\n    {res}")
                except Exception as e:
                    print(f"[X] Error generating hash: {e}")
            else:
                print("[X] Invalid format. Use: hash <algo> <word> (e.g., hash md5 password123)")
            continue
            
        # Allow format: username:password
        elif ":" in user_input:
            parts = user_input.split(":", 1)
            target_user = parts[0].strip().lower()
            pass_input = parts[1].strip()
            
            if target_user not in targets:
                print("[X] Unknown username.")
                continue
            if target_user in recovered:
                print(f"[!] You already recovered {target_user}'s password!")
                continue
                
            # Test guess against the user's specific algorithm
            user_algo = db_data[target_user]["algo"]
            if user_algo == "md5":
                hashed_guess = hashlib.md5(pass_input.encode()).hexdigest()
            elif user_algo == "sha1":
                hashed_guess = hashlib.sha1(pass_input.encode()).hexdigest()
            elif user_algo == "sha256":
                hashed_guess = hashlib.sha256(pass_input.encode()).hexdigest()
            elif user_algo == "sha3_256":
                hashed_guess = hashlib.sha3_256(pass_input.encode()).hexdigest()
                
            if hashed_guess == db_data[target_user]["hash"]:
                print(f"[+] SUCCESS! Cracked {target_user}'s password: '{pass_input}' (Algorithm was {user_algo.upper()})")
                recovered[target_user] = pass_input
                print(f"    Progress: {len(recovered)}/{len(targets)} accounts recovered.")
                
                # Check for shared equality leaks
                matching_users = [u for u, data in db_data.items() if data["hash"] == db_data[target_user]["hash"] and u not in recovered]
                if matching_users:
                    print(f"[!] Equality Leak Detected! User(s) {matching_users} share this exact same hash/password combination!")
            else:
                print(f"[X] Incorrect password for {target_user}. Hash mismatch.")
        else:
            print("[X] Invalid command. Type 'help', 'db', 'words', 'table', use 'hash <algo> <word>', or submit as 'username:password'.")
            
    print("\n" + "=" * 60)
    print("[+] LEVEL 2 COMPLETE! You successfully recovered all 10 passwords using rainbow tables or active hashing.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    clear_screen()
    run_level_2()