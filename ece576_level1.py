import base64
import random
import sys
import time

def clear_screen():
    print("\n" + "="*60 + "\n")

def slow_print(text, delay=0.03):
    """Simulates a hacker terminal typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def simulate_connection():
    """Adds immersion before the level starts."""
    slow_print("[*] Initializing connection to LegacyCorp servers...")
    time.sleep(0.4)
    slow_print("[*] Bypassing external firewall... SUCCESS")
    time.sleep(0.4)
    slow_print("[*] Downloading user database (users.db)... DONE")
    time.sleep(0.4)
    slow_print("[*] Loading intercepted common password list (rockyou_mini.txt)... DONE")
    time.sleep(0.4)

def run_level_1():
    clear_screen()
    simulate_connection()
    
    print("\n" + "=" * 60)
    print("  MODULE 1: CRACK THE LEAK — LEVEL 1")
    print("  Topic: Plaintext, Base64, & Dictionary Searches")
    print("=" * 60)
    print("\nScenario: You have breached 'LegacyCorp'.")
    print("They claim their database is secure because they use 'advanced encoding'.")
    print("You have their leaked database AND a list of commonly used passwords.")
    print("Find out which users are using these weak passwords to compromise their accounts.\n")
    
    passwords = [
        "password123", "admin", "qwerty", "letmein", "dragon", 
        "football", "monkey", "shadow", "trustno1", "secret"
    ]
    
    users = ["alice", "bob", "charlie", "diana", "evan", "frank", "grace", "hank", "irene", "jack"]
    
    shuffled_passwords = passwords.copy()
    random.shuffle(shuffled_passwords)
    
    db_data = {}
    targets = {}
    failed_attempts = {}
    
    for i, user in enumerate(users):
        pwd = shuffled_passwords[i]
        targets[user] = pwd
        failed_attempts[user] = 0
        
        # Randomly assign 50% as Plaintext, 50% as Base64
        if random.choice([True, False]):
            db_data[user] = {"stored_value": pwd, "type": "plaintext"}
        else:
            b64_val = base64.b64encode(pwd.encode()).decode()
            db_data[user] = {"stored_value": b64_val, "type": "base64"}

    # Automatically save answer key to a local file for the instructor
    with open("answer_key_level1.txt", "w") as f:
        f.write("=== LEVEL 1 INSTRUCTOR ANSWER KEY ===\n")
        for u in users:
            f.write(f"User: {u:<8} | Password: {targets[u]:<12} | Storage: {db_data[u]['type']}\n")

    print("[Available Commands & Instructions]")
    print("  • Type 'db'                  -> View the leaked database file")
    print("  • Type 'words'               -> View the intercepted common password list")
    print("  • Type 'search <word>'       -> Scan the database for a specific password")
    print("  • Type 'decode <string>'     -> Manually decode a Base64 string")
    print("  • Type 'username:password'   -> Submit a crack attempt (e.g., alice:qwerty)")
    print("  • Type 'quit'                -> Exit the game\n")
    
    recovered = set()
    
    while len(recovered) < len(targets):
        user_input = input("\n[LegacyCorp_DB] > ").strip()
        lower_input = user_input.lower()
        
        if lower_input == 'quit':
            sys.exit(0)
            
        elif lower_input in ['db', 'leak', 'database']:
            print("\n" + "="*50)
            print("  STOLEN DATABASE LEAK (LegacyCorp)")
            print("="*50)
            print(f"{'USERNAME':<12} | {'STORED CREDENTIAL'}")
            print("-" * 50)
            for user, info in db_data.items():
                status = "[COMPROMISED]" if user in recovered else ""
                print(f"  {user:<10} | {info['stored_value']:<20} {status}")
            print("-" * 50)
            continue

        elif lower_input == 'words':
            print("\n--- INTERCEPTED WORDLIST (rockyou_mini.txt) ---")
            # Shuffle just for display so it doesn't match the DB order
            display_words = passwords.copy()
            random.shuffle(display_words)
            print(", ".join(display_words))
            print("-" * 47)
            continue
            
        elif lower_input.startswith("search "):
            parts = user_input.split()
            if len(parts) >= 2:
                search_word = parts[1]
                b64_search_word = base64.b64encode(search_word.encode()).decode()
                
                print(f"\n[*] Scanning DB for Plaintext: '{search_word}'")
                print(f"[*] Scanning DB for Base64:    '{b64_search_word}'")
                time.sleep(0.8)
                
                match_found = False
                for user, info in db_data.items():
                    if info['stored_value'] == search_word or info['stored_value'] == b64_search_word:
                        print(f"\n🚨 MATCH FOUND! User '{user}' is using the password '{search_word}'.")
                        print(f"   (It was stored as {info['type']})")
                        match_found = True
                
                if not match_found:
                    print(f"\n[-] No users found using the password '{search_word}'.")
            else:
                print("❌ Invalid format. Use: search <word>")
            continue

        elif lower_input.startswith("decode "):
            parts = user_input.split()
            if len(parts) >= 2:
                b64_string = parts[1]
                try:
                    decoded_bytes = base64.b64decode(b64_string)
                    decoded_str = decoded_bytes.decode('utf-8')
                    sys.stdout.write("🔓 Decoding ")
                    for _ in range(3):
                        sys.stdout.write(".")
                        sys.stdout.flush()
                        time.sleep(0.2)
                    print(f"\n✅ Result: '{decoded_str}'")
                except Exception:
                    print("❌ Error: Invalid Base64 string. Are you sure that isn't plaintext?")
            else:
                print("❌ Invalid format. Use: decode <string>")
            continue
            
        elif ":" in user_input:
            parts = user_input.split(":", 1)
            target_user = parts[0].strip().lower()
            pass_input = parts[1].strip()
            
            if target_user not in targets:
                print("❌ Unknown username.")
                continue
            if target_user in recovered:
                print(f"⚠️ You already compromised {target_user}'s account!")
                continue
                
            if pass_input == targets[target_user]:
                print(f"✅ SUCCESS! {target_user}'s account compromised.")
                recovered.add(target_user)
                print(f"   Progress: {len(recovered)}/{len(targets)} accounts recovered.")
            else:
                failed_attempts[target_user] += 1
                print(f"❌ ACCESS DENIED. Incorrect password for {target_user}.")
                
                if failed_attempts[target_user] == 3:
                    print(f"🚨 [SYSTEM ALERT]: Multiple failed login attempts for user '{target_user}'.")
                    time.sleep(1)
        else:
            print("❌ Invalid command. Type 'help' or view the instructions above.")
            
    print("\n" + "="*60)
    print("🎉 LEVEL 1 COMPLETE!")
    slow_print("Lesson Learned: Encoding is NOT Encryption.")
    slow_print("By using a simple wordlist, you were able to automatically search and")
    slow_print("destroy LegacyCorp's 'advanced' Base64 storage.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_level_1()
