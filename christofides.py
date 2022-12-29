from heapq import heappop, heappush
import matplotlib.pyplot as plt
import networkx as nx
import itertools,random,time
def prim(graph, start):
  mst = []
  pq = []
  heappush(pq, (0, start, start))
  visited = set()
  while pq:
    weight, u, v = heappop(pq)
    if v in visited:continue
    if u!=v:mst.append((u, v, weight))
    visited.add(v)
    for neighbor, weight in graph[v]:
      if neighbor not in visited:
        heappush(pq, (weight, v, neighbor))
  return mst
def tree_to_graph(tree):
  graph={}
  tree_vertices=set([x for tup in tree for x in [tup[0],tup[1]]])
  for vertex in tree_vertices:graph[vertex]=[]
  for tup in tree:
    src,dest,weight=tup
    graph[src].append((dest,weight))
  return graph
def nx_to_graph(nx_item):
  graph={}
  tree_vertices=nx_item.nodes()
  for vertex in tree_vertices:graph[vertex]=[]
  nx_attributes=nx.get_edge_attributes(nx_item,'weight')
  for tup in nx_attributes:
    src,dest=tup
    graph[src].append((dest,nx_attributes[tup]))
  return graph
def odd_degree(tree):
  tree_vertices=set([x for tup in tree for x in [tup[0],tup[1]]])
  converted=tree_to_graph(tree)
  tree_graph = nx.Graph()
  for vertex in converted.keys():
    tree_graph.add_node(vertex)
    for neighbor,weight in converted[vertex]:tree_graph.add_edge(vertex, neighbor, weight=weight)
  odd_stable=[]
  for vertex in tree_vertices:
    if tree_graph.degree[vertex]%2!=0:
      odd_stable.append(vertex)
  return odd_stable
def get_cycle_edges(cycle):
  edges=[]
  for i in range(len(cycle)):
    try:
      edge=(cycle[i],cycle[i+1])
      edges.append(edge)
    except:pass
  return edges
def find_perfect_matching(graph_data):
  def calculate_score(matching):
    score=sum([x[2] for x in matching])
    return score
  matchings=[]
  vertices=set()
  edges=set()
  for vertex in graph_data:
    vertices.add(vertex)
    for tup in graph_data[vertex]:vertices.add(tup[0])
  for vertex in graph_data:
    for tup in graph_data[vertex]:edges.add((vertex,*tup))
  bulk_matchings=set()
  for comb in itertools.combinations(list(edges), len(vertices)//2):
    bulk_matchings.add(comb)
  bulk_matchings=[list(i) for i in bulk_matchings]
  for matching in bulk_matchings:
    involved_vertices=set()
    for tup in matching:
      involved_vertices.add(tup[0])
      involved_vertices.add(tup[1])
    if len(involved_vertices)==len(vertices):
      matchings.append(matching)
  best_matching=min(matchings,key=calculate_score)
  return best_matching
def calculate_eulerian(data):
  tmp=data.copy()
  cycle=[]
  starting_edge=random.choice(tmp)
  tmp.remove(starting_edge)
  start,end,_=starting_edge
  cycle.append(start)
  print(start,tmp)
  current_edge=starting_edge
  while tmp:
    found_new=False
    start_time=time.time()
    while not found_new:
      if time.time()-start_time>=5:
        return calculate_eulerian(data)
      new_edge_index=random.randint(0,len(tmp)-1)
      new_edge=tmp[new_edge_index]
      if (new_edge[0]!=start and new_edge[1]==end):
        new_edge=(new_edge[1],new_edge[0],new_edge[2])
        tmp[new_edge_index]=new_edge
      if new_edge[0]==end:
        current_edge=new_edge
        found_new=True
    start,end,_=current_edge
    cycle.append(start)
    tmp.remove(current_edge)
    print(start,end,tmp)
  cycle.append(end)
  return cycle
def remove_dupes(cycle):
  visited=[]
  for vertex in cycle:
    if vertex not in visited:
      visited.append(vertex)
  visited.append(visited[0])
  return visited
def draw_graph(graph):
  G = nx.Graph()
  for vertex in graph.keys():
    G.add_node(vertex)
    for neighbor in graph[vertex]:
      G.add_edge(vertex, neighbor)
  pos = nx.circular_layout(G)
  nx.draw_networkx_nodes(G, pos, node_size=500,node_color='k', alpha=0.9)
  labels = {vertex: str(vertex) for vertex in G.nodes()}
  nx.draw_networkx_labels(G, pos, labels=labels, font_weight='bold', font_size=16,font_color='white')
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.9 , connectionstyle='arc1, rad = 0.2')
  return G,pos
def draw_weighted_graph(graph):
  G = nx.Graph()
  for vertex in graph.keys():
    G.add_node(vertex)
    for neighbor,weight in graph[vertex]:
      G.add_edge(vertex, neighbor, weight=weight)
  pos = nx.circular_layout(G)
  nx.draw_networkx_nodes(G, pos, node_size=500,node_color='k', alpha=0.9)
  labels = {vertex: str(vertex) for vertex in G.nodes()}
  nx.draw_networkx_labels(G, pos, labels=labels, font_weight='bold', font_size=16,font_color='white')
  nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.9 , connectionstyle='arc3, rad = 0.3')
  nx.draw_networkx_edge_labels(graph,pos,edge_labels=nx.get_edge_attributes(G, "weight"))
  return G,pos
def draw_tree(graph,tree,pos,v_color='green',e_color='green'):
  drawn=nx.Graph()
  converted=tree_to_graph(tree)
  for vertex in converted.keys():
    drawn.add_node(vertex)
    for neighbor,weight in converted[vertex]:
      drawn.add_edge(vertex, neighbor, weight=weight)
  tree_vertices=list(converted)
  tree_edges=[(tup[0],tup[1]) for tup in tree]
  color_map = [e_color if vertex in tree_vertices else 'k' for vertex in graph.nodes()]
  nx.draw_networkx_nodes(graph, pos, node_size=500,node_color=color_map, alpha=0.9)
  color_map = [v_color if edge in tree_edges else 'gray' for edge in graph.edges()]
  nx.draw_networkx_edges(graph, pos, edge_color=color_map, width=3 , connectionstyle='arc3, rad = 0.3')
  nx.draw_networkx_edge_labels(graph,pos,edge_labels=nx.get_edge_attributes(graph, "weight"))
  return drawn
def draw_cycle(graph,pos,cycle,c_color='r'):
  color_map = []
  for vertex in graph.nodes():
    if vertex==cycle[0]:color_map.append('blue') 
    elif vertex in cycle:color_map.append(c_color)
    else:color_map.append('k')      
  nx.draw_networkx_nodes(graph, pos, node_size=500,node_color=color_map, alpha=0.9)
  nx.draw_networkx_edges(graph, pos, edgelist=get_cycle_edges(cycle), edge_color=c_color, width=3 , connectionstyle='arc3, rad = 0.3')
  nx.draw_networkx_edge_labels(graph,pos,edge_labels=nx.get_edge_attributes(graph, "weight"))
def draw_subgraph(graph,subgraph,tree,pos,s_color='yellow',t_color='green'):
  color_map=[]
  s_edges=subgraph.edges()
  s_vertices=subgraph.nodes()
  t_edges=tree.edges()
  t_vertices=tree.nodes()
  for node in graph.nodes():
    if node in s_vertices:color_map.append(s_color)
    elif node in t_vertices:color_map.append(t_color)
    else:color_map.append('k')
  nx.draw_networkx_nodes(graph, pos, node_size=500,node_color=color_map, alpha=0.9)
  plt.pause(1)
  color_map=[]
  for edge in graph.edges():
    if edge in s_edges:color_map.append(s_color)
    elif edge in t_edges:color_map.append(t_color)
    else:color_map.append('gray')
  nx.draw_networkx_edges(graph, pos, edge_color=color_map, width=3 , connectionstyle='arc3, rad = 0.3')
  nx.draw_networkx_edge_labels(graph,pos,edge_labels=nx.get_edge_attributes(graph, "weight"))
  pass
def draw_matching(graph,matching,subgraph,tree,pos,m_color='brown',s_color='yellow',t_color='green'):
  color_map=[]
  s_edges=subgraph.edges()
  s_vertices=subgraph.nodes()
  t_edges=tree.edges()
  t_vertices=tree.nodes()
  m_edges=matching.edges()
  m_vertices=matching.nodes()
  for node in graph.nodes():
    if node in m_vertices:color_map.append(m_color)
    elif node in s_vertices:color_map.append(s_color)
    elif node in t_vertices:color_map.append(t_color)
    else:color_map.append('k')
  nx.draw_networkx_nodes(graph, pos, node_size=500,node_color=color_map, alpha=0.9)
  color_map=[]
  for edge in graph.edges():
    if edge in m_edges:color_map.append(m_color)
    elif edge in s_edges:color_map.append(s_color)
    elif edge in t_edges:color_map.append(t_color)
    else:color_map.append('gray')
  nx.draw_networkx_edges(graph, pos, edge_color=color_map, width=3 , connectionstyle='arc3, rad = 0.3')
  nx.draw_networkx_edge_labels(graph,pos,edge_labels=nx.get_edge_attributes(graph, "weight"))
  pass
def christofides(graph):
  # Step 1 : Plot Graph
  drawn,pos=draw_weighted_graph(graph)
  plt.pause(1)
  # Step 2 : Get Minimum Spanning Tree
  spanning_tree=prim(graph,0)
  drawn_tree=draw_tree(drawn,spanning_tree,pos)
  plt.pause(1)
  # Step 3 : Get Odd Degree Vertices in Spanning Tree
  odd_stable=odd_degree(spanning_tree)
  # Step 4 : Get Subgraph from Odd Degree Vertices
  odd_subgraph=drawn.subgraph(odd_stable)
  drawn_subgraph=draw_subgraph(drawn,odd_subgraph,drawn_tree,pos,'yellow','green')
  plt.pause(1)
  odd_subgraph_data=nx_to_graph(odd_subgraph)
  # Step 5 : Get perfect Matching from subgraph
  perfect_matching=find_perfect_matching(odd_subgraph_data)
  unweighted_pm=list(set([(x[0],x[1]) for x in perfect_matching]))
  pm_subgraph=drawn.edge_subgraph(unweighted_pm)
  drawn_pm=draw_matching(drawn,pm_subgraph,odd_subgraph,drawn_tree,pos,'brown','yellow','green')
  # Step 6: Merge perfect matching and spanning tree
  plt.pause(1)
  eulerian_multigraph_data=list(spanning_tree+perfect_matching)
  drawn_eulerian=draw_tree(drawn,eulerian_multigraph_data,pos,'pink','pink')
  plt.pause(1)
  # Step 7 : Calculate Eulerian cycle from obtained graph
  eulerian_cycle=calculate_eulerian(eulerian_multigraph_data)
  # Step 8 : Remove duplicated vertices from eulerian cycle
  hamiltonian_cycle=remove_dupes(eulerian_cycle)
  cycle_edges=get_cycle_edges(hamiltonian_cycle)
  print(cycle_edges)
  if hamiltonian_cycle:
    print('Cycle Hamiltonien trouvé : '+str(hamiltonian_cycle))
  # Step 8 : Draw Hamiltionian cycle
    draw_cycle(drawn,pos,hamiltonian_cycle)
  plt.show()
christofides({
  0: [(1,1),(3,4),(4,2)],
  1: [(2,4),(3,1)],
  2: [(0,4),(3,1)],
  3: [],
  4: [(1,1)]
})