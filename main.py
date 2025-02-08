import argparse
from src.fetch_papers import fetch_papers, filter_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed")
    parser.add_argument("query", type=str, help="Query string for PubMed search")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Output filename for the CSV")
    args = parser.parse_args()

    if args.debug:
        print(f"Debug: Fetching papers for query '{args.query}'")

    # Fetch papers
    print("Fetching papers...")
    papers = fetch_papers(args.query, debug=args.debug)
    print(f"Fetched {len(papers)} papers.")

    # Filter papers
    print("Filtering papers...")
    filtered_papers = filter_papers(papers)
    print(f"Filtered {len(filtered_papers)} papers.")

    # Save results
    if args.file:
        print(f"Saving results to {args.file}...")
        save_to_csv(filtered_papers, args.file)
        print("Save complete.")
    else:
        print(filtered_papers)

if __name__ == "__main__":
    main()
