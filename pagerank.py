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
    choice = random()
    # Easiest for me will be to create a list with number of elements that adds up to a 1000, or 
    # 10000 with the proportional distirbution, and the choose at random from that list
    list_of_links =[]
    pages = corpus.keys()
    for page in pages:
        no_of_pages = corpus[page]*1000
        for n in range(no_of_pages):
            list_of_links.append(page)
    # TODO: ok Looks like I can change this, but I think I know how, Will need to create the 
    # TODO: probabilities in the list_of_links once and the select the link,
    # TODO: will need to write a simple equation that will define how many times each page 
    # TODO: will appear in the list
    if choice < damping_factor:
        # Here it needs to return only the page from the page dict, to choose from the links in 
        # that page
        return random.choice(list_of_links)
    else:
        page, links = random.choice(list(corpus.items()))
        return page


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    i = 0
    page_rank = dict()
    for page, __ in corpus:
        page_rank[page] = 0
    page_visited, __ = random.choice(list(corpus.items()))
    while i < n:
        page_visited = transition_model(corpus, page_visited, damping_factor)
        page_rank[page_visited] += 1
        #This currently returns not the percentage point, so will need to add
        # all the values and find part
    return page_rank


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
