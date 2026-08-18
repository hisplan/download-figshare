import json
import re
import urllib.request
import argparse
from urllib.parse import parse_qs, urlparse


def format_size(size_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


def parse_figshare_reference(reference):
    """Return (article_id, private_link) from a public URL, private URL, or raw ID."""
    text = str(reference).strip()

    if not text:
        raise ValueError("Figshare reference is empty.")

    if text.isdigit():
        return int(text), None

    parsed = urlparse(text)
    query = parse_qs(parsed.query)
    private_link = query.get("private_link", [None])[0]

    if parsed.netloc.endswith("figshare.com"):
        token_match = re.search(r"/s/([A-Za-z0-9]+)", text)
        if token_match:
            return None, token_match.group(1)

        match = re.search(r"/articles/(?:[^/]+/)?(\d+)(?:[/?#]|$)", text)
        if match:
            return int(match.group(1)), private_link

        match = re.search(r"/(?:s|articles(?:/dataset)?)/[^/]+/([^/?#]+)", text)
        if match and match.group(1).isdigit():
            return int(match.group(1)), private_link

    if "article_id" in query and query["article_id"]:
        return int(query["article_id"][0]), private_link

    match = re.search(r"/(\d+)(?:[/?#]|$)", text)
    if match:
        return int(match.group(1)), private_link

    raise ValueError(f"Could not extract a Figshare article ID from: {reference}")


def resolve_private_link_article_id(private_link):
    """Fetch a private shared-link page and extract the article ID from its HTML."""
    url = f"https://figshare.com/s/{private_link}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode("utf-8", errors="ignore")

    for pattern in (
        r'/articles/(?:[^/\"]+/)?(\d+)',
        r'"article_id"\s*:\s*(\d+)',
        r'"id"\s*:\s*(\d+)',
    ):
        match = re.search(pattern, html)
        if match:
            return int(match.group(1))

    raise ValueError(
        f"Could not resolve the article ID for private link '{private_link}'. "
        "Manually provide the article ID or pass a URL that includes it."
    )



def main(reference):

    article_id, private_link = parse_figshare_reference(reference)

    if article_id is None and private_link:
        article_id = resolve_private_link_article_id(private_link)

    api_url = f"https://api.figshare.com/v2/articles/{article_id}"
    if private_link:
        api_url += f"?private_link={private_link}"

    # Fetch metadata
    req = urllib.request.Request(api_url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode("utf-8"))

    # Print direct download URLs for each file
    for idx, file_info in enumerate(data.get("files", [])):
        print()
        print("-" * 150, idx + 1)
        print(file_info["name"])
        print(file_info["download_url"])
        print(format_size(file_info["size"]))
        print(f"curl -L -C - -o {file_info['name']} {file_info['download_url']}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get direct download links for files in a Figshare article."
    )
    parser.add_argument(
        "reference",
        type=str,
        help="Figshare article URL, private shared link, or article ID.",
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    reference = args.reference

    # reference = "https://figshare.com/ndownloader/articles/27261219?private_link=ee85bb1880921326249b"
    # reference = "https://plus.figshare.com/articles/dataset/Processed_data_for_X-Atlas_Orion_Genome-wide_Perturb-seq_Datasets_via_a_Scalable_Fix-Cryopreserve_Platform_for_Training_Dose-Dependent_Biological_Foundation_Models/29190726"

    main(reference)

