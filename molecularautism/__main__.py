#!/usr/bin/env python

from .recent import MolecularAutismRecent


if __name__ == '__main__':
    latest_articles = MolecularAutismRecent()
    latest_articles.download_articles()
