import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Carregar dados
# Lê o CSV com os dados coletados
df = pd.read_csv("../Api/data/raw/videos.csv")

# Garante que views sejam numéricos
df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0)

# 2. Filtrar top vídeos por impacto
# Mantém apenas os 250 vídeos mais vistos
df = df.sort_values(by="views", ascending=False).head(100)

# 3. Criar grafo (estrutura)
G = nx.Graph()

# adiciona todos os vídeos como nós
G.add_nodes_from(df["video_id"])

# Agrupa vídeos por canal
grouped = df.groupby("channel")

# Cria conexões entre vídeos do mesmo canal
for channel, group in grouped:
    videos = group["video_id"].tolist()

    # Conecta todos com todos (clique) - Cada vídeo terá a mesma centralidade dentro do canal, porém será medido os canais que mais prouziram conteúdo relacionado com o tema.
    for i in range(len(videos)):
        for j in range(i + 1, len(videos)):
            G.add_edge(videos[i], videos[j])

# 4. Métricas da rede
print("Número de nós Grafo principal:", G.number_of_nodes())
print("Número de arestas: Grafo principal", G.number_of_edges())
print("Coeficiente de clustering médio:", nx.average_clustering(G))

# Centralidades
degree_centrality = nx.degree_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# 5. Criar subgrafo (Top 50 mais importantes)
# Seleciona nós com maior centralidade
top_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:50] # type: ignore

G_small = G.subgraph(top_nodes)
print("Número de nós:", G_small.number_of_nodes())
print("Número de arestas:", G_small.number_of_edges())

# Recalcula centralidade para o subgrafo
degree_centrality_small = nx.degree_centrality(G_small)

# 6. Criar dicionários auxiliares
# Mapeia vídeo → canal
video_to_channel = dict(zip(df["video_id"], df["channel"]))

# Mapeia vídeo → views
views_dict = dict(zip(df["video_id"], df["views"]))

# Valor máximo de views (para normalização)
max_views = max(views_dict.values())

# 7. Criar cores por canal
# Apenas canais presentes no subgrafo
channels_in_graph = sorted(set(video_to_channel[node] for node in G_small.nodes()))

# Mapear canal → número
color_map = {channel: i for i, channel in enumerate(channels_in_graph)}

# Lista de cores (numérica)
num_channels = len(color_map)

colors = [
    color_map[video_to_channel[node]]
    for node in G_small.nodes()
]

# 8. Tamanho dos nós (modelo híbrido)
# Combina:
# - centralidade (estrutura)
# - views (impacto)
# Cada nó tera tamanho proporcional a quantidade de visualizações e a centralidade do nó, ou seja, os nós mais centrais e com mais visualizações serão maiores, destacando os vídeos mais relevantes dentro da rede.

sizes = []

for node in G_small.nodes():
    centrality = degree_centrality_small[node]
    views = views_dict[node]

    # Normaliza views
    views_norm = views / max_views if max_views > 0 else 0

    # Combinação ponderada
    size = (0.5 * centrality + 0.5 * views_norm) * 3000

    sizes.append(size)

# 9. Plot do grafo
plt.figure(figsize=(18, 12))

# Layout (organização dos nós)
pos = nx.spring_layout(G_small, k=1.2, iterations=100, seed=42)

# Desenha nós
nx.draw_networkx_nodes(
    G_small,
    pos,
    node_size=sizes,
    node_color=colors,
    cmap=plt.cm.tab20, # type: ignore
    vmin=0,
    vmax=len(color_map)-1,
    alpha=0.9
)

# Desenha arestas
nx.draw_networkx_edges(
    G_small,
    pos,
    edge_color='gray',
    alpha=0.25,
    width=0.8
)



# 11. Nome dos canais (clusters)
components = list(nx.connected_components(G_small))

for comp in components:
    video = list(comp)[0]
    channel = video_to_channel.get(video, "Unknown")

    # Posição média do cluster
    x = sum(pos[n][0] for n in comp) / len(comp)
    y = sum(pos[n][1] for n in comp) / len(comp)

    # Texto acima do cluster
    plt.text(
        x,
        y + 0.09,
        channel,
        fontsize=11,
        ha='center',
        fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
    )

# 12. Legenda
legend_handles = []

for channel, idx in color_map.items():
    color = plt.cm.tab20(idx / (len(color_map)-1 if len(color_map) > 1 else 1)) # type: ignore
    patch = mpatches.Patch(color=color, label=channel)
    legend_handles.append(patch)

plt.legend(handles=legend_handles, title="Canais", fontsize=9)

# 13. Título
plt.title(
    "Rede de Vídeos sobre Estreito de Ormuz\n"
    "Tamanho dos nós proporcional à centralidade e visualizações",
    fontsize=14
)

plt.axis("off")

# 14. Salvar imagem
plt.savefig("grafo_hibrido.png", dpi=300, bbox_inches='tight')
print("Grafo salvo como grafo_hibrido.png")