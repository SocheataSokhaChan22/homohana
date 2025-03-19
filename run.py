import networkx as nx
import matplotlib.pyplot as plt

# Define tasks with dependencies
tasks = [
    {"Task ID": "T1", "Task Name": "Design Company Portfolio of UX/UI Projects", "Duration": 11, "Start Date": "2004-10-28", "End Date": "2004-11-08", "Dependency": None},
    {"Task ID": "T2", "Task Name": "Design Banking POS App for Merchant", "Duration": 13, "Start Date": "2004-10-20", "End Date": "2004-11-10", "Dependency": None},
    {"Task ID": "T3", "Task Name": "Refine Company Portfolio", "Duration": 15, "Start Date": "2004-11-08", "End Date": "2004-11-23", "Dependency": "T1"},
    {"Task ID": "T4", "Task Name": "Draft Wireframe for Government Website", "Duration": 10, "Start Date": "2004-11-22", "End Date": "2004-12-02", "Dependency": None},
    {"Task ID": "T5", "Task Name": "Revise UX/UI of Bank App for Merchandise", "Duration": 13, "Start Date": "2004-11-18", "End Date": "2004-12-01", "Dependency": "T2"},
    {"Task ID": "T6", "Task Name": "Redesign Company HR Management App", "Duration": 22, "Start Date": "2004-09-22", "End Date": "2004-12-26", "Dependency": None},
    {"Task ID": "T7", "Task Name": "Revise UX/UI of Car Listing Project Web Office", "Duration": 15, "Start Date": "2004-09-16", "End Date": "2004-12-10", "Dependency": None},
    {"Task ID": "T8", "Task Name": "Design UX/UI for Web Back Office for Logistics Co.", "Duration": 16, "Start Date": "2004-09-16", "End Date": "2005-01-01", "Dependency": None},
    {"Task ID": "T9", "Task Name": "Design Mobile App for Logistics Company", "Duration": 13, "Start Date": "2005-01-05", "End Date": "2005-01-21", "Dependency": "T8"},
    {"Task ID": "T10", "Task Name": "Payment System Design", "Duration": 12, "Start Date": "2005-01-20", "End Date": "2005-02-01", "Dependency": None},
    {"Task ID": "T11", "Task Name": "Sale System for Operator", "Duration": 11, "Start Date": "2005-01-22", "End Date": "2005-02-03", "Dependency": None},
    {"Task ID": "T12", "Task Name": "Sale System for Administrator", "Duration": 12, "Start Date": "2005-01-25", "End Date": "2005-02-06", "Dependency": "T11"},
    {"Task ID": "T13", "Task Name": "Redesign In-House Employee App", "Duration": 10, "Start Date": "2005-02-13", "End Date": "2005-09-10", "Dependency": None},
]

# Create a directed graph
G = nx.DiGraph()

# Add nodes (tasks) to the graph
for task in tasks:
    G.add_node(
        task["Task ID"],
        label=f"{task['Task ID']}\n{task['Task Name']}\nDuration: {task['Duration']} days\nStart: {task['Start Date']}\nEnd: {task['End Date']}",
    )

# Add edges (dependencies) to the graph
for task in tasks:
    if task["Dependency"]:
        G.add_edge(task["Dependency"], task["Task ID"])

# Define positions for nodes
pos = {
    "T1": (0, 3), "T2": (0, 2), "T3": (1, 3), "T4": (1, 1),
    "T5": (1, 2), "T6": (2, 0), "T7": (2, 1), "T8": (2, 2),
    "T9": (3, 2), "T10": (3, 1), "T11": (3, 0), "T12": (4, 0),
    "T13": (4, 1),
}

# Create the plot
plt.figure(figsize=(14, 8))

# Draw rectangular nodes
for node, (x, y) in pos.items():
    label = G.nodes[node]["label"]
    plt.gca().add_patch(plt.Rectangle((x - 0.4, y - 0.2), 0.8, 0.4, edgecolor="black", facecolor="skyblue", alpha=0.8))
    plt.text(x, y, label, ha="center", va="center", fontsize=8, fontweight="bold")

# Draw edges (dependencies)
for edge in G.edges():
    start_pos = pos[edge[0]]
    end_pos = pos[edge[1]]
    plt.arrow(
        start_pos[0], start_pos[1],
        end_pos[0] - start_pos[0], end_pos[1] - start_pos[1],
        head_width=0.05, head_length=0.1, fc="gray", ec="gray", linestyle="-", linewidth=1.5
    )

# Display the PERT Chart
plt.title("PERT Chart for Socheata Sokhachan's Projects", fontsize=16)
plt.axis("off")  # Turn off the axis
plt.tight_layout()
plt.show()