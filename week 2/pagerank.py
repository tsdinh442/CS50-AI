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
    d = (1 - damping_factor) / len(corpus)
    temp = dict.fromkeys(corpus.keys(), d)
 
    if corpus[page]:
        for link in corpus[page]:
            temp[link] += damping_factor / len(corpus[page])
    else:
        for p in corpus:
            temp[p] += damping_factor / len(corpus)
        
    return temp

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    temp = dict.fromkeys(corpus.keys(), 0)
    page = random.choice(list(corpus.keys()))
    temp[page] += 1 / n
    for i in range(n - 1):           
        m = transition_model(corpus, page, damping_factor)
        page = random.choices(list(m.keys()), list(m.values()))
        page = page[0]
        temp[page] += 1 / n
        
    return temp


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    THRESHOLD = 0.0005
    d = (1 - damping_factor) / len(corpus)
    b = dict.fromkeys(corpus.keys(), False)
    temp = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    
    while True:
        for m in corpus:
            sigma = 0
            for n in corpus:
                if m in corpus[n]:
                    sigma += temp[n] / len(corpus[n])
            new = d + damping_factor * sigma

            if abs(new - temp[m]) < THRESHOLD:
                b[m] = True
            temp[m] = new

        if all(value == True for value in b.values()):
            break
             
    return temp

if __name__ == "__main__":
    main()
