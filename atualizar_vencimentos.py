import os
from datetime import datetime
from supabase import create_client, Client

# Captura as chaves que você configurou nos Secrets do GitHub
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

def executar_automacao():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verificando contas vencidas...")
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("Erro: As variáveis de ambiente SUPABASE_URL ou SUPABASE_ANON_KEY não foram encontradas.")
        return

    # Conecta ao banco do Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    hoje = datetime.now().date().isoformat()
    
    try:
        # Atualiza para 'Atrasado' se o vencimento for menor que hoje e o status for 'Pendente'
        resultado = supabase.table("contas_a_pagar") \
            .update({"status": "Atrasado"}) \
            .lt("data_vencimento", hoje) \
            .eq("status", "Pendente") \
            .execute()
        
        contas_atualizadas = resultado.data
        print(f"Sucesso! {len(contas_atualizadas)} conta(s) modificada(s) para 'Atrasado'.")
            
    except Exception as e:
        print(f"Erro na execução: {str(e)}")

if __name__ == "__main__":
    executar_automacao()
