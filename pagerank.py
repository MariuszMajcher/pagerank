import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # OK so it seems that I have to return a dictionary here, that will correspond to the probabilites of the pages, 
    # page links each have proportion of 0.85 and all the pages in corpus have proportion of 0.15
    proportions = dict()

    # In case there are no links on that page
    if corpus[page] == {}:
        for page in list(corpus.keys()):
            proportions[page] = 1 / len(corpus)
        return proportions
    
    for page in corpus.keys():
        proportions[page] = ((1 - damping_factor) / len(corpus)) # Create each page with proportion of chance being choosen

    links = corpus[page]
    for link in links:
        proportions[link] += (damping_factor / len(links)) # This will add these pages proportion of 0.85
    return proportions



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    choosen_page = random.choice(list(corpus.keys()))
    i = 0

    # Create dictinary with 0 for each page, each page will add 1 visit to it, at the end will change it to create proportion of 1 instead by dividing each result by n
    probabilites = dict()
    for page in corpus.keys():
        probabilites[page] = 0

    probabilites[choosen_page] += 1

    while i < n:
        i += 1
        list_of_links = []
        proportions = transition_model(corpus, choosen_page, damping_factor)

        # TODO: New idea, the choosen page will be selected based on single random, that float will somehow link to the page choosen
        # TODO: So on each iteration will create a new dictionary, it will contain the low and high, 
        # First low is zero, first high is whatever the value at this page, next low is previous high and next high is value stored at this page,
        # Then generate random and return key that falls in the range of each stored tuple!
        # for key, times in list(proportions.items()):
        #     j = times * 1000
        #     while j > 0:
        #         list_of_links.append(key)

        # Thist might be slow but for now it`s only method that comes to my mind
        choosen_page = random.choice(list_of_links)
        probabilites[choosen_page] += 1

    for page in probabilites:
        probabilites[page] = probabilites[page] / n

    return probabilites 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    page_rank = dict()
    for page,links in corpus:
        page_rank[page] = 1/N
    converged = False
    while not converged:
        converged = True
        for page, page_r in page_rank:
            #Now need to finish the formula, not sure how to create it, 
            #Maybe best to create a separate function that can be called
            page_rank[page] = (1 - damping_factor) / N + damping_factor*(())


if __name__ == "__main__":
    main()
