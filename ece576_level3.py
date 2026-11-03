import hashlib
import random
import sys

# Fix Windows terminal crashes caused by emojis and special characters
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def clear_screen():
    print("\n" + "=" * 60 + "\n")

def print_database(db_data, recovered):
    """Displays the leaked database records with salts and hints."""
    print("\n" + "=" * 95)
    print("  STOLEN DATABASE LEAK (SecureHash Ltd)")
    print("=" * 95)
    print(f"  {'USERNAME':<8} | {'ALGO':<8} | {'SALT':<6} | {'HASH VALUE (FIRST 32 CHARS)':<35} | {'PASSWORD HINT'}")
    print("-" * 95)
    for user, info in db_data.items():
        status = "[CRACKED]" if user in recovered else info['clue']
        display_hash = info['hash'][:32] + "..." if len(info['hash']) > 32 else info['hash']
        print(f"  {user:<8} | {info['algo']:<8} | {info['salt']:<6} | {display_hash:<35} | {status}")
    print("-" * 95)

def print_wordlist(candidate_wordlist):
    """Displays the candidate password wordlist to help interpret the hints."""
    print("\n--- CANDIDATE PASSWORD WORDLIST (Each hint matches 2-3 words below) ---")
    print(", ".join(candidate_wordlist))
    print("-" * 71)

def print_rainbow_table():
    """Displays the standard unsalted rainbow table to show why salts defeat it."""
    print("\n" + "=" * 85)
    print("  PRECOMPUTED RAINBOW LOOKUP TABLE (Unsalted)")
    print("=" * 85)
    print("  Notice: None of these standard hashes match the database anymore due to the salts!")
    print("-" * 85)
    print(f"{'ALGO':<14} | {'HASH VALUE':<64} | {'PLAINTEXT'}")
    print("-" * 85)
    
    algo_groups = [("MD5", "md5"), ("SHA-1", "sha1"), ("SHA-256", "sha256"), ("SHA3-256", "sha3_256")]
    sample_words = ["password123", "admin123", "letmein", "sunshine"]
    
    for display_name, algo_key in algo_groups:
        for pwd in sample_words:
            if algo_key == "md5":
                h_val = hashlib.md5(pwd.encode()).hexdigest()
            elif algo_key == "sha1":
                h_val = hashlib.sha1(pwd.encode()).hexdigest()
            elif algo_key == "sha256":
                h_val = hashlib.sha256(pwd.encode()).hexdigest()
            elif algo_key == "sha3_256":
                h_val = hashlib.sha3_256(pwd.encode()).hexdigest()
                
            print(f"{display_name:<14} | {h_val} | {pwd}")
        print("-" * 85)
        
    print("=" * 85)

def print_instructions():
    """Displays the game instructions and available commands."""
    print("\n" + "=" * 95)
    print("  HOW TO PLAY")
    print("=" * 95)
    print("  1. Inspect the STOLEN DATABASE LEAK above. Every user now has a random 4-character")
    print("     SALT prepended to their password before hashing: HASH(salt + password).")
    print("  2. Look at Alice & Grace (both use 'password123' with SHA-256) and Bob & Frank")
    print("     (both use 'admin123' with MD5). Because their salts are different, their final")
    print("     database hashes look completely different! This proves salts defeat equality leaks.")
    print("  3. Read a user's PASSWORD HINT to narrow their password down to 2-3 possibilities")
    print("     from the CANDIDATE PASSWORD WORDLIST above.")
    print("  4. Test your 2-3 candidate words using the user's specific algo and salt:")
    print("     * Type 'hash <algo> <salt> <word>' (e.g., hash sha256 a1b2 password123)")
    print("  5. Once the generated hash matches the database, submit 'username:password'.")
    print("     Recover at least 5 out of 10 user accounts to complete the level!")
    print("\n[Available Commands]")
    print("  * hash <algo> <salt> <word> -> Test a salted word (e.g., hash sha256 a1b2 password123)")
    print("  * username:password         -> Submit a crack attempt (e.g., alice:password123)")
    print("  * db                        -> Re-display the leaked database table")
    print("  * words                     -> Re-display the candidate password wordlist")
    print("  * table                     -> Re-display the unsalted rainbow table")
    print("  * help                      -> Re-display these instructions")
    print("  * quit                      -> Exit the game")
    print("=" * 95)

def print_answer_key(db_data, targets):
    """Displays the instructor answer key directly in the terminal for debugging."""
    print("\n" + "=" * 110)
    print("  [DEBUG] INSTRUCTOR ANSWER SHEET")
    print("=" * 110)
    print(f"  {'USER':<8} | {'PLAINTEXT':<12} | {'SALT':<6} | {'ALGO':<9} | {'HINT':<28} | {'COPY-PASTE INPUT'}")
    print("-" * 110)
    for u, info in db_data.items():
        submission = f"{u}:{targets[u]}"
        print(f"  {u:<8} | {targets[u]:<12} | {info['salt']:<6} | {info['algo']:<9} | {info['clue']:<28} | {submission}")
    print("-" * 110)
    print("  Tip: Type 'solve' at the prompt to auto-complete the level.")
    print("=" * 110)

def run_level_3():
    print("=" * 60)
    print("  MODULE 1: CRACK THE LEAK - LEVEL 3")
    print("  Topic: Salted Fast Hashes & Contextual Clues")
    print("=" * 60)
    print("\nScenario: 'SecureHash Ltd' learned from Level 2 and added unique per-user salts.")
    print("Notice how Alice & Grace share 'password123' (SHA-256) and Bob & Frank share 'admin123' (MD5),")
    print("yet their final database hashes look completely different because of unique salts!")
    
    # User profiles with two identical password pairs (Alice/Grace and Bob/Frank)
    user_profiles = [
        ("alice", "password123", "Classic lazy password (SHA-256)"),   # SHA-256
        ("bob", "admin123", "Default IT credentials (MD5)"),          # MD5
        ("charlie", "letmein", "Doorway / Access phrase"),
        ("diana", "sunshine", "Weather / Sky phenomenon"),
        ("evan", "iloveyou", "Three-word phrase (no spaces)"),
        ("frank", "admin123", "Default IT credentials (MD5)"),          # MD5 (Identical pwd & algo to Bob, different salt!)
        ("grace", "password123", "Classic lazy password (SHA-256)"),  # SHA-256 (Identical pwd & algo to Alice, different salt!)
        ("hank", "dragon", "Real or mythical creature"),
        ("irene", "football", "Popular stadium sport"),
        ("jack", "letmein", "Doorway / Access phrase")
    ]
    
    candidate_wordlist = [
        "password123", "admin123", "welcome123",
        "letmein", "welcome", "openup",
        "sunshine", "thunder", "rainbow",
        "iloveyou", "trustno1",
        "secret", "classified", "private",
        "dragon", "monkey", "falcon",
        "football", "baseball", "soccer"
    ]
    random.shuffle(candidate_wordlist)
    
    db_data = {}
    targets = {}
    
    for user, pwd, clue in user_profiles:
        # Force specific algorithms for the matching pairs to highlight salt differences
        if user in ["alice", "grace"]:
            algo = "sha256"
        elif user in ["bob", "frank"]:
            algo = "md5"
        else:
            algo = random.choice(["md5", "sha1", "sha256", "sha3_256"])
            
        salt = "".join(random.choices("0123456789abcdef", k=4))
        
        # Hashing format: HASH(salt + password)
        salted_payload = (salt + pwd).encode()
        
        if algo == "md5":
            h = hashlib.md5(salted_payload).hexdigest()
        elif algo == "sha1":
            h = hashlib.sha1(salted_payload).hexdigest()
        elif algo == "sha256":
            h = hashlib.sha256(salted_payload).hexdigest()
        elif algo == "sha3_256":
            h = hashlib.sha3_256(salted_payload).hexdigest()
            
        db_data[user] = {"hash": h, "algo": algo, "salt": salt, "clue": clue}
        targets[user] = pwd

    # Save detailed answer key with copy-paste strings to local file for the instructor
    try:
        with open("answer_key_level3.txt", "w", encoding="utf-8") as f:
            f.write("=== LEVEL 3 INSTRUCTOR ANSWER KEY ===\n\n")
            f.write(f"{'USER':<10} | {'PASSWORD':<14} | {'SALT':<6} | {'ALGO':<10} | {'HINT':<32} | {'SUBMISSION'}\n")
            f.write("-" * 102 + "\n")
            for u, pwd in targets.items():
                sub = f"{u}:{pwd}"
                f.write(f"{u:<10} | {pwd:<14} | {db_data[u]['salt']:<6} | {db_data[u]['algo']:<10} | {db_data[u]['clue']:<32} | {sub}\n")
            f.write("\n=== QUICK COPY-PASTE SUBMISSIONS ===\n")
            for u, pwd in targets.items():
                f.write(f"{u}:{pwd}\n")
    except Exception as e:
        print(f"[!] Note: Could not save local answer key ({e})")

    recovered = {}
    target_goal = 5

    # Automatically display rainbow table, database, candidate wordlist, and instructions
    print_rainbow_table()
    print_database(db_data, recovered)
    print_wordlist(candidate_wordlist)
    print_instructions()
    
    while len(recovered) < target_goal:
        user_input = input(f"\n[Level 3] (Recovered {len(recovered)}/{target_goal}) > ").strip()
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
            print_rainbow_table()
            continue

        elif lower_input == 'help':
            print_instructions()
            continue

        # Hidden debug command to view answers in-terminal
        elif lower_input in ['answers', 'key', 'debug']:
            print_answer_key(db_data, targets)
            continue

        # Hidden debug command to immediately finish the level
        elif lower_input == 'solve':
            print("\n[*] [DEBUG] Auto-solving 5 accounts to complete the level...")
            for u, pwd in targets.items():
                if u not in recovered:
                    recovered[u] = pwd
                    print(f"[+] Compromised {u} ({u}:{pwd} | Salt: {db_data[u]['salt']} | Algo: {db_data[u]['algo'].upper()})")
                if len(recovered) >= target_goal:
                    break
            continue
            
        elif lower_input.startswith("hash "):
            parts = user_input.split()
            if len(parts) >= 4:
                algo_choice = parts[1].lower()
                salt_choice = parts[2]
                word_choice = " ".join(parts[3:])
                
                try:
                    payload = (salt_choice + word_choice).encode()
                    if algo_choice == "md5":
                        res = hashlib.md5(payload).hexdigest()
                    elif algo_choice in ["sha1", "sha-1"]:
                        res = hashlib.sha1(payload).hexdigest()
                    elif algo_choice in ["sha256", "sha-256", "sha2"]:
                        res = hashlib.sha256(payload).hexdigest()
                    elif algo_choice in ["sha3", "sha3_256", "sha3-256"]:
                        res = hashlib.sha3_256(payload).hexdigest()
                    else:
                        print("[X] Unknown algorithm. Choose from: md5, sha1, sha256, sha3_256")
                        continue
                    
                    print(f"[*] [{algo_choice.upper()}] Hash of '{salt_choice}' + '{word_choice}':\n    {res}")
                except Exception as e:
                    print(f"[X] Error generating hash: {e}")
            else:
                print("[X] Invalid format. Use: hash <algo> <salt> <word> (e.g., hash sha256 a1b2 password123)")
            continue
            
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
                
            user_algo = db_data[target_user]["algo"]
            user_salt = db_data[target_user]["salt"]
            test_payload = (user_salt + pass_input).encode()
            
            if user_algo == "md5":
                hashed_guess = hashlib.md5(test_payload).hexdigest()
            elif user_algo == "sha1":
                hashed_guess = hashlib.sha1(test_payload).hexdigest()
            elif user_algo == "sha256":
                hashed_guess = hashlib.sha256(test_payload).hexdigest()
            elif user_algo == "sha3_256":
                hashed_guess = hashlib.sha3_256(test_payload).hexdigest()
                
            if hashed_guess == db_data[target_user]["hash"]:
                print(f"[+] SUCCESS! Cracked {target_user}'s password: '{pass_input}'")
                recovered[target_user] = pass_input
            else:
                print(f"[X] Incorrect password for {target_user}. Use 'hash {user_algo} {user_salt} <word>' to test candidates first!")
        else:
            print("[X] Invalid command. Type 'help', 'db', 'words', 'table', use 'hash <algo> <salt> <word>', or submit as 'username:password'.")
            
    print("\n" + "=" * 60)
    print("[+] LEVEL 3 COMPLETE! You successfully bypassed the salts and recovered 5 accounts.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    clear_screen()
    run_level_3()