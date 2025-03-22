from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from loguru import logger

def setup_driver(headless=False):
    """Setup and return a Chrome WebDriver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    
    # Adicionar opções para evitar detecção como bot
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Instalar e configurar o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Modificar o navigator.webdriver para evitar detecção
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def scrape_olx_with_selenium(query, headless=False):
    """Scrape OLX using Selenium with visible Chrome browser"""
    driver = setup_driver(headless=headless)
    
    try:
        search_url = f"https://www.olx.com.br/brasil?q={query.replace(' ', '+')}"
        logger.info(f"Abrindo URL no Chrome: {search_url}")
        
        # Abrir a URL no navegador
        driver.get(search_url)
        
        # Esperar alguns segundos para carregar completamente
        time.sleep(3)
        
        # Esperar até que a página carregue completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Tentar extrair dados do script JSON
        json_data = None
        try:
            script_element = driver.find_element(By.ID, "__NEXT_DATA__")
            if script_element:
                json_text = script_element.get_attribute("innerHTML")
                json_data = json.loads(json_text)
                
                # Extrair anúncios do JSON
                ads = json_data.get("props", {}).get("pageProps", {}).get("ads", [])
                
                if ads:
                    logger.info(f"Encontrados {len(ads)} anúncios no JSON")
                    
                    # Processar os primeiros 10 anúncios
                    results = []
                    for ad in ads[:10]:
                        title = ad.get("subject", "Título desconhecido")
                        price = ad.get("price", "Preço não informado")
                        url = ad.get("url", "")
                        
                        results.append({
                            "title": title,
                            "price": price,
                            "url": url
                        })
                        
                        print(f"Anúncio: {title} - {price}")
                        print(f"Link: {url}")
                        print("-" * 50)
                    
                    return results
        except Exception as e:
            logger.error(f"Erro ao extrair dados do JSON: {str(e)}")
        
        # Se não conseguiu extrair do JSON, tenta extrair do HTML
        logger.info("Tentando extrair dados do HTML")
        
        # Encontrar os elementos de anúncios
        ad_elements = driver.find_elements(By.CSS_SELECTOR, "li.sc-1fcmfeb-2")
        
        if ad_elements:
            logger.info(f"Encontrados {len(ad_elements)} anúncios no HTML")
            
            results = []
            for i, element in enumerate(ad_elements[:10]):
                try:
                    title_element = element.find_element(By.CSS_SELECTOR, "h2")
                    title = title_element.text.strip() if title_element else "Título desconhecido"
                    
                    price_element = element.find_element(By.CSS_SELECTOR, "span.m7nrfa-0")
                    price = price_element.text.strip() if price_element else "Preço não informado"
                    
                    link_element = element.find_element(By.TAG_NAME, "a")
                    url = link_element.get_attribute("href") if link_element else ""
                    
                    results.append({
                        "title": title,
                        "price": price,
                        "url": url
                    })
                    
                    print(f"Anúncio: {title} - {price}")
                    print(f"Link: {url}")
                    print("-" * 50)
                except Exception as e:
                    logger.error(f"Erro ao processar anúncio {i}: {str(e)}")
            
            return results
        else:
            logger.error("Não foram encontrados anúncios na página")
            return []
        
    except Exception as e:
        logger.error(f"Erro ao fazer scraping com Selenium: {str(e)}")
        return []
    
    finally:
        # O navegador permanecerá aberto para visualização
        # Para fechar automaticamente, descomente a linha abaixo
        # driver.quit()
        pass

if __name__ == "__main__":
    import sys
    
    query = "iphone"
    if len(sys.argv) > 1:
        query = sys.argv[1]
    
    headless = False  # Defina como True para executar em modo headless (sem interface)
    
    print(f"Realizando busca por: {query}")
    results = scrape_olx_with_selenium(query, headless=headless)
    print(f"Encontrados {len(results)} produtos.")
    
    # Mantenha o programa em execução para visualizar o navegador
    if not headless and results:
        input("Pressione Enter para fechar o navegador...")
