class TrieNode:
    """A single node in the Trie (a branch point)."""
    def __init__(self):
        # Maps a character (like 'a') to another TrieNode
        self.children = {}
        
        # This is the "star" 🌟 we talked about.
        # It's True if a word ends at this node.
        self.is_end_of_word = False

class Trie:
    """The main Trie data structure."""
    def __init__(self):
        # The root is the "trunk" of the tree.
        # It's an empty node to start from.
        self.root = TrieNode()

    def insert(self, word):
        """Adds a word to the Trie."""
        
        # Always start from the trunk (root)
        current_node = self.root
        
        # Go through each letter in the word
        for char in word:
            # Check if this letter is already a branch (child)
            if char not in current_node.children:
                # If not, create a new branch (a new TrieNode)
                current_node.children[char] = TrieNode()
            
            # Follow the branch to the next node
            current_node = current_node.children[char]
        
        # After the loop, we are at the last letter.
        # We put a "star" here to mark the end of the word.
        current_node.is_end_of_word = True
        print(f"Successfully added '{word}' to the Trie.")

    def search(self, word):
        """Checks if a complete word is in the Trie."""
        current_node = self.root
        
        for char in word:
            # If the letter (branch) doesn't exist, the word isn't here.
            if char not in current_node.children:
                return False
            # Follow the branch
            current_node = current_node.children[char]
            
        # We found the path, but is it a *word*?
        # We must check for the "star" 🌟.
        return current_node.is_end_of_word

    def starts_with(self, prefix):
        """Checks if any word in the trie starts with this prefix."""
        current_node = self.root
        
        for char in prefix:
            # If the path breaks, no word can start with this.
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
            
        # The entire prefix path exists, so it's a valid start.
        return True

# --- Main program to run ---
if __name__ == "__main__":
    # Create our magical word tree
    my_trie = Trie()
    print("Created a new, empty Trie (word tree)!")
    print("-" * 20)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Add a word")
        print("  2. Search for a word")
        print("  3. Check for a prefix")
        print("  q. Quit")
        
        choice = input("Enter choice (1, 2, 3, or q): ").strip().lower()
        
        if choice == 'q':
            print("Goodbye!")
            break
            
        elif choice == '1':
            # --- ADD A WORD ---
            word_to_add = input("Enter the word to ADD: ").strip().lower()
            if word_to_add:
                my_trie.insert(word_to_add)
            else:
                print("Please enter a valid word.")
                
        elif choice == '2':
            # --- SEARCH FOR A WORD ---
            word_to_search = input("Enter the word to SEARCH for: ").strip().lower()
            if word_to_search:
                if my_trie.search(word_to_search):
                    print(f"✅ YES! The word '{word_to_search}' is in the trie.")
                else:
                    print(f"❌ NO! The word '{word_to_search}' is not in the trie.")
            else:
                print("Please enter a valid word.")

        elif choice == '3':
            # --- CHECK FOR A PREFIX ---
            prefix_to_check = input("Enter the PREFIX to check: ").strip().lower()
            if prefix_to_check:
                if my_trie.starts_with(prefix_to_check):
                    print(f"✅ YES! At least one word starts with '{prefix_to_check}'.")
                else:
                    print(f"❌ NO! No words start with '{prefix_to_check}'.")
            else:
                print("Please enter a valid prefix.")
                
        else:
            print("That's not a valid choice. Please try again.")