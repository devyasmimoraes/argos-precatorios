from fastapi import FastAPI
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "API online e pronta para os precatórios"}

@app.get("/buscar/{processo}")
async def buscar(processo: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(25000)  # 25s MÁXIMO!
        
        try:
            await page.goto(f"https://cna.oab.org.br/busca/{processo}")
            
            # Nome principal OU vazio
            nome = await page.locator(".nome-advogado, h1, .title").first
            nome_texto = await nome.text_content() or ""
            
            # Se vazio, confirma
            if not nome_texto.strip():
                nome_texto = ""
            
            # OAB OU vazio
            oab = await page.locator(".numero-oab, .oab-number").first
            oab_texto = await oab.text_content() or ""
            
            return {
                "processo": processo,
                "nome": nome_texto.strip(),
                "oab": oab_texto.strip(),
                "status": "sucesso" if nome_texto.strip() else "vazio"
            }
            
        except Exception:
            return {
                "processo": processo,
                "nome": "",
                "oab": "",
                "status": "timeout"
            }
