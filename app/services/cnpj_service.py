import requests
import re

class CNPJService:
    BASE_URL = "https://brasilapi.com.br/api/cnpj/v1/"
    
    @staticmethod
    def limpar_cnpj(cnpj):
        """Remove caracteres especiais do CNPJ"""
        return re.sub(r'[^\d]', '', cnpj)
    
    @staticmethod
    def buscar_dados_cnpj(cnpj):
        """Busca dados do CNPJ na API Brasil API"""
        try:
            cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
            
            if len(cnpj_limpo) != 14:
                return None, "CNPJ deve ter 14 dígitos"
            
            url = f"{CNPJService.BASE_URL}{cnpj_limpo}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 404:
                return None, "CNPJ não encontrado"
            else:
                return None, f"Erro na consulta: {response.status_code}"
                
        except requests.RequestException as e:
            return None, f"Erro de conexão: {str(e)}"
        except Exception as e:
            return None, f"Erro inesperado: {str(e)}"
    
    @staticmethod
    def formatar_cnpj(cnpj):
        """Formata CNPJ com pontos, barras e hífen"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj
