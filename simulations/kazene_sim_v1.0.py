import networkx as nx
import random
import matplotlib.pyplot as plt

# ----------------------------
# PARAMETERS
# ----------------------------
num_queries = 5
steps = 50
growth_rate = 0.2       # probability of adding new node
decay = 0.9             # influence decay per generation
TV = 1000               # Total Value for royalty distribution

# ----------------------------
# INITIALIZATION
# ----------------------------
G = nx.DiGraph()
influence = {}

# Create initial queries
for i in range(num_queries):
    node = f"Query_{i}"
    G.add_node(node, generation=0)
    influence[node] = 1.0

# ----------------------------
# SIMULATION LOOP
# ----------------------------
for step in range(steps):
    nodes = list(G.nodes)

    for node in nodes:
        if random.random() < growth_rate:
            new_node = f"{node}_gen_{step}"
            gen = G.nodes[node]["generation"] + 1
            G.add_node(new_node, generation=gen)
            G.add_edge(node, new_node)

            # influence decays with generation depth
            influence[new_node] = influence[node] * decay

# ----------------------------
# FINAL INFLUENCE CALCULATION
# ----------------------------
total_IS = sum(influence.values())

royalties = {
    node: (influence[node] / total_IS) * TV
    for node in G.nodes
}

# ----------------------------
# OUTPUT SUMMARY
# ----------------------------
print("Total nodes:", len(G.nodes))
print("Total influence:", round(total_IS, 3))
print("\nRoyalty distribution (top 10):\n")

for n, r in list(sorted(royalties.items(), key=lambda x: -x[1]))[:10]:
    print(n, "=>", round(r, 3))

# ----------------------------
# OPTIONAL VISUALIZATION
# ----------------------------
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, node_size=20, arrows=False)
plt.title("Kazene Civilization Network Expansion")
plt.show()
