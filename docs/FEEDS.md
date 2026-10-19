# Feeds

Awesome Physics ships an OPML file, [`dev/feeds.opml`](../dev/feeds.opml), that
can be imported into any feed reader (Feedly, Inoreader, Newsboat, Thunderbird,
FreshRSS, and so on).

## Source of truth

Feeds are maintained in [`dev/data/feeds.csv`](../dev/data/feeds.csv):

```csv
title,url,htmlUrl,category
Phys.org,https://phys.org/rss-feed/,https://phys.org/,Physics News
```

- `title` — display name in the feed reader.
- `url` — the RSS or Atom XML endpoint.
- `htmlUrl` — the human-readable website.
- `category` — the OPML folder the feed is placed in.

## Regenerating the OPML file

```sh
make opml
```

This runs `dev/scripts/generate_opml.py` and rewrites `dev/feeds.opml` as valid
OPML 2.0. Always commit the regenerated file together with the CSV change.

## Categories

Current categories:

- Preprints
- Physics News
- Particle Physics
- Astronomy and Space
- Journals
- Research
- Software and Tools

Add a new category by using a new value in the `category` column; the generator
creates the folder automatically.

## Good feed candidates

- Preprint servers with per-category feeds, such as arXiv.
- Laboratory and agency newsrooms.
- Open access journals that publish a feed.
- Community and Q&A sites with a feed.

Avoid feeds that are paywalled, unpublished, or updated less than once a year.
