import hashlib
import random
import sys

def clear_screen():
    print("\n" + "="*60 + "\n")

def run_level_3():
    print("=" * 60)
    print("  MODULE 1: CRACK THE LEAK — LEVEL 3")
    print("  Topic: Salted Fast Hashes & Contextual Clues")
    print("=" * 60)
    print("\nScenario: 'SecureHash Ltd' learned from Level 2 and added unique per-user salts.")
    print("Precomputed rainbow tables are now useless, and equality leaks are gone.")
    print("However, they also leaked a 'password hint' column. Use these clues along with")
    print("the salt to actively hash and recover at least 5 out of 10 passwords.\n")
    
    # Passwords with intentional duplicates to prove equality leaks are defeated
    user_profiles = [
        ("alice", "password123", "Classic lazy password"),
        ("bob", "admin123", "Default IT credentials"),
        ("charlie", "letmein", "Begging the computer"),
        ("diana", "sunshine", "Favorite type of weather"),
        ("evan", "iloveyou", "Sentimental phrase"),
        ("frank", "secret", "Not so hidden"),
        ("grace", "password123", "Classic lazy password"),
        ("hank", "dragon", "Mythical lizard"),
        ("irene", "football", "Favorite sport"),
        ("jack", "letmein", "Begging the computer")
    ]
    
    algorithms = ["md5", "sha1", "sha256", "sha3_256"]
    
    random.shuffle(user_profiles)
    
    db_data = {}
    targets = {}
    
    for user, pwd, clue in user_profiles:
        algo = random.choice(algorithms)
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

    with open("answer_key_level3.txt", "w") as f:
        f.write("=== LEVEL 3 INSTRUCTOR ANSWER KEY ===\n")
        for u, pwd in targets.items():
            f.write(f"User: {u:<8} | Password: {pwd:<12} | Salt: {db_data[u]['salt']} | Algo: {db_data[u]['algo']}\n")

    print("[Available Commands & Instructions]")
    print("  • Type 'db'                          -> View the leaked database file (with salts and hints)")
    print("  • Type 'table'                       -> View standard rainbow table (observe why it fails)")
    print("  • Type 'hash <algo> <salt> <word>'   -> Test a word (e.g., hash md5 a1b2 password123)")
    print("  • Type 'username:password'           -> Submit a crack attempt (e.g., alice:password123)")
    print("  • Type 'quit'                        -> Exit the game\n")
    
    recovered = {}
    target_goal = 5
    
    while len(recovered) < target_goal:
        user_input = input(f"\n[Level 3] (Recovered {len(recovered)}/{target_goal}) > ").strip()
        lower_input = user_input.lower()
        
        if lower_input == 'quit':
            sys.exit(0)
            
        if lower_input in ['db', 'leak', 'database']:
            print("\n" + "="*95)
            print("  STOLEN DATABASE LEAK (SecureHash Ltd)")
            print("="*95)
            print(f"{'USERNAME':<10} | {'ALGO':<8} | {'SALT':<6} | {'HASH VALUE':<32} | {'PASSWORD HINT'}")
            print("-" * 95)
            for user, info in db_data.items():
                status = "[CRACKED]" if user in recovered else info['clue']
                # Truncate hash for display if it's too long, just to keep terminal clean
                display_hash = info['hash'][:32] + "..." if len(info['hash']) > 32 else info['hash']
                print(f"  {user:<8} | {info['algo']:<8} | {info['salt']:<6} | {display_hash:<32} | {status}")
            print("-" * 95)
            continue
            
        if lower_input == 'table':
            print("\n" + "="*85)
            print("  PRECOMPUTED RAINBOW LOOKUP TABLE (Unsalted)")
            print("="*85)
            print("Notice: None of these standard hashes match the database anymore due to the salts.")
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
                
            print("="*85 + "\n")
            continue
            
        if lower_input.startswith("hash "):
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
                        print("❌ Unknown algorithm. Choose from: md5, sha1, sha256, sha3_256")
                        continue
                    
                    print(f"🔍 [{algo_choice.upper()}] Hash of '{salt_choice}' + '{word_choice}':\n   {res}")
                except Exception as e:
                    print(f"❌ Error generating hash: {e}")
            else:
                print("❌ Invalid format. Use: hash <algo> <salt> <word> (e.g., hash md5 a1b2 password123)")
            continue
            
        if ":" in user_input:
            parts = user_input.split(":", 1)
            target_user = parts[0].strip().lower()
            pass_input = parts[1].strip()
            
            if target_user not in targets:
                print("❌ Unknown username.")
                continue
            if target_user in recovered:
                print(f"⚠️ You already recovered {target_user}'s password!")
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
                print(f"✅ SUCCESS! Cracked {target_user}'s password: '{pass_input}'")
                recovered[target_user] = pass_input
            else:
                print(f"❌ Incorrect password for {target_user}. Hash mismatch.")
        else:
            print("❌ Invalid command. Type 'db', 'table', use 'hash <algo> <salt> <word>', or submit as 'username:password'.")
            
    print("\n🎉 LEVEL 3 COMPLETE! You successfully bypassed the salts and recovered 5 accounts.")

if __name__ == "__main__":
    clear_screen()
    run_level_3()
