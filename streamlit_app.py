import importlib.util
import os
import streamlit as st
import difflib

# Load the Trie from data-structure.py dynamically to avoid import path issues
THIS_DIR = os.path.dirname(__file__)
MODULE_PATH = os.path.join(THIS_DIR, "data-structure.py")

spec = importlib.util.spec_from_file_location("data_structure_module", MODULE_PATH)
data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_module)

# Grab the Trie class
Trie = getattr(data_module, "Trie")


def trie_to_dot(node, node_id=0, labels=None, edges=None):
    """Generate DOT nodes and edges from the Trie recursively.

    Returns (labels, edges, next_id)
    """
    if labels is None:
        labels = {}
    if edges is None:
        edges = []

    # label for this node: show '*' if end of word
    labels[node_id] = "*" if node.is_end_of_word else ""

    next_id = node_id + 1
    for ch, child in node.children.items():
        child_id = next_id
        next_id += 1
        edges.append((node_id, child_id, ch))
        labels, edges, next_id = trie_to_dot(child, child_id, labels, edges)

    return labels, edges, next_id


def build_dot(labels, edges):
    lines = ["digraph Trie {", "  node [shape=circle];"]
    for nid, lab in labels.items():
        # show label and mark end of word with a doublecircle
        if lab == "*":
            lines.append(f'  {nid} [label="{nid}*", shape=doublecircle];')
        else:
            lines.append(f'  {nid} [label="{nid}"];')

    for a, b, ch in edges:
        lines.append(f'  {a} -> {b} [label="{ch}"];')

    lines.append("}")
    return "\n".join(lines)


def main():
    st.title("Trie Visualizer & Playground")

    # Use session state to persist trie across reruns
    if "trie" not in st.session_state:
        st.session_state.trie = Trie()
        st.session_state.words = []

    tab = st.tabs(["Visualizer", "Playground"])

    # --- Visualizer tab ---
    with tab[0]:
        st.header("Trie Graphviz Visualizer")
        st.write("Visual representation of the Trie. Add words in the Playground tab to populate the graph.")

        labels, edges, _ = trie_to_dot(st.session_state.trie.root)
        dot = build_dot(labels, edges)

        # Streamlit supports graphviz_chart; we provide the dot string
        st.graphviz_chart(dot)

        # 'Show DOT source' removed per request

    # --- Playground tab ---
    with tab[1]:
        st.header("Playground: add / search / prefix / spelling helper")

        col1, col2 = st.columns(2)
        with col1:
            # Use a form so the text input and submit are sent together on one click
            with st.form(key="add_form"):
                word_to_add = st.text_input("Word to add", key="add_input")
                submitted = st.form_submit_button("Add")
                if submitted:
                    if word_to_add:
                        w = word_to_add.strip().lower()
                        st.session_state.trie.insert(w)
                        st.session_state.words.append(w)
                        st.success(f"Added '{w}'")
                    else:
                        st.error("Enter a non-empty word.")

            st.markdown("---")
            st.subheader("Current words")
            if st.session_state.words:
                st.write(", ".join(sorted(set(st.session_state.words))))
            else:
                st.info("No words added yet.")

        with col2:
            search_word = st.text_input("Search word", key="search_input")
            if st.button("Search"):
                if search_word:
                    s = search_word.strip().lower()
                    found = st.session_state.trie.search(s)
                    if found:
                        st.success(f"The word '{s}' exists in the Trie.")
                    else:
                        st.warning(f"The word '{s}' was NOT found.")
                        # spelling suggestions using difflib
                        if st.session_state.words:
                            suggestions = difflib.get_close_matches(s, st.session_state.words, n=5, cutoff=0.6)
                            if suggestions:
                                st.info("Did you mean: " + ", ".join(suggestions))
                else:
                    st.error("Enter a word to search for.")

            prefix = st.text_input("Prefix to check", key="prefix_input")
            if st.button("Check Prefix"):
                if prefix:
                    p = prefix.strip().lower()
                    ok = st.session_state.trie.starts_with(p)
                    if ok:
                        st.success(f"At least one word starts with '{p}'.")
                    else:
                        st.warning(f"No words start with '{p}'.")
                else:
                    st.error("Enter a prefix to check.")

            # --- Spelling helper ---
            st.markdown("#### Spelling helper")
            spell_word = st.text_input("Word to check spelling", key="spell_input")
            if st.button("Suggest spelling", key="suggest_button"):
                if not spell_word:
                    st.error("Enter a word to suggest for.")
                else:
                    if not st.session_state.words:
                        st.info("No words in dictionary yet to compare against.")
                    else:
                        s = spell_word.strip().lower()
                        suggestions = difflib.get_close_matches(s, st.session_state.words, n=8, cutoff=0.5)
                        if not suggestions:
                            st.info("No similar words found.")
                        else:
                            st.write("Suggestions:")
                            for i, sug in enumerate(suggestions):
                                a, b = st.columns([6,1])
                                a.write(sug)
                                # unique key per suggestion so Streamlit can handle clicks
                                if b.button("Add", key=f"add_sug_{i}_{sug}"):
                                    st.session_state.trie.insert(sug)
                                    st.session_state.words.append(sug)
                                    st.success(f"Added '{sug}'")

        st.markdown("---")
        st.caption("Spelling suggestions use simple similarity against current session words (difflib).")


if __name__ == "__main__":
    main()
