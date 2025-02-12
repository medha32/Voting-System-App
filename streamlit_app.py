import streamlit as st
from collections import defaultdict

def main():
    st.set_page_config(page_title="Voting Systems Explorer", layout="wide")
    
    st.title("🗳️ Voting Systems Explorer")
    st.sidebar.header("📌Select one voting method")
    system = st.sidebar.selectbox("Select one",[
        "First past the post",
        "Preferential voting",
        "Approval Voting",
        "Condorcet Method",
        "Borda Count",
    ])
    
    with st.sidebar:
        st.markdown("---")
        st.caption("Developed to explore different voting mechanisms.")
    
    if system == "First past the post":
        first_system()
    elif system == "Borda Count":
        borda_system()
    elif system == "Preferential voting":
        preferential_system()
    elif system == "Approval Voting":
        approval_system()
    elif system == "Condorcet Method":
        condorcet_system()

def get_candidates():
    candidates_input = st.text_input("Enter candidates:", "Alice, Bob, Charlie")
    candidates = [c.strip() for c in candidates_input.split(',') if c.strip()]
    if len(candidates) < 2:
        st.warning("Please enter at least 2 candidates.")
        return []
    return candidates

def display_results(results, metric_name):
    sorted_results = sorted(results.items(), key=lambda x: (-x[1], x[0]))
    max_score = max([score for _, score in sorted_results]) if sorted_results else 1
    
    st.subheader("📊 Results")
    for candidate, score in sorted_results:
        progress = score / max_score
        st.metric(label=f"{candidate}", value=f"{score} {metric_name}")
        st.progress(progress)
        st.write("---")

def first_system():
    st.header("🏆 First past the post voting System")
    st.markdown("**Each voter selects one candidate. The candidate with the most votes wins**")
    candidates = get_candidates()
    if not candidates:
        return
    
    num_voters = st.number_input("Number of voters", min_value=1, value=3)
    votes = [st.radio(f"Voter {i+1}", candidates, key=f"Firstpastthepost_{i}") for i in range(num_voters)]
    
    if st.button("Calculate Plurality Result", use_container_width=True):
        results = defaultdict(int)
        for vote in votes:
            results[vote] += 1
        display_results(results, "Votes")

def borda_system():
    st.header("📊 Borda Count System")
    st.markdown("**Voters rank candidates.But candidates are given an individual point based on their popularity among the voters.Points of voters are assigned based on ranking**")
    candidates = get_candidates()
    if not candidates:
        return
    
    num_voters = st.number_input("Number of voters", min_value=1, value=3)
    rankings = []
    
    for i in range(num_voters):
        with st.expander(f"Voter {i+1} Ranking"):
            ranking = st.multiselect(f"Rank candidates (most to least preferred)", candidates, default=candidates, key=f"borda_{i}")
            rankings.append(ranking)
    
    if st.button("Calculate Borda Count", use_container_width=True):
        scores = defaultdict(int)
        for ranking in rankings:
            for idx, candidate in enumerate(reversed(ranking)):
                scores[candidate] += idx
        display_results(scores, "Borda Score")

def preferential_system():
    st.header("🔄 Preferential Voting")
    st.markdown("Candidates are eliminated in rounds until one achieves a majority.")
    candidates = get_candidates()
    if not candidates:
        return
    
    num_voters = st.number_input("Number of voters", min_value=1, value=3)
    rankings = []
    for i in range(num_voters):
        with st.expander(f"Voter {i+1} Ranking"):
            ranking = st.multiselect(f"Rank candidates (most to least preferred)", candidates, default=candidates, key=f"irv_{i}")
            rankings.append(ranking)
    
    if st.button("Run my preference", use_container_width=True):
        remaining_candidates = candidates.copy()
        round_num = 1
        while True:
            st.subheader(f"Round {round_num}")
            vote_counts = defaultdict(int)
            for ranking in rankings:
                for candidate in ranking:
                    if candidate in remaining_candidates:
                        vote_counts[candidate] += 1
                        break
            display_results(vote_counts, "First Choice Votes")
            
            max_votes = max(vote_counts.values())
            total_votes = sum(vote_counts.values())
            if max_votes > total_votes / 2:
                winner = [c for c, v in vote_counts.items() if v == max_votes]
                st.success(f"🎉 Winner: {', '.join(winner)}")
                break
            
            min_votes = min(vote_counts.values())
            eliminated = [c for c, v in vote_counts.items() if v == min_votes]
            remaining_candidates = [c for c in remaining_candidates if c not in eliminated]
            
            if len(remaining_candidates) == 0:
                st.warning("No winner could be determined.")
                break
            round_num += 1

def approval_system():
    st.header("✅ Approval Voting System")
    st.markdown("Voters can approve of any number of candidates.")
    candidates = get_candidates()
    if not candidates:
        return
    
    num_voters = st.number_input("Number of voters", min_value=1, value=3)
    approvals = defaultdict(int)
    
    for i in range(num_voters):
        with st.expander(f"Voter {i+1}"):
            selected = st.multiselect("Select candidates you approve of:", candidates, key=f"approval_{i}")
            for candidate in selected:
                approvals[candidate] += 1
    
    if st.button("Calculate Approval Results", use_container_width=True):
        display_results(approvals, "Approvals")

def condorcet_system():
    st.header("⚖️ Condorcet Method")
    st.markdown("A candidate who beats all others in head-to-head comparisons wins.")
    candidates = get_candidates()
    if not candidates:
        return
    
    num_voters = st.number_input("Number of voters", min_value=1, value=3)
    rankings = []
    for i in range(num_voters):
        with st.expander(f"Voter {i+1} Ranking"):
            ranking = st.multiselect("Rank candidates (most to least preferred)", candidates, default=candidates, key=f"condorcet_{i}")
            rankings.append(ranking)
    
    if st.button("Find Condorcet Winner", use_container_width=True):
        st.warning("Condorcet implementation in progress!")

if __name__ == "__main__":
    main()
