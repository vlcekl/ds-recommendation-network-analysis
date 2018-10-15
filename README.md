# ds-recommendation-network-analysis

Publication recommendation system based on references found in Wikipedia
pages, and using categorization of topics on Wikipedia. The system recommends
and ranks most relevant publications related to a target publication based on
semantic closeness and number of references within the relevant categories.

The primary source of data for Wikipedia citation statistics comes from online
repository: https://analytics.wikimedia.org/datasets/archive/public-datasets/all/mwrefs/mwcites-20180301/

Additional information about grouping web pages based on categories is obtained by web scraping Wikipedia
and finding more detailed information about publications based on web scraping
other resources, such as Google search results.

The relations between publications, topic pages, and categories are stored in
a directed graph structure using NetworkX library. Web scraping is accomplishe using requests and BeautifulSoup libraries.

The main code including GraphRank class and web scraping functionality is
included in the src/recomm directory, an example and testing of the system is
presented in a Jupyter notebook, and additional documentation is in the
reports directory.

[Slide deck](./reports/recommendation_system_slide_deck.pdf) 
