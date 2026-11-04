# hashing_project_ece576
ECE576 Hashing Game


## How to Run and Test the Modules

### Testing Individual Game Modules

1. Open **Python IDLE** on your computer.
2. Open the Python file (`.py`) for the game module you want to test.
3. Run the program by selecting **Run → Run Module (F5)**.
4. Each game module can be opened and executed separately to test its individual functionality.
5. Repeat these steps for each game module you want to test.

### Dashboard

- The dashboard is a simple HTML page.
- Open the dashboard's `.html` file in a web browser to view it.
- No Python execution is required to launch the dashboard.


## Level 1: Plaintext & Base64

- Inspect the leaked database to find passwords stored in readable plaintext or Base64 encoding.
- Uncover plaintext passwords using a dictionary search (`search <word>`) to check the wordlist, or manually decode credentials using `decode <string>` to convert Base64 into readable text.
- Compromise an account by entering `username:password` (e.g., `alice:qwerty`).
- Compromise all **10 user accounts** to complete the level.

**Available Commands:**
- `search <word>` - Search the wordlist for a password.
- `decode <string>` - Decode a Base64-encoded string.
- `username:password` - Attempt to compromise an account.
- `db` - Inspect the leaked database.
- `words` - View the available wordlist.
- `help` - Display available commands.
- `quit` - Exit the level.

---

## Level 2: Unsalted Fast Hashes & Rainbow Tables

- Inspect the database to find passwords hashed using MD5, SHA-1, SHA-256, or SHA3-256.
- Uncover passwords by matching hashes against a precomputed rainbow lookup table, or use active hashing (`hash <algo> <word>`) to manually generate and compare hashes.
- Watch for **equality leaks**: users sharing identical passwords and hashing algorithms will have identical hashes because no salts are used.
- Submit cracked passwords using `username:password` to compromise all **10 user accounts** and complete the level.

**Available Commands:**
- `hash <algo> <word>` - Generate a hash using the specified algorithm.
- `username:password` - Attempt to compromise an account.
- `db` - Inspect the database.
- `words` - View the available wordlist.
- `table` - View the precomputed rainbow lookup table.
- `help` - Display available commands.
- `quit` - Exit the level.

---

## Level 3: Salted Fast Hashes & Contextual Clues

- Inspect the database to see that each user's password has a random 4-character salt prepended before hashing.
- Notice that users sharing identical passwords and hashing algorithms now have completely different hashes, demonstrating how salts prevent equality leaks.
- Read each user's password hint to narrow down their password to 2–3 possibilities from the candidate wordlist.
- Test candidate passwords using the user's specific hashing algorithm and salt via `hash <algo> <salt> <word>`.
- Once a generated hash matches the database entry, submit `username:password` to recover at least **5 out of 10 accounts** and complete the level.

**Available Commands:**
- `hash <algo> <salt> <word>` - Generate a salted hash using the specified algorithm, salt, and password.
- `username:password` - Attempt to compromise an account.
- `db` - Inspect the database.
- `words` - View the available wordlist.
- `table` - View the precomputed lookup table.
- `help` - Display available commands.
- `quit` - Exit the level.
