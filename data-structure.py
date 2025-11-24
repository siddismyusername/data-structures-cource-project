class TrieNode:
    """A single node in the Trie (a branch point)."""
    def __init__(self):
        self.children = {}
        
        self.is_end_of_word = False

class Trie:
    """The main Trie data structure."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Adds a word to the Trie."""
        
        current_node = self.root
        
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            
            current_node = current_node.children[char]
        
        current_node.is_end_of_word = True
        print(f"Successfully added '{word}' to the Trie.")

    def search(self, word):
        """Checks if a complete word is in the Trie."""
        current_node = self.root
        
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
            
        return current_node.is_end_of_word

    def starts_with(self, prefix):
        """Checks if any word in the trie starts with this prefix."""
        current_node = self.root
        
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
            
        return True

if __name__ == "__main__":
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
            word_to_add = input("Enter the word to ADD: ").strip().lower()
            if word_to_add:
                my_trie.insert(word_to_add)
            else:
                print("Please enter a valid word.")
                
        elif choice == '2':
            word_to_search = input("Enter the word to SEARCH for: ").strip().lower()
            if word_to_search:
                if my_trie.search(word_to_search):
                    print(f"✅ YES! The word '{word_to_search}' is in the trie.")
                else:
                    print(f"❌ NO! The word '{word_to_search}' is not in the trie.")
            else:
                print("Please enter a valid word.")

        elif choice == '3':
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