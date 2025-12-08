import os
import json
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Indicator, IndicatorRecord

class Command(BaseCommand):
    help = 'Importa dados da pasta data/'

    def handle(self, *args, **kwargs):
        base_path = '/app/data_source' 

        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)
            
            if not os.path.isdir(folder_path): continue
            
            # Pula pasta de mapas ou sem metadata para processar apenas dados relevantes
            meta_path = os.path.join(folder_path, 'metadata.json')
            if not os.path.exists(meta_path):
                self.stdout.write(self.style.WARNING(f"Pulando '{folder_name}': sem metadata."))
                continue

            self.stdout.write(f"Processando: {folder_name}...")

            # 1. LER OS METADADOS COM A ESTRUTURA COMPLEXA
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            
            # Extração segura dos campos aninhados
            ficha = meta.get('ficha', {})
            
            # Nome do indicador
            title = meta.get('nome', folder_name)
            
            # Descrição (Resumo)
            description = ficha.get('resumo', '')
            
            category = "Geral"
            cat_list = ficha.get('categoria', [])
            if cat_list and isinstance(cat_list, list) and len(cat_list) > 0:
                try:                    
                    category = cat_list[0][1] 
                except:
                    pass

            # Cria ou Atualiza o Indicador no Banco
            indicator, created = Indicator.objects.update_or_create(
                uid=folder_name,
                defaults={
                    'title': title,
                    'description': description,
                    'unit': 'Casos',
                    'category': category
                }
            )

            # 2. LER DADOS (CSV)
            csv_path = os.path.join(folder_path, 'raw_data.csv')
            if os.path.exists(csv_path):
                # Se o indicador já existia, limpa os registros antigos para não duplicar
                if not created:
                    indicator.records.all().delete()

                records_buffer = []
                # Lê o CSV com Pandas
                for chunk in pd.read_csv(csv_path, chunksize=5000):
                    for _, row in chunk.iterrows():
                        # Limpeza básica: remove NaNs
                        row_dict = row.dropna().to_dict()
                        
                        records_buffer.append(IndicatorRecord(
                            indicator=indicator,
                            data=row_dict
                        ))
                    
                    IndicatorRecord.objects.bulk_create(records_buffer)
                    records_buffer = []
                    self.stdout.write(f"  + Lote inserido...")
                
                # Grava o resto
                if records_buffer:
                    IndicatorRecord.objects.bulk_create(records_buffer)

        self.stdout.write(self.style.SUCCESS('Importação Concluída com Sucesso!'))