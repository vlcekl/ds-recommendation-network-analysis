import networkx as nx
from collections import Counter, defaultdict
from .read_wiki import get_cats, pub_info, get_cat_children


class GraphRank:
    """
    Class containing reference graph and methods to construct and query it.
    """

    def __init__(self):
        """
        Initialize a directed graph
        """

        self.G = nx.DiGraph()



    def build_graph(self, df, page_title, page_id, pub_type, pub_id):
        """
        Reads publication and wikipedia data from a pandas dataframe and returns a directed graph
        representing references from the wiki pages to the publications.
        
        Parameters
        ----------
        df: pandas data fram
            contains all available publication and wikipedia data and their relations (refrences)
        wiki_title: str
                    wikipedia topic page title
        wiki_id: int64
                 wikipedia page id
        pub_type: str
                  Type of the publication id (e.g., isbn, doi, ...)
        pub_id: str
                  Publication id of a given type
        
        Returns
        -------
        G: networkx digraph object
        """
        
        # list of unique web page ids (web_page nodes)
        wp_ids = df[page_id].unique()
 
        # list of unique web page names
        wp_titles = df[page_title].unique()
        wp_set = set(wp_titles)
 
        # list of unique publications (publication nodes)
        pub_ids = [(ptype, pid) for ptype, pid in df[[pub_type, pub_id]].values]
        pub_set = set(pub_ids)
 
        # list of references (edges)
        edges = [(page, (ptype, pid)) for page, ptype, pid in df[[page_title, pub_type, pub_id]].values]
        
        # creata a node lists for the use in the graph
        wp_node_list = [(title, {'bipartite':'web_page', 'pid': pid,'address':'/wiki/'+title.replace(' ','_'), 'ptype':'topic','depth':0}) for pid, title in zip(wp_ids, wp_titles)]
        pub_node_list = [(pub_id, {'bipartite':'publication', 'ptype':'pub'}) for pub_id in pub_ids] #, 'type':pub_id
        
        self.G.add_nodes_from(wp_node_list)  #, bipartite='web_page')
        self.G.add_nodes_from(pub_node_list) #, bipartite='publication')
        self.G.add_edges_from(edges)

        self.wpage_nodes = [(node, data) for node, data in self.G.nodes(data=True) if data['bipartite']=='web_page']

        # set for quickly checking presence of web_page nodes
        self.node_titles = set([node for node, data in self.G.nodes(data=True) if data['bipartite']=='web_page'])


    def add_cats(self, wpage_nodes, node_titles):
        """
        Add nodes with category pages.
        """

        for node in wpage_nodes:
 
            # get the address of the page
            address = node[1]['address']
 
            # scrape the page and return tags for categories
            cats = get_cats(address)
 
            # create nodes for the categories (if new)
            for c in cats:
 
                # get category page title (== node identification)
                title = c.get_text()
 
                if title not in node_titles:
 
                    # get category page address
                    cat_ref = c.get('href')
 
                    # create a new node tuple
                    new_node = (title, {'address':cat_ref, 'ptype':'category'})
 
                    # create a new node
                    self.SG.add_node(title, address=cat_ref, ptype='category')
 
                    # update queue and node_titles set
                    node_titles.add(title)
                    
                # create a new edge pointing from higher level category to the present page
                self.SG.add_edge(title, node[0])

    def add_pages(self, cat, wpage_tags):
        """
        Add nodes with category pages.
        """

        # list of all topic nodes
        node_titles = [node for node, data in self.G.nodes(data=True) if data['ptype'] == 'topic']

        # create nodes for the categories (if new)
        for c in wpage_tags:
 
            # get category page title (== node identification)
            title = c.get_text()

            if title in node_titles:
 
                # create a new node
                self.SG.add_node(title, self.G.node[title])

                # create a new edge pointing from higher level category to the present page
                self.SG.add_edge(cat[0], title)
 

    def rank_publications(self):
        """
        Calcualate bipartite degree centrality ranking of publications within a given graph G.
        
        Parameters
        ----------
        G: networkx graph object
           usually a subgraph of the main graph containing publication nodes (bipartite=publication)
        
        Returns
        -------
        pub_rank: list of tuples (graph node, degree centrality) ordered by degree centrality
        """
        
        # Select publication and topic page nodes
        pub_nodes = [node for node, data in G.nodes(data=True) if data['bipartite'] == 'publication']
        wpage_nodes = [node for node, data in G.nodes(data=True) if data['bipartite'] == 'web_page']
 
        # Create a bipartite subgraph of topic nodes and publications
        SG = self.G.subgraph(pub_nodes + wpage_nodes)
 
        # calcualate degree centrality
        dcent = nx.bipartite.degree_centrality(SG, wpage_nodes)
        
        # save webpage nodes with their degree centrality
        pub_dcent = [(node, dcent[node]) for node in pub_nodes]
        
        # sort publication nodes from highest to lowest
        pub_rank = sorted(pub_dcent, key=lambda x: x[1], reverse=True)
        
        return pub_rank


    def find_most_relevant(self, publication, n_highest_pubs=10):
        """
        Finds and prints N most relevant publications to the original publication (based on citations)
        
        Parameters
        ----------
        publication: tuple (str, str)
                     Identification of the original publication based on id type and number
        n_highest_pubs: int
                        number of publications to list
                        
        Returns
        -------
        Prints list on the screen
        """
        
        # Original publication and its wikipedia citations
        print('Original publication:', publication, '\nTitle:', pub_info(publication)[1],'\n\n')
        page_list = self.G.predecessors(publication)
        print(len(page_list), 'pages referring to the publication:\n', page_list,'\n\n')
        
        # Level 1 - citing topic pages
        # Find all publications referenced by wiki pages that also cite the original publication
        level1_pubs = []
        for page in page_list:
            level1_pubs.extend([pub for pub in self.G.successors(page)])

        # Select N most highly cited publications
        pub_counts = Counter(level1_pubs)
        del pub_counts[publication]
        most_cited = pub_counts.most_common(n_highest_pubs)

        # Print information about highly cited publications
#        for i, pub in enumerate(most_cited, 1):
#            info = pub_info(pub[0])
#            print('Rank:', i, '\nCitations:', pub[1])
#            print('ID:', pub[0])
#            print('Source:', info[0])
#            print('Title:', info[1],'\n')

        # Level 2 - Categories from citing topic pages
        # Find pages linked to the topic pages through common category
        # Get additional publications through their descendants (exclude those in level 1)

        # create a subgraph of related pages and publications
        self.SG = self.G.subgraph(page_list + level1_pubs)
        
        wpage_nodes = [(node, data) for node, data in self.SG.nodes(data=True) if data['bipartite']=='web_page']
        node_titles = set([node for node, data in self.SG.nodes(data=True) if data['bipartite']=='web_page'])

        # Add category nodes and descending pages
        self.add_cats(wpage_nodes, node_titles)

        # Go through category nodes and get their publication children
        cat_nodes = [(node, data) for node, data in self.SG.nodes(data=True) if data['ptype']=='category']
        print('Number of categories for level 2 publications:', len(cat_nodes))

        level2_pubs = []
        for cat in cat_nodes:
            wpage_tags = get_cat_children(cat[0])

            # Add topic nodes and edges to the subgraph
            self.add_pages(cat, wpage_tags)

        wpage_nodes = [(node, data) for node, data in self.SG.nodes(data=True) if data['ptype']=='topic']

        level2_pubs = []
        for page in wpage_nodes:
            level2_pubs.extend([pub for pub in self.G.successors(page[0])])

        pub_counts2 = Counter(level2_pubs)

        # Find and merge duplicates
        num_pub = n_highest_pubs*3 if n_highest_pubs*3 < len(pub_counts2) else len(pub_counts2)
        most_cited2 = pub_counts2.most_common(num_pub)
        select_pubs = defaultdict(dict)
        pub_titles = defaultdict(int)
        for i, pub in enumerate(most_cited2, 1):
            info = pub_info(pub[0])
            title = info[1]
            cites = pub[1]
            source = info[0]
            pubid = pub[0]
            select_pubs[title[:10]] = [title, cites, source, pubid]
            pub_titles[title[:10]] += cites
            if pub[0] == publication:
                title_orig = title[:10]


        # delete title references to the original publication
        del pub_titles[title_orig]

        pub_ranks = dict(sorted(pub_titles.items(), key=lambda x: x[1], reverse=True))

        for i, key in enumerate(pub_ranks, 1):
            cites = pub_ranks[key]
            pubid = select_pubs[key][3]
            link = select_pubs[key][2]
            title = select_pubs[key][0]

            print('Rank:', i, '\nCitations:', cites)
            print('ID:', pubid)
            print('Source:', link)
            print('Title:', title,'\n')
            if i == 13:
                break
            #print('Rank:', i, '\nCitations:', pub[1])
            #print('ID:', pub[0])
            #print('Source:', info[0])
            #print('Title:', info[1],'\n')

#        del pub_counts2[publication]
#        print('Total number of level 2 publications:', len(pub_counts2))
#        most_cited2 = pub_counts2.most_common(n_highest_pubs)
#
#        # Print information about highly cited publications
#        #for i, pub in enumerate(most_cited2, 1):
#        for i, pub in enumerate(selected, 1):
#            info = pub_info(pub[0])
#            print('Rank:', i, '\nCitations:', pub[1])
#            print('ID:', pub[0])
#            print('Source:', info[0])
#            print('Title:', info[1],'\n')

