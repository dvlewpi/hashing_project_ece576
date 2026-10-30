import hashlib
import random
import sys

def clear_screen():
    print("\n" + "="*60 + "\n")

def run_level_2():
    print("=" * 60)
    print("  MODULE 1: CRACK THE LEAK — LEVEL 2")
    print("  Topic: Unsalted Fast Hashes & Grouped Rainbow Tables")
    print("=" * 60)
    print("\nScenario: 'FastHash Inc' leaked a database of 10 user accounts.")
    print("Different hashing algorithms were used (MD5, SHA-1, SHA-256, SHA3-256)")
    print("with no salts. You can use the grouped rainbow table or active hashing!\n")
    
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

    print("Leaked Database Records:")
    for user, info in db_data.items():
        print(f"  [User: {user:<8}] -> Hash: {info['hash']}")
    
    candidate_wordlist = [
        "password123", "admin123", "letmein", "sunshine", "iloveyou", 
        "secret", "monkey", "dragon", "football", "baseball", "123456"
    ]
    
    print("\n[Available Commands & Instructions]")
    print("  • Type 'words'                 -> View candidate password wordlist")
    print("  • Type 'table'                 -> View precomputed rainbow lookup table (grouped by algorithm)")
    print("  • Type 'hash <algo> <word>'    -> Test a word (e.g., hash md5 password123)")
    print("  • Type 'username:password'     -> Submit a crack attempt (e.g., alice:password123)")
    print("  • Type 'quit'                  -> Exit the game\n")
    
    recovered = {}
    
    while len(recovered) < len(targets):
        user_input = input("\nEnter command or submission: ").strip()
        lower_input = user_input.lower()
        
        if lower_input == 'quit':
            sys.exit(0)
            
        if lower_input == 'words':
            print("\n--- CANDIDATE PASSWORD WORDLIST ---")
            print(", ".join(candidate_wordlist))
            print("-" * 35 + "\n")
            continue
            
        if lower_input == 'table':
            print("\n" + "="*85)
            print("  PRECOMPUTED RAINBOW LOOKUP TABLE (Grouped by Algorithm)")
            print("="*85)
            print(f"{'ALGO':<12} | {'HASH VALUE':<64} | {'PLAINTEXT'}")
            print("-" * 85)
            
            algo_groups = [("MD5", "md5"), ("SHA-1", "sha1"), ("SHA-256", "sha256"), ("SHA3-256", "sha3_256")]
            
            for display_name, algo_key in algo_groups:
                # Shuffle words inside each group so they appear randomized per algorithm
                group_words = candidate_wordlist.copy()
                random.shuffle(group_words)
                
                for pwd in group_words:
                    if algo_key == "md5":
                        h_val = hashlib.md5(pwd.encode()).hexdigest()
                    elif algo_key == "sha1":
                        h_val = hashlib.sha1(pwd.encode()).hexdigest()
                    elif algo_key == "sha256":
                        h_val = hashlib.sha256(pwd.encode()).hexdigest()
                    elif algo_key == "sha3_256":
                        h_val = hashlib.sha3_256(pwd.encode()).hexdigest()
                        
                    print(f"{display_name:<12} | {h_val} | {pwd}")
                print("-" * 85) # Clean separator between algorithm groups
                
            print("="*85 + "\n")
            continue
            
        # Allow students to generate hashes manually to test guesses
        if lower_input.startswith("hash "):
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
                        print("❌ Unknown algorithm. Choose from: md5, sha1, sha256, sha3_256")
                        continue
                    
                    print(f"🔍 [{algo_choice.upper()}] Hash of '{word_choice}':\n   {res}")
                except Exception as e:
                    print(f"❌ Error generating hash: {e}")
            else:
                print("❌ Invalid format. Use: hash <algo> <word> (e.g., hash md5 password123)")
            continue
            
        # Allow format: username:password
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
                print(f"✅ SUCCESS! Cracked {target_user}'s password: '{pass_input}' (Algorithm was {user_algo.upper()})")
                recovered[target_user] = pass_input
                print(f"   Progress: {len(recovered)}/{len(targets)} accounts recovered.")
                
                # Check for shared equality leaks
                matching_users = [u for u, data in db_data.items() if data["hash"] == db_data[target_user]["hash"] and u not in recovered]
                if matching_users:
                    print(f"💡 Equality Leak Detected! User(s) {matching_users} share this exact same hash/password combination!")
            else:
                print(f"❌ Incorrect password for {target_user}. Hash mismatch.")
        else:
            print("❌ Invalid command. Type 'words', 'table', use 'hash <algo> <word>', or submit as 'username:password'.")
            
    print("\n🎉 LEVEL 2 COMPLETE! You successfully recovered all 10 passwords using rainbow tables or active hashing.")

if __name__ == "__main__":
    clear_screen()
    run_level_2()
