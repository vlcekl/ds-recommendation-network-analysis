# Recommendation system based on publication citation ranking

## The problem
Search for relevant literature is often a tedious procedure, that requires following a large number of links and, if performed by a human,
is prone to missing imporant sources. The goal of this project is to use public resources, such as Wikipedia, to develop a system that would automatically search large numbers of links
and recommend a publication to a customer either for purchase or as suggested reading. The value of such a system would follow from its higher speed and thoroughness compared
to manual search.

## Clients
1. A book selling company that is building a recommendation system based on user browsing data.
   Based on the suggestions of the proposed system, the seller will be able to place tailored advertising or other suggestions for the customer,
   and increase thus chances of succesful sale.
2. Independent researchers or institutions seeking to speedup and automate relevant literature search and meta-analysis studies of published research.
   Given the explosion of scientific and other publications, relevant research is .
   The recommendation system could possibly be extended to work with other online resources and gradually built up
   to create a map of research areas or, in general, knowledge for further machine learning-powered science.

## Datasets
The main source of data will be the open wkimedia dataset on citations 
1. Wikimedia open data set available for download: https://analytics.wikimedia.org/datasets/archive/public-datasets/all/mwrefs/
2. Wikipedia traffic trends available for download: http://dumps.wikimedia.org/other/pagecounts-raw/
3. Webscraping wikipedia through its API and the corresponding python library
   for specific information about the pages.

## Approach

1. Gather data through direct download and web scraping using python Wikipedia API
2. Construct a bipartite graph between Wikipedia web pages and publications.
3. Assign values to the Wikipedia nodes identifying the categories into witch
   they belong.
4. Assign additional values (ranks) based on popularity of the pages based on the
   traffic dataset.
5. Using NetworkX library, analyze the bipartite graph to find subgraphs based on node categories,
   determine characteristics such as the degree centrality, betweenness
   centrality, closeness centrality. Use this information to build a list of
   close publications according to their citations and the page popularity.
6. Build a recommendation system suggesting literature based on viewed
   Wikipedia pages and selected publications. Rank the suggestions and provide
   basic information about the publication.
7. Extend the system by including the possibility of entering a specific
   publication or category to receive recommendations.

## Deliverables
The completed system will take a list of publications or wiki pages as input and suggests a list of other, most relevant publications.
It will also highlight new publications, whose popularity is quickly rising.

The deliverables will include the code in the form of jupyter notebooks on
exploratory and statistical network analysis, as well as a recommendation
system based on the analysis. The results will be described in a separate paper and a slide deck.
