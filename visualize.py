import matplotlib.pyplot as plt
import networkx as nx
from Graph import *
from cutset import is_connected_after_removal
from itertools import combinations

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.nx_graph = self._convert_to_networkx()
    
    def _convert_to_networkx(self):
        """Convert our custom Graph to NetworkX graph for visualization"""
        G = nx.Graph()
        
        # Add all nodes
        for node in self.graph.adj:
            G.add_node(node)
        
        # Add all edges (avoid duplicates)
        added_edges = set()
        for node in self.graph.adj:
            for neighbor in self.graph.adj[node]:
                edge = tuple(sorted([node, neighbor]))
                if edge not in added_edges:
                    G.add_edge(node, neighbor)
                    added_edges.add(edge)
        
        return G
    
    def visualize_original(self, title="Original Graph", save_path=None):
        """Visualize the original graph"""
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.nx_graph, seed=42)
        
        nx.draw_networkx_nodes(self.nx_graph, pos, 
                              node_color='lightblue', 
                              node_size=1500,
                              alpha=0.9)
        nx.draw_networkx_labels(self.nx_graph, pos, 
                               font_size=16, 
                               font_weight='bold')
        nx.draw_networkx_edges(self.nx_graph, pos, 
                              width=2, 
                              alpha=0.6)
        
        plt.title(title, fontsize=18, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Saved: {save_path}")
        
        plt.close()
        return pos
    
    def visualize_with_cutset(self, cutset_nodes, pos=None, save_path=None):
        """Visualize graph with cutset nodes highlighted"""
        if pos is None:
            pos = nx.spring_layout(self.nx_graph, seed=42)
        
        plt.figure(figsize=(10, 8))
        
        # Separate nodes into cutset and non-cutset
        cutset = set(cutset_nodes)
        normal_nodes = [n for n in self.nx_graph.nodes() if n not in cutset]
        
        # Draw normal nodes
        nx.draw_networkx_nodes(self.nx_graph, pos,
                              nodelist=normal_nodes,
                              node_color='lightblue',
                              node_size=1500,
                              alpha=0.9)
        
        # Draw cutset nodes in red
        nx.draw_networkx_nodes(self.nx_graph, pos,
                              nodelist=list(cutset_nodes),
                              node_color='red',
                              node_size=1500,
                              alpha=0.9)
        
        nx.draw_networkx_labels(self.nx_graph, pos,
                               font_size=16,
                               font_weight='bold',
                               font_color='white')
        nx.draw_networkx_edges(self.nx_graph, pos,
                              width=2,
                              alpha=0.6)
        
        plt.title(f"Graph with Cutset (Red): {cutset_nodes}", 
                 fontsize=18, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Saved: {save_path}")
        
        plt.close()
        return pos
    
    def visualize_after_removal(self, removed_nodes, pos=None, save_path=None):
        """Visualize graph after removing cutset nodes"""
        if pos is None:
            pos = nx.spring_layout(self.nx_graph, seed=42)
        
        # Create a new graph without the removed nodes
        G_after = self.nx_graph.copy()
        G_after.remove_nodes_from(removed_nodes)
        
        plt.figure(figsize=(10, 8))
        
        # Get connected components
        components = list(nx.connected_components(G_after))
        
        # Color nodes by component
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'plum']
        
        for i, component in enumerate(components):
            color = colors[i % len(colors)]
            nx.draw_networkx_nodes(G_after, pos,
                                  nodelist=list(component),
                                  node_color=color,
                                  node_size=1500,
                                  alpha=0.9,
                                  label=f'Component {i+1}')
        
        # Only draw labels and edges for remaining nodes
        remaining_labels = {n: n for n in G_after.nodes()}
        nx.draw_networkx_labels(G_after, pos,
                               labels=remaining_labels,
                               font_size=16,
                               font_weight='bold')
        nx.draw_networkx_edges(G_after, pos,
                              width=2,
                              alpha=0.6)
        
        connected = nx.is_connected(G_after) if len(G_after.nodes()) > 0 else False
        status = "CONNECTED" if connected else "DISCONNECTED"
        
        plt.title(f"After Removing {removed_nodes}\nGraph is {status} ({len(components)} component(s))",
                 fontsize=18, fontweight='bold')
        
        if len(components) > 1:
            plt.legend(loc='upper right', fontsize=12)
        
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Saved: {save_path}")
        
        plt.close()
        return pos
    
    def show_cutset_comparison(self, cutset_nodes, save_path=None):
        """Show before and after side by side"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        pos = nx.spring_layout(self.nx_graph, seed=42)
        
        # Before (with cutset highlighted)
        plt.sca(ax1)
        cutset = set(cutset_nodes)
        normal_nodes = [n for n in self.nx_graph.nodes() if n not in cutset]
        
        nx.draw_networkx_nodes(self.nx_graph, pos,
                              nodelist=normal_nodes,
                              node_color='lightblue',
                              node_size=1500,
                              alpha=0.9,
                              ax=ax1)
        nx.draw_networkx_nodes(self.nx_graph, pos,
                              nodelist=list(cutset_nodes),
                              node_color='red',
                              node_size=1500,
                              alpha=0.9,
                              ax=ax1)
        nx.draw_networkx_labels(self.nx_graph, pos,
                               font_size=16,
                               font_weight='bold',
                               font_color='white',
                               ax=ax1)
        nx.draw_networkx_edges(self.nx_graph, pos,
                              width=2,
                              alpha=0.6,
                              ax=ax1)
        ax1.set_title(f"BEFORE: Cutset Nodes (Red)\n{cutset_nodes}",
                     fontsize=16, fontweight='bold')
        ax1.axis('off')
        
        # After
        plt.sca(ax2)
        G_after = self.nx_graph.copy()
        G_after.remove_nodes_from(cutset_nodes)
        
        components = list(nx.connected_components(G_after))
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'plum']
        
        for i, component in enumerate(components):
            color = colors[i % len(colors)]
            nx.draw_networkx_nodes(G_after, pos,
                                  nodelist=list(component),
                                  node_color=color,
                                  node_size=1500,
                                  alpha=0.9,
                                  ax=ax2,
                                  label=f'Component {i+1}')
        
        remaining_labels = {n: n for n in G_after.nodes()}
        nx.draw_networkx_labels(G_after, pos,
                               labels=remaining_labels,
                               font_size=16,
                               font_weight='bold',
                               ax=ax2)
        nx.draw_networkx_edges(G_after, pos,
                              width=2,
                              alpha=0.6,
                              ax=ax2)
        
        connected = nx.is_connected(G_after) if len(G_after.nodes()) > 0 else False
        status = "CONNECTED" if connected else "DISCONNECTED"
        
        ax2.set_title(f"AFTER: Removed Cutset\nGraph is {status} ({len(components)} component(s))",
                     fontsize=16, fontweight='bold')
        
        if len(components) > 1:
            ax2.legend(loc='upper right', fontsize=12)
        
        ax2.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  Saved: {save_path}")
        
        plt.close()


def find_and_visualize_cutset(graph, k, output_dir="visualizations"):
    """Find a k-cutset and visualize it"""
    import os
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\nCreated directory: {output_dir}/")
    
    print(f"\n{'='*60}")
    print(f"Searching for a {k}-cutset...")
    print(f"{'='*60}")
    
    nodes = list(graph.adj.keys())
    visualizer = GraphVisualizer(graph)
    
    # Show original graph first
    print("\nSaving original graph...")
    original_path = f"{output_dir}/original_graph.png"
    visualizer.visualize_original(f"Original Graph ({len(nodes)} nodes)", save_path=original_path)
    
    # Try all combinations of k nodes
    found = False
    for combo in combinations(nodes, k):
        removed = set(combo)
        
        if not is_connected_after_removal(graph, removed):
            print(f"\n✓ Cutset found: {combo}")
            print("  Removing these nodes disconnects the graph!")
            
            # Show comparison
            combo_str = "_".join(str(c) for c in combo)
            comparison_path = f"{output_dir}/cutset_{k}_comparison_{combo_str}.png"
            visualizer.show_cutset_comparison(combo, save_path=comparison_path)
            
            found = True
            break
    
    if not found:
        print(f"\n✗ No {k}-cutset exists in this graph.")
        print(f"  The graph cannot be disconnected by removing {k} nodes.")
    
    return found


# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("GRAPH CUTSET VISUALIZER")
    print("="*60)
    
    # Test with the graph from Graph.py
    print("\nTesting with default graph from Graph.py")
    print("Graph structure:")
    print("  Nodes: A, B, C, D, E, F")
    print("  Edges: A-B, A-C, A-D, D-E, D-F")
    
    # Find and visualize different k-cutsets
    find_and_visualize_cutset(graph, 1)
    find_and_visualize_cutset(graph, 2)
    find_and_visualize_cutset(graph, 3)