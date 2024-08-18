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
    proportions = {}

    # Case where the page has no outgoing links
    if len(corpus[page]) == 0:
        for p in corpus:
            proportions[p] = 1 / len(corpus)
    else:
        # Distribute the random jump probability
        for p in corpus:
            proportions[p] = (1 - damping_factor) / len(corpus)

        # Distribute the damping factor among linked pages
        for link in corpus[page]:
            proportions[link] += damping_factor / len(corpus[page])

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

    # Initialize the probabilities dictionary
    probabilities = {page: 0 for page in corpus.keys()}

    # Start by sampling the first page
    probabilities[choosen_page] += 1

    for _ in range(1, n):  # already sampled the first page
        proportions = transition_model(corpus, choosen_page, damping_factor)
        choice = random.random()

        cumulative_probability = 0.0
        for page, prob in proportions.items():
            cumulative_probability += prob
            if choice < cumulative_probability:
                choosen_page = page
                probabilities[page] += 1
                break

    # Normalize the probabilities
    probabilities = {page: count / n for page, count in probabilities.items()}
    
    return probabilities



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
