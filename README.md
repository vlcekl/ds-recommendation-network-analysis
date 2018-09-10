# ds-recommendation-network-analysis

Publication recommendation system based on references found in Wikipedia
pages, and using categorization of topics on Wikipedia. The system recommends
and ranks most relevant publications related to a target publications.

The primary source of data for Wikipedia citation statistics comes from online
repository: https://analytics.wikimedia.org/datasets/archive/public-datasets/all/mwrefs/mwcites-20180301/

Additional information about grouping web pages based on categories is obtained by web scraping.

The relations between publications, topic pages, and categories are stored in
a directed graph structure using NetworkX library.

Web scraping is accomplishe using requests and BeautifulSoup libraries

