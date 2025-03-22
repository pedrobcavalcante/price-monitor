from visual_scraper import scrape_olx_with_selenium

def main():
    query = input("Digite o termo de busca (ex: iphone): ")
    if not query:
        query = "iphone"
    
    print(f"Searching for: {query}")
    results = scrape_olx_with_selenium(query, headless=False)
    
    print(f"Found {len(results)} products:")
    
    # O navegador permanecerá aberto para visualização
    if results:
        input("Pressione Enter para fechar o navegador...")

if __name__ == "__main__":
    main()
