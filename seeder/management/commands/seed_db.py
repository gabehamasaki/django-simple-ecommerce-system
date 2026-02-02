import random
from django.core.management.base import BaseCommand
from django.db import transaction
from customers.models import Customer, Address
from inventory.models import Product, Category


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais de teste para e-commerce de tecnologia'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o seeding do banco de dados...")

        try:
            with transaction.atomic():
                # ==========================================
                # 1. CRIAR CATEGORIAS PRINCIPAIS
                # ==========================================
                self.stdout.write("\n📁 Criando categorias principais...")

                main_categories_data = [
                    {"name": "Hardware", "description": "Componentes internos para computadores"},
                    {"name": "Periféricos", "description": "Dispositivos externos e acessórios"},
                    {"name": "Computadores", "description": "PCs completos e notebooks"},
                    {"name": "Redes e Conectividade", "description": "Equipamentos de rede e conexão"},
                    {"name": "Acessórios", "description": "Cabos, adaptadores e outros acessórios"},
                ]

                main_categories = {}
                for cat_data in main_categories_data:
                    category, _ = Category.objects.get_or_create(
                        name=cat_data["name"],
                        defaults={"description": cat_data["description"], "parent": None}
                    )
                    main_categories[cat_data["name"]] = category
                    self.stdout.write(f"  ✓ {cat_data['name']}")

                # ==========================================
                # 2. CRIAR SUBCATEGORIAS
                # ==========================================
                self.stdout.write("\n📂 Criando subcategorias...")

                subcategories_data = [
                    # Hardware
                    {"name": "Processadores", "description": "CPUs Intel, AMD e outros processadores", "parent": "Hardware"},
                    {"name": "Placas de Vídeo", "description": "GPUs NVIDIA, AMD e placas gráficas", "parent": "Hardware"},
                    {"name": "Memória RAM", "description": "Módulos de memória DDR4, DDR5", "parent": "Hardware"},
                    {"name": "Armazenamento SSD", "description": "SSDs SATA e NVMe", "parent": "Hardware"},
                    {"name": "Armazenamento HDD", "description": "Discos rígidos mecânicos", "parent": "Hardware"},
                    {"name": "Placas-Mãe Intel", "description": "Motherboards para processadores Intel", "parent": "Hardware"},
                    {"name": "Placas-Mãe AMD", "description": "Motherboards para processadores AMD", "parent": "Hardware"},
                    {"name": "Fontes de Alimentação", "description": "PSUs e fontes modulares", "parent": "Hardware"},
                    {"name": "Gabinetes", "description": "Cases e gabinetes para PC", "parent": "Hardware"},
                    {"name": "Water Coolers", "description": "Refrigeração líquida AIO e custom", "parent": "Hardware"},
                    {"name": "Air Coolers", "description": "Coolers de ar para CPU", "parent": "Hardware"},
                    {"name": "Ventoinhas", "description": "Fans para gabinete e radiadores", "parent": "Hardware"},
                    {"name": "Placas de Captura", "description": "Captura de vídeo para streaming", "parent": "Hardware"},
                    {"name": "Placas de Som", "description": "DACs e placas de áudio dedicadas", "parent": "Hardware"},

                    # Periféricos
                    {"name": "Monitores Gaming", "description": "Monitores de alta taxa de atualização", "parent": "Periféricos"},
                    {"name": "Monitores Profissionais", "description": "Monitores para design e edição", "parent": "Periféricos"},
                    {"name": "Monitores Ultrawide", "description": "Monitores 21:9 e 32:9", "parent": "Periféricos"},
                    {"name": "Teclados Mecânicos", "description": "Teclados com switches mecânicos", "parent": "Periféricos"},
                    {"name": "Teclados Membrana", "description": "Teclados convencionais e slim", "parent": "Periféricos"},
                    {"name": "Mouses Gaming", "description": "Mouses de alta precisão para jogos", "parent": "Periféricos"},
                    {"name": "Mouses Ergonômicos", "description": "Mouses para produtividade", "parent": "Periféricos"},
                    {"name": "Headsets Gaming", "description": "Headsets com microfone para jogos", "parent": "Periféricos"},
                    {"name": "Fones de Ouvido", "description": "Fones audiophile e casual", "parent": "Periféricos"},
                    {"name": "Microfones", "description": "Microfones USB e XLR", "parent": "Periféricos"},
                    {"name": "Webcams", "description": "Câmeras para streaming e videoconferência", "parent": "Periféricos"},
                    {"name": "Mousepads", "description": "Superfícies para mouse", "parent": "Periféricos"},
                    {"name": "Controles", "description": "Gamepads e joysticks", "parent": "Periféricos"},
                    {"name": "Volantes e Pedais", "description": "Equipamentos de simulação", "parent": "Periféricos"},

                    # Computadores
                    {"name": "PCs Gamer High-End", "description": "Computadores topo de linha", "parent": "Computadores"},
                    {"name": "PCs Gamer Intermediário", "description": "Computadores custo-benefício", "parent": "Computadores"},
                    {"name": "PCs Gamer Entry", "description": "Computadores de entrada", "parent": "Computadores"},
                    {"name": "PCs Workstation", "description": "Estações de trabalho profissionais", "parent": "Computadores"},
                    {"name": "Notebooks Gaming", "description": "Laptops para jogos", "parent": "Computadores"},
                    {"name": "Notebooks Profissionais", "description": "Laptops para trabalho", "parent": "Computadores"},
                    {"name": "Mini PCs", "description": "Computadores compactos", "parent": "Computadores"},

                    # Redes e Conectividade
                    {"name": "Roteadores", "description": "Roteadores WiFi e mesh", "parent": "Redes e Conectividade"},
                    {"name": "Switches", "description": "Switches de rede", "parent": "Redes e Conectividade"},
                    {"name": "Placas de Rede", "description": "Adaptadores WiFi e Ethernet", "parent": "Redes e Conectividade"},
                    {"name": "Access Points", "description": "Pontos de acesso wireless", "parent": "Redes e Conectividade"},

                    # Acessórios
                    {"name": "Cabos e Adaptadores", "description": "Cabos HDMI, USB, DisplayPort", "parent": "Acessórios"},
                    {"name": "Suportes e Braços", "description": "Suportes para monitor e headset", "parent": "Acessórios"},
                    {"name": "Iluminação RGB", "description": "Fitas LED e iluminação ambiente", "parent": "Acessórios"},
                    {"name": "Pasta Térmica", "description": "Compostos térmicos e pads", "parent": "Acessórios"},
                    {"name": "Ferramentas", "description": "Kits de ferramentas para PC", "parent": "Acessórios"},
                ]

                categories = {**main_categories}
                for cat_data in subcategories_data:
                    category, _ = Category.objects.get_or_create(
                        name=cat_data["name"],
                        defaults={
                            "description": cat_data["description"],
                            "parent": main_categories[cat_data["parent"]]
                        }
                    )
                    categories[cat_data["name"]] = category
                    self.stdout.write(f"    ✓ {cat_data['parent']} > {cat_data['name']}")

                # ==========================================
                # 3. CRIAR PRODUTOS (70+ produtos)
                # ==========================================
                self.stdout.write("\n📦 Criando produtos...")

                products_data = [
                    # ========== PROCESSADORES ==========
                    {"name": "Intel Core i9-14900K", "description": "Processador Intel de 14ª geração, 24 núcleos (8P+16E), 5.8GHz Turbo, LGA1700", "price": 3499.90, "stock_quantity": 15, "category": "Processadores"},
                    {"name": "Intel Core i9-14900KF", "description": "Versão sem gráficos integrados do i9-14900K, 24 núcleos, 5.8GHz", "price": 3299.90, "stock_quantity": 12, "category": "Processadores"},
                    {"name": "Intel Core i7-14700K", "description": "Processador Intel de 14ª geração, 20 núcleos (8P+12E), 5.6GHz Turbo", "price": 2599.90, "stock_quantity": 25, "category": "Processadores"},
                    {"name": "Intel Core i7-14700KF", "description": "Versão sem iGPU do i7-14700K, excelente para gaming", "price": 2399.90, "stock_quantity": 20, "category": "Processadores"},
                    {"name": "Intel Core i5-14600K", "description": "Processador de 14ª geração, 14 núcleos, 5.3GHz Turbo, ótimo custo-benefício", "price": 1799.90, "stock_quantity": 35, "category": "Processadores"},
                    {"name": "Intel Core i5-14400F", "description": "Processador de entrada, 10 núcleos, sem iGPU, excelente para builds econômicos", "price": 1099.90, "stock_quantity": 50, "category": "Processadores"},
                    {"name": "AMD Ryzen 9 7950X", "description": "Processador AMD Zen 4, 16 núcleos, 32 threads, 5.7GHz Turbo, AM5", "price": 3299.90, "stock_quantity": 12, "category": "Processadores"},
                    {"name": "AMD Ryzen 9 7950X3D", "description": "Versão com 3D V-Cache do 7950X, 128MB de cache, ideal para gaming e produtividade", "price": 4299.90, "stock_quantity": 8, "category": "Processadores"},
                    {"name": "AMD Ryzen 9 7900X", "description": "12 núcleos Zen 4, 5.6GHz Turbo, excelente multitarefa", "price": 2699.90, "stock_quantity": 18, "category": "Processadores"},
                    {"name": "AMD Ryzen 7 7800X3D", "description": "8 núcleos com 3D V-Cache, 96MB de cache, melhor CPU para gaming", "price": 2899.90, "stock_quantity": 22, "category": "Processadores"},
                    {"name": "AMD Ryzen 7 7700X", "description": "8 núcleos Zen 4, 5.4GHz, ótimo para gaming e streaming", "price": 2199.90, "stock_quantity": 28, "category": "Processadores"},
                    {"name": "AMD Ryzen 5 7600X", "description": "6 núcleos Zen 4, 5.3GHz, entrada para AM5", "price": 1499.90, "stock_quantity": 40, "category": "Processadores"},
                    {"name": "AMD Ryzen 5 7600", "description": "6 núcleos Zen 4 de baixo consumo, 65W TDP", "price": 1299.90, "stock_quantity": 45, "category": "Processadores"},

                    # ========== PLACAS DE VÍDEO ==========
                    {"name": "NVIDIA GeForce RTX 4090 24GB", "description": "GPU flagship Ada Lovelace, 24GB GDDR6X, 16384 CUDA cores", "price": 12999.90, "stock_quantity": 5, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4090 Founders Edition", "description": "Versão de referência da RTX 4090, design premium", "price": 13499.90, "stock_quantity": 3, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4080 Super 16GB", "description": "GPU de alto desempenho, 16GB GDDR6X, 10240 CUDA cores", "price": 7999.90, "stock_quantity": 10, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4080 16GB", "description": "Versão original da RTX 4080, excelente 4K gaming", "price": 7499.90, "stock_quantity": 8, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4070 Ti Super 16GB", "description": "GPU com 16GB VRAM, ideal para 1440p e 4K", "price": 5499.90, "stock_quantity": 18, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4070 Ti 12GB", "description": "Excelente para 1440p gaming, ray tracing otimizado", "price": 4999.90, "stock_quantity": 15, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4070 Super 12GB", "description": "Melhor custo-benefício para 1440p", "price": 3999.90, "stock_quantity": 25, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4070 12GB", "description": "GPU eficiente para gaming em 1440p", "price": 3499.90, "stock_quantity": 30, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4060 Ti 16GB", "description": "Versão com 16GB para jogos exigentes em VRAM", "price": 2999.90, "stock_quantity": 20, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4060 Ti 8GB", "description": "GPU mainstream, excelente 1080p gaming", "price": 2499.90, "stock_quantity": 35, "category": "Placas de Vídeo"},
                    {"name": "NVIDIA GeForce RTX 4060 8GB", "description": "Entrada na série 40, DLSS 3 e ray tracing", "price": 1999.90, "stock_quantity": 45, "category": "Placas de Vídeo"},
                    {"name": "AMD Radeon RX 7900 XTX 24GB", "description": "GPU AMD flagship RDNA 3, 24GB GDDR6, 96 CUs", "price": 6999.90, "stock_quantity": 8, "category": "Placas de Vídeo"},
                    {"name": "AMD Radeon RX 7900 XT 20GB", "description": "Alto desempenho RDNA 3, 20GB VRAM", "price": 5499.90, "stock_quantity": 12, "category": "Placas de Vídeo"},
                    {"name": "AMD Radeon RX 7800 XT 16GB", "description": "Excelente para 1440p, 16GB VRAM", "price": 3299.90, "stock_quantity": 22, "category": "Placas de Vídeo"},
                    {"name": "AMD Radeon RX 7700 XT 12GB", "description": "GPU intermediária RDNA 3, ótimo custo-benefício", "price": 2699.90, "stock_quantity": 28, "category": "Placas de Vídeo"},
                    {"name": "AMD Radeon RX 7600 8GB", "description": "Entrada RDNA 3, ideal para 1080p gaming", "price": 1799.90, "stock_quantity": 40, "category": "Placas de Vídeo"},

                    # ========== MEMÓRIA RAM ==========
                    {"name": "Corsair Vengeance DDR5 32GB (2x16GB) 6000MHz", "description": "Kit DDR5 de alta performance, Intel XMP 3.0", "price": 899.90, "stock_quantity": 45, "category": "Memória RAM"},
                    {"name": "Corsair Vengeance DDR5 64GB (2x32GB) 5600MHz", "description": "Kit DDR5 para workstations e gaming extremo", "price": 1599.90, "stock_quantity": 20, "category": "Memória RAM"},
                    {"name": "G.Skill Trident Z5 RGB DDR5 32GB (2x16GB) 6400MHz", "description": "Memória premium com RGB customizável, CL32", "price": 1099.90, "stock_quantity": 30, "category": "Memória RAM"},
                    {"name": "G.Skill Trident Z5 RGB DDR5 64GB (2x32GB) 6400MHz", "description": "Kit 64GB para entusiastas, iluminação RGB", "price": 1999.90, "stock_quantity": 15, "category": "Memória RAM"},
                    {"name": "Kingston Fury Beast DDR5 32GB (2x16GB) 5200MHz", "description": "DDR5 confiável, perfil EXPO/XMP", "price": 749.90, "stock_quantity": 50, "category": "Memória RAM"},
                    {"name": "Kingston Fury Beast DDR4 32GB (2x16GB) 3200MHz", "description": "Kit DDR4 para builds intermediários, CL16", "price": 549.90, "stock_quantity": 60, "category": "Memória RAM"},
                    {"name": "Kingston Fury Beast DDR4 16GB (2x8GB) 3200MHz", "description": "Kit entrada DDR4, ideal para orçamento limitado", "price": 299.90, "stock_quantity": 80, "category": "Memória RAM"},
                    {"name": "Teamgroup T-Force Delta RGB DDR5 32GB (2x16GB) 6000MHz", "description": "DDR5 com RGB difuso, visual único", "price": 849.90, "stock_quantity": 35, "category": "Memória RAM"},
                    {"name": "Crucial DDR5 32GB (2x16GB) 4800MHz", "description": "DDR5 básico, excelente estabilidade", "price": 649.90, "stock_quantity": 55, "category": "Memória RAM"},

                    # ========== ARMAZENAMENTO SSD ==========
                    {"name": "Samsung 990 Pro 2TB NVMe", "description": "SSD NVMe Gen4 flagship, 7450MB/s leitura, 6900MB/s escrita", "price": 1299.90, "stock_quantity": 35, "category": "Armazenamento SSD"},
                    {"name": "Samsung 990 Pro 1TB NVMe", "description": "SSD NVMe Gen4, velocidade máxima", "price": 749.90, "stock_quantity": 50, "category": "Armazenamento SSD"},
                    {"name": "Samsung 990 Pro 4TB NVMe", "description": "Alta capacidade e velocidade extrema", "price": 2499.90, "stock_quantity": 15, "category": "Armazenamento SSD"},
                    {"name": "WD Black SN850X 2TB NVMe", "description": "SSD gaming de alto desempenho, 7300MB/s", "price": 1199.90, "stock_quantity": 40, "category": "Armazenamento SSD"},
                    {"name": "WD Black SN850X 1TB NVMe", "description": "SSD gaming, otimizado para DirectStorage", "price": 699.90, "stock_quantity": 55, "category": "Armazenamento SSD"},
                    {"name": "Crucial T700 2TB NVMe Gen5", "description": "SSD Gen5, até 12400MB/s, mais rápido do mercado", "price": 1899.90, "stock_quantity": 12, "category": "Armazenamento SSD"},
                    {"name": "Crucial T700 1TB NVMe Gen5", "description": "Velocidade Gen5 em capacidade menor", "price": 999.90, "stock_quantity": 20, "category": "Armazenamento SSD"},
                    {"name": "Kingston KC3000 2TB NVMe", "description": "SSD entusiasta, 7000MB/s, ótimo preço", "price": 999.90, "stock_quantity": 45, "category": "Armazenamento SSD"},
                    {"name": "Samsung 870 EVO 2TB SATA", "description": "SSD SATA confiável, ideal para storage", "price": 699.90, "stock_quantity": 40, "category": "Armazenamento SSD"},
                    {"name": "Samsung 870 EVO 1TB SATA", "description": "SSD SATA mainstream, 560MB/s", "price": 399.90, "stock_quantity": 65, "category": "Armazenamento SSD"},

                    # ========== ARMAZENAMENTO HDD ==========
                    {"name": "Seagate Barracuda 4TB HDD", "description": "HD de alta capacidade, 5400RPM, 256MB cache", "price": 499.90, "stock_quantity": 50, "category": "Armazenamento HDD"},
                    {"name": "Seagate Barracuda 2TB HDD", "description": "HD custo-benefício para armazenamento", "price": 349.90, "stock_quantity": 70, "category": "Armazenamento HDD"},
                    {"name": "WD Blue 4TB HDD", "description": "HD confiável para desktop, 5400RPM", "price": 549.90, "stock_quantity": 45, "category": "Armazenamento HDD"},
                    {"name": "WD Red Plus 8TB NAS", "description": "HD para NAS, otimizado para 24/7", "price": 999.90, "stock_quantity": 25, "category": "Armazenamento HDD"},
                    {"name": "Seagate IronWolf 8TB NAS", "description": "HD enterprise para sistemas NAS", "price": 1099.90, "stock_quantity": 20, "category": "Armazenamento HDD"},

                    # ========== PLACAS-MÃE INTEL ==========
                    {"name": "ASUS ROG Maximus Z790 Hero", "description": "Motherboard premium LGA1700, DDR5, WiFi 6E, 2x Thunderbolt 4", "price": 3999.90, "stock_quantity": 8, "category": "Placas-Mãe Intel"},
                    {"name": "ASUS ROG Strix Z790-E Gaming WiFi", "description": "Placa-mãe gaming, DDR5, 4x M.2, WiFi 6E", "price": 2999.90, "stock_quantity": 12, "category": "Placas-Mãe Intel"},
                    {"name": "MSI MEG Z790 ACE", "description": "Motherboard entusiasta, 24+1+2 fases, DDR5", "price": 3499.90, "stock_quantity": 6, "category": "Placas-Mãe Intel"},
                    {"name": "MSI MAG Z790 Tomahawk WiFi", "description": "Placa-mãe versátil, ótimo VRM, DDR5", "price": 1999.90, "stock_quantity": 20, "category": "Placas-Mãe Intel"},
                    {"name": "Gigabyte Z790 Aorus Master", "description": "Motherboard premium, 20+1+2 fases, Thunderbolt", "price": 2799.90, "stock_quantity": 10, "category": "Placas-Mãe Intel"},
                    {"name": "Gigabyte B760 Aorus Elite AX", "description": "Motherboard custo-benefício, DDR5, WiFi 6E", "price": 1199.90, "stock_quantity": 30, "category": "Placas-Mãe Intel"},
                    {"name": "ASUS Prime B760M-A WiFi", "description": "Placa-mãe mATX, DDR5, ideal para builds compactos", "price": 899.90, "stock_quantity": 40, "category": "Placas-Mãe Intel"},
                    {"name": "ASRock B760M Pro RS/D4", "description": "Motherboard DDR4, opção econômica LGA1700", "price": 699.90, "stock_quantity": 50, "category": "Placas-Mãe Intel"},

                    # ========== PLACAS-MÃE AMD ==========
                    {"name": "ASUS ROG Crosshair X670E Hero", "description": "Motherboard flagship AM5, DDR5-6400+, WiFi 6E", "price": 4299.90, "stock_quantity": 6, "category": "Placas-Mãe AMD"},
                    {"name": "ASUS ROG Strix X670E-E Gaming WiFi", "description": "Placa-mãe gaming AM5, excelente VRM", "price": 2999.90, "stock_quantity": 10, "category": "Placas-Mãe AMD"},
                    {"name": "MSI MEG X670E ACE", "description": "Motherboard entusiasta AM5, 22+2+1 fases", "price": 3799.90, "stock_quantity": 5, "category": "Placas-Mãe AMD"},
                    {"name": "MSI MAG B650 Tomahawk WiFi", "description": "Placa-mãe AM5 custo-benefício, DDR5, WiFi 6E", "price": 1499.90, "stock_quantity": 22, "category": "Placas-Mãe AMD"},
                    {"name": "Gigabyte X670E Aorus Master", "description": "Motherboard premium AM5, PCIe 5.0 completo", "price": 3299.90, "stock_quantity": 8, "category": "Placas-Mãe AMD"},
                    {"name": "Gigabyte B650 Aorus Elite AX", "description": "Placa AM5 versátil, DDR5, WiFi 6E", "price": 1299.90, "stock_quantity": 28, "category": "Placas-Mãe AMD"},
                    {"name": "ASRock B650M PG Riptide WiFi", "description": "Motherboard mATX AM5, compacta e eficiente", "price": 999.90, "stock_quantity": 35, "category": "Placas-Mãe AMD"},
                    {"name": "ASUS TUF Gaming A620M-Plus", "description": "Entrada AM5, DDR5, ideal para Ryzen 7000", "price": 799.90, "stock_quantity": 45, "category": "Placas-Mãe AMD"},

                    # ========== FONTES DE ALIMENTAÇÃO ==========
                    {"name": "Corsair RM1000x 1000W 80+ Gold", "description": "Fonte modular de alta eficiência, cabos flat", "price": 1099.90, "stock_quantity": 25, "category": "Fontes de Alimentação"},
                    {"name": "Corsair RM850x 850W 80+ Gold", "description": "Fonte modular, ventilador Zero RPM", "price": 799.90, "stock_quantity": 35, "category": "Fontes de Alimentação"},
                    {"name": "Corsair HX1500i 1500W 80+ Platinum", "description": "Fonte premium para builds extremos, iCUE", "price": 1999.90, "stock_quantity": 10, "category": "Fontes de Alimentação"},
                    {"name": "EVGA SuperNOVA 1000 G7 1000W 80+ Gold", "description": "Fonte confiável, garantia 10 anos", "price": 999.90, "stock_quantity": 30, "category": "Fontes de Alimentação"},
                    {"name": "EVGA SuperNOVA 850 G7 850W 80+ Gold", "description": "Ótimo custo-benefício, full modular", "price": 699.90, "stock_quantity": 40, "category": "Fontes de Alimentação"},
                    {"name": "Seasonic Focus GX-1000 1000W 80+ Gold", "description": "Fonte japonesa, componentes premium", "price": 1199.90, "stock_quantity": 20, "category": "Fontes de Alimentação"},
                    {"name": "Seasonic Prime TX-1000 1000W 80+ Titanium", "description": "Eficiência máxima, componentes topo de linha", "price": 1799.90, "stock_quantity": 8, "category": "Fontes de Alimentação"},
                    {"name": "be quiet! Straight Power 12 850W", "description": "Fonte silenciosa, 80+ Platinum", "price": 899.90, "stock_quantity": 25, "category": "Fontes de Alimentação"},
                    {"name": "Cooler Master V850 SFX Gold", "description": "Fonte SFX para builds ITX, full modular", "price": 849.90, "stock_quantity": 18, "category": "Fontes de Alimentação"},

                    # ========== GABINETES ==========
                    {"name": "NZXT H7 Flow", "description": "Mid-tower com excelente airflow, painel mesh", "price": 899.90, "stock_quantity": 20, "category": "Gabinetes"},
                    {"name": "NZXT H9 Elite", "description": "Full-tower premium, vidro temperado dual", "price": 1499.90, "stock_quantity": 12, "category": "Gabinetes"},
                    {"name": "Lian Li O11 Dynamic EVO", "description": "Case modular para custom loops, dual chamber", "price": 1199.90, "stock_quantity": 15, "category": "Gabinetes"},
                    {"name": "Lian Li Lancool III", "description": "Mid-tower versátil, excelente gestão de cabos", "price": 999.90, "stock_quantity": 22, "category": "Gabinetes"},
                    {"name": "Corsair 5000D Airflow", "description": "Case espaçoso, suporte para radiadores grandes", "price": 1099.90, "stock_quantity": 18, "category": "Gabinetes"},
                    {"name": "Corsair 4000D Airflow", "description": "Mid-tower compacto, ótimo airflow", "price": 699.90, "stock_quantity": 30, "category": "Gabinetes"},
                    {"name": "Fractal Design Torrent", "description": "Airflow extremo, fans 180mm inclusos", "price": 1299.90, "stock_quantity": 14, "category": "Gabinetes"},
                    {"name": "Fractal Design North", "description": "Design minimalista com frente em madeira", "price": 899.90, "stock_quantity": 20, "category": "Gabinetes"},
                    {"name": "Phanteks Eclipse G360A", "description": "Case compacto, mesh frontal, ótimo preço", "price": 599.90, "stock_quantity": 35, "category": "Gabinetes"},
                    {"name": "be quiet! Dark Base Pro 901", "description": "Full-tower silencioso, modular", "price": 1799.90, "stock_quantity": 8, "category": "Gabinetes"},

                    # ========== WATER COOLERS ==========
                    {"name": "NZXT Kraken X73 RGB 360mm", "description": "AIO 360mm, display LCD, iluminação RGB", "price": 1299.90, "stock_quantity": 18, "category": "Water Coolers"},
                    {"name": "NZXT Kraken Z73 RGB 360mm", "description": "AIO premium com display LCD customizável", "price": 1699.90, "stock_quantity": 12, "category": "Water Coolers"},
                    {"name": "Corsair iCUE H150i Elite LCD XT 360mm", "description": "AIO com tela IPS, integração iCUE", "price": 1599.90, "stock_quantity": 15, "category": "Water Coolers"},
                    {"name": "Corsair iCUE H100i Elite 240mm", "description": "AIO compacto, excelente performance", "price": 999.90, "stock_quantity": 25, "category": "Water Coolers"},
                    {"name": "ASUS ROG Ryujin III 360 ARGB", "description": "AIO com display OLED, bomba Asetek", "price": 1899.90, "stock_quantity": 8, "category": "Water Coolers"},
                    {"name": "Arctic Liquid Freezer II 360", "description": "AIO custo-benefício, excelente performance térmica", "price": 799.90, "stock_quantity": 30, "category": "Water Coolers"},
                    {"name": "Arctic Liquid Freezer II 280", "description": "AIO 280mm, silencioso e eficiente", "price": 649.90, "stock_quantity": 35, "category": "Water Coolers"},
                    {"name": "EK-AIO 360 D-RGB", "description": "AIO da EK, qualidade de custom loop", "price": 1099.90, "stock_quantity": 20, "category": "Water Coolers"},

                    # ========== AIR COOLERS ==========
                    {"name": "Noctua NH-D15 chromax.black", "description": "Air cooler dual-tower topo de linha, silencioso", "price": 699.90, "stock_quantity": 25, "category": "Air Coolers"},
                    {"name": "Noctua NH-D15S", "description": "Versão single-fan do NH-D15, compatibilidade RAM", "price": 599.90, "stock_quantity": 30, "category": "Air Coolers"},
                    {"name": "Noctua NH-U12A", "description": "Cooler compacto de alta performance", "price": 499.90, "stock_quantity": 35, "category": "Air Coolers"},
                    {"name": "be quiet! Dark Rock Pro 5", "description": "Air cooler silencioso, 270W TDP", "price": 549.90, "stock_quantity": 28, "category": "Air Coolers"},
                    {"name": "be quiet! Dark Rock 4", "description": "Cooler single-tower, excelente silêncio", "price": 399.90, "stock_quantity": 40, "category": "Air Coolers"},
                    {"name": "Thermalright Peerless Assassin 120 SE", "description": "Dual-tower custo-benefício incrível", "price": 249.90, "stock_quantity": 50, "category": "Air Coolers"},
                    {"name": "DeepCool AK620", "description": "Dual-tower com ótima relação preço/performance", "price": 299.90, "stock_quantity": 45, "category": "Air Coolers"},
                    {"name": "Cooler Master Hyper 212 Black Edition", "description": "Cooler clássico, entrada confiável", "price": 199.90, "stock_quantity": 60, "category": "Air Coolers"},

                    # ========== VENTOINHAS ==========
                    {"name": "Noctua NF-A12x25 PWM", "description": "Ventoinha premium 120mm, melhor estática", "price": 189.90, "stock_quantity": 50, "category": "Ventoinhas"},
                    {"name": "Noctua NF-A14 PWM chromax.black", "description": "Fan 140mm, silencioso e potente", "price": 169.90, "stock_quantity": 45, "category": "Ventoinhas"},
                    {"name": "Corsair iCUE ML120 RGB Elite (3-pack)", "description": "Kit 3 fans RGB, levitação magnética", "price": 399.90, "stock_quantity": 30, "category": "Ventoinhas"},
                    {"name": "Lian Li UNI FAN SL-Infinity 120 (3-pack)", "description": "Fans infinity mirror, conexão daisy-chain", "price": 499.90, "stock_quantity": 25, "category": "Ventoinhas"},
                    {"name": "Arctic P12 PWM PST (5-pack)", "description": "Kit econômico de fans, conexão PST", "price": 149.90, "stock_quantity": 70, "category": "Ventoinhas"},
                    {"name": "be quiet! Light Wings 120mm (3-pack)", "description": "Fans ARGB silenciosos", "price": 349.90, "stock_quantity": 35, "category": "Ventoinhas"},

                    # ========== MONITORES GAMING ==========
                    {"name": "Samsung Odyssey Neo G8 32\" 4K 240Hz", "description": "Monitor Mini LED, HDR2000, curvo 1000R", "price": 6999.90, "stock_quantity": 6, "category": "Monitores Gaming"},
                    {"name": "LG UltraGear 27GP950 27\" 4K 144Hz", "description": "Monitor 4K Nano IPS, HDMI 2.1, G-Sync", "price": 3499.90, "stock_quantity": 12, "category": "Monitores Gaming"},
                    {"name": "ASUS ROG Swift PG279QM 27\" 1440p 240Hz", "description": "Monitor IPS 1440p, G-Sync, Reflex Analyzer", "price": 2999.90, "stock_quantity": 15, "category": "Monitores Gaming"},
                    {"name": "ASUS ROG Swift PG27AQN 27\" 1440p 360Hz", "description": "Monitor mais rápido do mundo, esports", "price": 4999.90, "stock_quantity": 8, "category": "Monitores Gaming"},
                    {"name": "BenQ ZOWIE XL2566K 24.5\" 360Hz", "description": "Monitor esports profissional, DyAc+", "price": 3799.90, "stock_quantity": 10, "category": "Monitores Gaming"},
                    {"name": "Alienware AW2723DF 27\" 1440p 280Hz", "description": "Monitor QD-OLED gaming, cores vibrantes", "price": 3999.90, "stock_quantity": 12, "category": "Monitores Gaming"},
                    {"name": "Acer Predator XB273U 27\" 1440p 170Hz", "description": "Monitor IPS gaming, ótimo custo-benefício", "price": 1999.90, "stock_quantity": 20, "category": "Monitores Gaming"},

                    # ========== MONITORES ULTRAWIDE ==========
                    {"name": "Samsung Odyssey G9 49\" 240Hz DQHD", "description": "Monitor ultrawide curvo 32:9, 1000R", "price": 7999.90, "stock_quantity": 6, "category": "Monitores Ultrawide"},
                    {"name": "Samsung Odyssey OLED G9 49\" 240Hz", "description": "Primeiro ultrawide OLED, cores perfeitas", "price": 9999.90, "stock_quantity": 4, "category": "Monitores Ultrawide"},
                    {"name": "LG UltraGear 45GR95QE 45\" OLED 240Hz", "description": "Ultrawide OLED curvo, 21:9", "price": 8999.90, "stock_quantity": 5, "category": "Monitores Ultrawide"},
                    {"name": "Alienware AW3423DWF 34\" QD-OLED 165Hz", "description": "Ultrawide QD-OLED, HDR True Black", "price": 5999.90, "stock_quantity": 10, "category": "Monitores Ultrawide"},
                    {"name": "LG 34WP85C-B 34\" 1440p USB-C", "description": "Ultrawide produtividade, 90W USB-C", "price": 2999.90, "stock_quantity": 15, "category": "Monitores Ultrawide"},

                    # ========== TECLADOS MECÂNICOS ==========
                    {"name": "Logitech G Pro X TKL Lightspeed", "description": "Teclado wireless pro, switches hot-swap", "price": 999.90, "stock_quantity": 30, "category": "Teclados Mecânicos"},
                    {"name": "Razer Huntsman V3 Pro", "description": "Teclado com switches ópticos analógicos", "price": 1499.90, "stock_quantity": 20, "category": "Teclados Mecânicos"},
                    {"name": "Razer Huntsman V3 Pro TKL", "description": "Versão TKL, switches analógicos", "price": 1299.90, "stock_quantity": 25, "category": "Teclados Mecânicos"},
                    {"name": "Wooting 60HE", "description": "Teclado 60% com Hall Effect, Rapid Trigger", "price": 1199.90, "stock_quantity": 15, "category": "Teclados Mecânicos"},
                    {"name": "SteelSeries Apex Pro TKL", "description": "Switches OmniPoint ajustáveis", "price": 1099.90, "stock_quantity": 22, "category": "Teclados Mecânicos"},
                    {"name": "Ducky One 3 TKL", "description": "Teclado premium, hot-swap, PBT keycaps", "price": 899.90, "stock_quantity": 28, "category": "Teclados Mecânicos"},
                    {"name": "Keychron Q1 Pro", "description": "Teclado custom 75%, QMK/VIA", "price": 999.90, "stock_quantity": 25, "category": "Teclados Mecânicos"},
                    {"name": "Corsair K70 RGB Pro", "description": "Teclado full-size, switches Cherry MX", "price": 899.90, "stock_quantity": 30, "category": "Teclados Mecânicos"},
                    {"name": "HyperX Alloy Origins 60", "description": "Teclado 60% compacto, switches HyperX", "price": 499.90, "stock_quantity": 40, "category": "Teclados Mecânicos"},

                    # ========== MOUSES GAMING ==========
                    {"name": "Logitech G Pro X Superlight 2", "description": "Mouse wireless 60g, sensor HERO 2", "price": 899.90, "stock_quantity": 35, "category": "Mouses Gaming"},
                    {"name": "Logitech G502 X Plus", "description": "Mouse wireless ergonômico, LIGHTFORCE", "price": 799.90, "stock_quantity": 30, "category": "Mouses Gaming"},
                    {"name": "Razer DeathAdder V3 Pro", "description": "Mouse ergonômico wireless, Focus Pro 30K", "price": 799.90, "stock_quantity": 40, "category": "Mouses Gaming"},
                    {"name": "Razer Viper V3 Pro", "description": "Mouse ultraleve 54g, sensor 35K", "price": 899.90, "stock_quantity": 25, "category": "Mouses Gaming"},
                    {"name": "Finalmouse UltralightX", "description": "Mouse ultraleve premium, edição limitada", "price": 999.90, "stock_quantity": 10, "category": "Mouses Gaming"},
                    {"name": "Pulsar X2 Wireless", "description": "Mouse simétrico ultraleve, sensor PAW3395", "price": 699.90, "stock_quantity": 30, "category": "Mouses Gaming"},
                    {"name": "Zowie EC2-CW", "description": "Mouse wireless ergonômico, sensor 3395", "price": 649.90, "stock_quantity": 35, "category": "Mouses Gaming"},
                    {"name": "SteelSeries Aerox 5 Wireless", "description": "Mouse leve com botões extras", "price": 599.90, "stock_quantity": 28, "category": "Mouses Gaming"},
                    {"name": "Endgame Gear XM2we", "description": "Mouse wireless 63g, excelente shape", "price": 549.90, "stock_quantity": 32, "category": "Mouses Gaming"},

                    # ========== HEADSETS GAMING ==========
                    {"name": "SteelSeries Arctis Nova Pro Wireless", "description": "Headset premium, ANC, dual wireless", "price": 2199.90, "stock_quantity": 15, "category": "Headsets Gaming"},
                    {"name": "SteelSeries Arctis Nova 7 Wireless", "description": "Headset wireless multi-plataforma", "price": 1099.90, "stock_quantity": 25, "category": "Headsets Gaming"},
                    {"name": "Logitech G Pro X 2 Lightspeed", "description": "Headset pro wireless, drivers 50mm", "price": 1299.90, "stock_quantity": 20, "category": "Headsets Gaming"},
                    {"name": "Razer BlackShark V2 Pro", "description": "Headset esports wireless, THX Spatial", "price": 999.90, "stock_quantity": 30, "category": "Headsets Gaming"},
                    {"name": "HyperX Cloud III Wireless", "description": "Headset confortável, bateria 120h", "price": 899.90, "stock_quantity": 28, "category": "Headsets Gaming"},
                    {"name": "HyperX Cloud Alpha Wireless", "description": "Headset com 300h de bateria", "price": 999.90, "stock_quantity": 22, "category": "Headsets Gaming"},
                    {"name": "Corsair Virtuoso RGB Wireless XT", "description": "Headset premium, Dolby Atmos", "price": 1499.90, "stock_quantity": 18, "category": "Headsets Gaming"},
                    {"name": "Astro A50 Gen 4", "description": "Headset wireless com base de carga", "price": 1799.90, "stock_quantity": 12, "category": "Headsets Gaming"},

                    # ========== MICROFONES ==========
                    {"name": "Shure SM7B", "description": "Microfone dinâmico profissional, padrão broadcast", "price": 2499.90, "stock_quantity": 15, "category": "Microfones"},
                    {"name": "Elgato Wave:3", "description": "Microfone USB condensador, software Wave Link", "price": 899.90, "stock_quantity": 30, "category": "Microfones"},
                    {"name": "Blue Yeti X", "description": "Microfone USB popular, padrões múltiplos", "price": 799.90, "stock_quantity": 35, "category": "Microfones"},
                    {"name": "Rode NT-USB+", "description": "Microfone USB studio quality", "price": 999.90, "stock_quantity": 25, "category": "Microfones"},
                    {"name": "HyperX QuadCast S", "description": "Microfone USB RGB, anti-vibração", "price": 699.90, "stock_quantity": 40, "category": "Microfones"},
                    {"name": "Audio-Technica AT2020USB-X", "description": "Microfone condensador USB, qualidade AT", "price": 749.90, "stock_quantity": 28, "category": "Microfones"},

                    # ========== WEBCAMS ==========
                    {"name": "Elgato Facecam Pro 4K", "description": "Webcam 4K60, sensor Sony, ajustes manuais", "price": 1799.90, "stock_quantity": 20, "category": "Webcams"},
                    {"name": "Elgato Facecam", "description": "Webcam 1080p60, sensor Sony STARVIS", "price": 999.90, "stock_quantity": 30, "category": "Webcams"},
                    {"name": "Logitech Brio 4K Pro", "description": "Webcam 4K HDR, Windows Hello", "price": 1299.90, "stock_quantity": 25, "category": "Webcams"},
                    {"name": "Logitech C920s HD Pro", "description": "Webcam 1080p clássica, privacy shutter", "price": 449.90, "stock_quantity": 50, "category": "Webcams"},
                    {"name": "Razer Kiyo Pro Ultra", "description": "Webcam 4K com sensor grande", "price": 1499.90, "stock_quantity": 18, "category": "Webcams"},

                    # ========== MOUSEPADS ==========
                    {"name": "Artisan FX Hien XL", "description": "Mousepad japonês premium, superfície híbrida", "price": 399.90, "stock_quantity": 25, "category": "Mousepads"},
                    {"name": "Logitech G840 XL", "description": "Mousepad extended, superfície consistente", "price": 249.90, "stock_quantity": 40, "category": "Mousepads"},
                    {"name": "SteelSeries QcK Heavy XXL", "description": "Mousepad grande, 6mm de espessura", "price": 199.90, "stock_quantity": 50, "category": "Mousepads"},
                    {"name": "Razer Strider XXL", "description": "Mousepad híbrido, textura única", "price": 299.90, "stock_quantity": 35, "category": "Mousepads"},
                    {"name": "Pulsar ParaControl V2 XL", "description": "Mousepad de controle, bordas costuradas", "price": 179.90, "stock_quantity": 45, "category": "Mousepads"},

                    # ========== PCS GAMER HIGH-END ==========
                    {"name": "PC Gamer Ultimate - RTX 4090 + i9-14900K", "description": "i9-14900K, RTX 4090 24GB, 64GB DDR5-6000, 2TB NVMe Gen5, AIO 360mm", "price": 32999.90, "stock_quantity": 3, "category": "PCs Gamer High-End"},
                    {"name": "PC Gamer Extreme - RTX 4090 + R9 7950X3D", "description": "Ryzen 9 7950X3D, RTX 4090, 64GB DDR5, 2TB NVMe, Custom Loop", "price": 35999.90, "stock_quantity": 2, "category": "PCs Gamer High-End"},
                    {"name": "PC Gamer Elite - RTX 4080 Super + i9-14900K", "description": "i9-14900K, RTX 4080 Super, 32GB DDR5-6400, 2TB NVMe", "price": 24999.90, "stock_quantity": 4, "category": "PCs Gamer High-End"},

                    # ========== PCS GAMER INTERMEDIÁRIO ==========
                    {"name": "PC Gamer Pro - RTX 4070 Ti Super + R7 7800X3D", "description": "Ryzen 7 7800X3D, RTX 4070 Ti Super, 32GB DDR5, 1TB NVMe", "price": 15999.90, "stock_quantity": 6, "category": "PCs Gamer Intermediário"},
                    {"name": "PC Gamer Performance - RTX 4070 Super + i7-14700K", "description": "i7-14700K, RTX 4070 Super, 32GB DDR5, 1TB NVMe", "price": 12999.90, "stock_quantity": 8, "category": "PCs Gamer Intermediário"},
                    {"name": "PC Gamer Plus - RTX 4070 + R7 7700X", "description": "Ryzen 7 7700X, RTX 4070, 16GB DDR5, 1TB NVMe", "price": 9999.90, "stock_quantity": 10, "category": "PCs Gamer Intermediário"},

                    # ========== PCS GAMER ENTRY ==========
                    {"name": "PC Gamer Start - RTX 4060 Ti + i5-14400F", "description": "i5-14400F, RTX 4060 Ti, 16GB DDR4, 512GB NVMe", "price": 6499.90, "stock_quantity": 12, "category": "PCs Gamer Entry"},
                    {"name": "PC Gamer Essential - RTX 4060 + R5 7600", "description": "Ryzen 5 7600, RTX 4060, 16GB DDR5, 512GB NVMe", "price": 5499.90, "stock_quantity": 15, "category": "PCs Gamer Entry"},
                    {"name": "PC Gamer Basic - RX 7600 + i5-12400F", "description": "i5-12400F, RX 7600, 16GB DDR4, 480GB SSD", "price": 4299.90, "stock_quantity": 18, "category": "PCs Gamer Entry"},

                    # ========== NOTEBOOKS GAMING ==========
                    {"name": "ASUS ROG Strix G18 RTX 4090", "description": "18\" QHD+ 240Hz, i9-14900HX, RTX 4090, 32GB, 1TB", "price": 24999.90, "stock_quantity": 3, "category": "Notebooks Gaming"},
                    {"name": "ASUS ROG Strix G16 RTX 4070", "description": "16\" FHD+ 165Hz, i9-14900HX, RTX 4070, 16GB, 512GB", "price": 14999.90, "stock_quantity": 6, "category": "Notebooks Gaming"},
                    {"name": "Lenovo Legion Pro 7i RTX 4080", "description": "16\" WQXGA 240Hz, i9-14900HX, RTX 4080, 32GB, 1TB", "price": 19999.90, "stock_quantity": 4, "category": "Notebooks Gaming"},
                    {"name": "Lenovo Legion 5 Pro RTX 4070", "description": "16\" WQXGA 165Hz, R7 7745HX, RTX 4070, 16GB, 512GB", "price": 11999.90, "stock_quantity": 8, "category": "Notebooks Gaming"},
                    {"name": "Dell G16 Gaming RTX 4060", "description": "16\" QHD+ 165Hz, i7-14650HX, RTX 4060, 16GB, 512GB", "price": 8999.90, "stock_quantity": 12, "category": "Notebooks Gaming"},
                    {"name": "Acer Nitro 5 RTX 4050", "description": "15.6\" FHD 144Hz, i5-13500H, RTX 4050, 8GB, 512GB", "price": 5999.90, "stock_quantity": 20, "category": "Notebooks Gaming"},
                    {"name": "MSI Katana 15 RTX 4060", "description": "15.6\" FHD 144Hz, i7-13620H, RTX 4060, 16GB, 512GB", "price": 7499.90, "stock_quantity": 15, "category": "Notebooks Gaming"},

                    # ========== ROTEADORES ==========
                    {"name": "ASUS ROG Rapture GT-AX11000 Pro", "description": "Roteador tri-band WiFi 6E, gaming dedicado", "price": 2999.90, "stock_quantity": 12, "category": "Roteadores"},
                    {"name": "ASUS ZenWiFi Pro ET12 (2-pack)", "description": "Mesh WiFi 6E, cobertura 6000 sq ft", "price": 3499.90, "stock_quantity": 10, "category": "Roteadores"},
                    {"name": "TP-Link Archer AXE300", "description": "Roteador WiFi 6E quad-band", "price": 2499.90, "stock_quantity": 15, "category": "Roteadores"},
                    {"name": "Netgear Nighthawk RAXE500", "description": "WiFi 6E tri-band, 12 streams", "price": 2799.90, "stock_quantity": 10, "category": "Roteadores"},
                    {"name": "TP-Link Deco XE75 (3-pack)", "description": "Mesh WiFi 6E, setup fácil", "price": 1799.90, "stock_quantity": 20, "category": "Roteadores"},

                    # ========== CABOS E ADAPTADORES ==========
                    {"name": "Cabo HDMI 2.1 8K 2m", "description": "HDMI 2.1 certificado, 48Gbps, 8K60Hz/4K120Hz", "price": 149.90, "stock_quantity": 80, "category": "Cabos e Adaptadores"},
                    {"name": "Cabo DisplayPort 2.1 2m", "description": "DP 2.1 UHBR20, 16K suporte", "price": 199.90, "stock_quantity": 60, "category": "Cabos e Adaptadores"},
                    {"name": "Cabo USB-C Thunderbolt 4 1m", "description": "40Gbps, 100W PD, vídeo 8K", "price": 249.90, "stock_quantity": 50, "category": "Cabos e Adaptadores"},
                    {"name": "Hub USB-C 10-em-1", "description": "HDMI 4K, USB-A, SD, Ethernet, 100W PD", "price": 299.90, "stock_quantity": 45, "category": "Cabos e Adaptadores"},
                    {"name": "Adaptador USB-C para DisplayPort 8K", "description": "Conversão DP 1.4, 8K30Hz", "price": 129.90, "stock_quantity": 70, "category": "Cabos e Adaptadores"},

                    # ========== PASTA TÉRMICA ==========
                    {"name": "Thermal Grizzly Kryonaut 1g", "description": "Pasta térmica premium, 12.5W/mK", "price": 79.90, "stock_quantity": 100, "category": "Pasta Térmica"},
                    {"name": "Thermal Grizzly Conductonaut 1g", "description": "Metal líquido, 73W/mK, cuidado extremo", "price": 129.90, "stock_quantity": 60, "category": "Pasta Térmica"},
                    {"name": "Noctua NT-H2 3.5g", "description": "Pasta térmica Noctua, fácil aplicação", "price": 99.90, "stock_quantity": 80, "category": "Pasta Térmica"},
                    {"name": "Arctic MX-6 4g", "description": "Pasta térmica custo-benefício, longa duração", "price": 59.90, "stock_quantity": 120, "category": "Pasta Térmica"},
                    {"name": "Thermal Grizzly Carbonaut (38x38mm)", "description": "Pad térmico de grafeno, reutilizável", "price": 149.90, "stock_quantity": 40, "category": "Pasta Térmica"},
                ]

                for prod_data in products_data:
                    Product.objects.get_or_create(
                        name=prod_data["name"],
                        defaults={
                            "description": prod_data["description"],
                            "price": prod_data["price"],
                            "stock_quantity": prod_data["stock_quantity"],
                            "category": categories[prod_data["category"]]
                        }
                    )
                self.stdout.write(f"  ✓ {len(products_data)} produtos processados")

                # ==========================================
                # 4. CRIAR CLIENTES (15 clientes)
                # ==========================================
                self.stdout.write("\n👤 Criando clientes...")

                customers_data = [
                    {"first_name": "João", "last_name": "Silva", "email": "joao.silva@email.com", "phone_number": "11987654321"},
                    {"first_name": "Maria", "last_name": "Santos", "email": "maria.santos@email.com", "phone_number": "11976543210"},
                    {"first_name": "Pedro", "last_name": "Oliveira", "email": "pedro.oliveira@email.com", "phone_number": "21998765432"},
                    {"first_name": "Ana", "last_name": "Costa", "email": "ana.costa@email.com", "phone_number": "21987654321"},
                    {"first_name": "Lucas", "last_name": "Ferreira", "email": "lucas.ferreira@email.com", "phone_number": "31999887766"},
                    {"first_name": "Juliana", "last_name": "Rodrigues", "email": "juliana.rodrigues@email.com", "phone_number": "31988776655"},
                    {"first_name": "Rafael", "last_name": "Almeida", "email": "rafael.almeida@email.com", "phone_number": "41997766554"},
                    {"first_name": "Camila", "last_name": "Pereira", "email": "camila.pereira@email.com", "phone_number": "41986655443"},
                    {"first_name": "Bruno", "last_name": "Martins", "email": "bruno.martins@email.com", "phone_number": "51995544332"},
                    {"first_name": "Fernanda", "last_name": "Lima", "email": "fernanda.lima@email.com", "phone_number": "51984433221"},
                    {"first_name": "Gabriel", "last_name": "Souza", "email": "gabriel.souza@email.com", "phone_number": "61993322110"},
                    {"first_name": "Larissa", "last_name": "Carvalho", "email": "larissa.carvalho@email.com", "phone_number": "61982211009"},
                    {"first_name": "Thiago", "last_name": "Nascimento", "email": "thiago.nascimento@email.com", "phone_number": "71991100998"},
                    {"first_name": "Beatriz", "last_name": "Moreira", "email": "beatriz.moreira@email.com", "phone_number": "71980099887"},
                    {"first_name": "Diego", "last_name": "Barbosa", "email": "diego.barbosa@email.com", "phone_number": "81979988776"},
                ]

                # ==========================================
                # 5. CRIAR ENDEREÇOS (1-3 por cliente)
                # ==========================================
                addresses_pool = [
                    {"street": "Rua Augusta, 1500", "city": "São Paulo", "state": "SP", "postal_code": "01304-001", "country": "Brasil"},
                    {"street": "Av. Paulista, 2000", "city": "São Paulo", "state": "SP", "postal_code": "01310-100", "country": "Brasil"},
                    {"street": "Rua Oscar Freire, 800", "city": "São Paulo", "state": "SP", "postal_code": "01426-001", "country": "Brasil"},
                    {"street": "Rua Haddock Lobo, 595", "city": "São Paulo", "state": "SP", "postal_code": "01414-001", "country": "Brasil"},
                    {"street": "Av. Atlântica, 1702", "city": "Rio de Janeiro", "state": "RJ", "postal_code": "22021-001", "country": "Brasil"},
                    {"street": "Rua Visconde de Pirajá, 550", "city": "Rio de Janeiro", "state": "RJ", "postal_code": "22410-002", "country": "Brasil"},
                    {"street": "Av. Nossa Senhora de Copacabana, 1200", "city": "Rio de Janeiro", "state": "RJ", "postal_code": "22070-012", "country": "Brasil"},
                    {"street": "Rua Dias Ferreira, 417", "city": "Rio de Janeiro", "state": "RJ", "postal_code": "22431-050", "country": "Brasil"},
                    {"street": "Rua da Bahia, 1234", "city": "Belo Horizonte", "state": "MG", "postal_code": "30160-011", "country": "Brasil"},
                    {"street": "Av. Afonso Pena, 2800", "city": "Belo Horizonte", "state": "MG", "postal_code": "30130-009", "country": "Brasil"},
                    {"street": "Rua Pernambuco, 1000", "city": "Belo Horizonte", "state": "MG", "postal_code": "30130-151", "country": "Brasil"},
                    {"street": "Rua XV de Novembro, 500", "city": "Curitiba", "state": "PR", "postal_code": "80020-310", "country": "Brasil"},
                    {"street": "Av. Batel, 1800", "city": "Curitiba", "state": "PR", "postal_code": "80420-090", "country": "Brasil"},
                    {"street": "Rua Comendador Araújo, 300", "city": "Curitiba", "state": "PR", "postal_code": "80420-000", "country": "Brasil"},
                    {"street": "Rua dos Andradas, 1200", "city": "Porto Alegre", "state": "RS", "postal_code": "90020-015", "country": "Brasil"},
                    {"street": "Av. Ipiranga, 6681", "city": "Porto Alegre", "state": "RS", "postal_code": "90619-900", "country": "Brasil"},
                    {"street": "Rua Padre Chagas, 200", "city": "Porto Alegre", "state": "RS", "postal_code": "90570-080", "country": "Brasil"},
                    {"street": "SQN 308 Bloco A, Apt 102", "city": "Brasília", "state": "DF", "postal_code": "70747-010", "country": "Brasil"},
                    {"street": "SGAS 910 Conjunto B", "city": "Brasília", "state": "DF", "postal_code": "70390-100", "country": "Brasil"},
                    {"street": "CLN 402 Bloco D", "city": "Brasília", "state": "DF", "postal_code": "70847-540", "country": "Brasil"},
                    {"street": "Rua Felipe Schmidt, 450", "city": "Florianópolis", "state": "SC", "postal_code": "88010-001", "country": "Brasil"},
                    {"street": "Av. Beira Mar Norte, 2500", "city": "Florianópolis", "state": "SC", "postal_code": "88015-200", "country": "Brasil"},
                    {"street": "Rua Bocaiúva, 2000", "city": "Florianópolis", "state": "SC", "postal_code": "88015-530", "country": "Brasil"},
                    {"street": "Rua Chile, 300", "city": "Salvador", "state": "BA", "postal_code": "40020-000", "country": "Brasil"},
                    {"street": "Av. Tancredo Neves, 1500", "city": "Salvador", "state": "BA", "postal_code": "41820-020", "country": "Brasil"},
                    {"street": "Rua do Bom Jesus, 200", "city": "Recife", "state": "PE", "postal_code": "50030-170", "country": "Brasil"},
                    {"street": "Av. Boa Viagem, 4000", "city": "Recife", "state": "PE", "postal_code": "51021-000", "country": "Brasil"},
                    {"street": "Rua da Aurora, 900", "city": "Recife", "state": "PE", "postal_code": "50050-000", "country": "Brasil"},
                    {"street": "Av. Desembargador Moreira, 2500", "city": "Fortaleza", "state": "CE", "postal_code": "60170-002", "country": "Brasil"},
                    {"street": "Rua Dragão do Mar, 150", "city": "Fortaleza", "state": "CE", "postal_code": "60060-390", "country": "Brasil"},
                ]

                random.seed(42)  # Para reprodutibilidade

                for customer_data in customers_data:
                    customer, created = Customer.objects.get_or_create(
                        email=customer_data["email"],
                        defaults={
                            "first_name": customer_data["first_name"],
                            "last_name": customer_data["last_name"],
                            "phone_number": customer_data["phone_number"]
                        }
                    )
                    self.stdout.write(f"  ✓ {customer_data['first_name']} {customer_data['last_name']}")

                    # Criar 1 a 3 endereços para cada cliente
                    num_addresses = random.randint(1, 3)
                    selected_addresses = random.sample(addresses_pool, num_addresses)

                    for addr_data in selected_addresses:
                        Address.objects.get_or_create(
                            customer=customer,
                            street=addr_data["street"],
                            defaults={
                                "city": addr_data["city"],
                                "state": addr_data["state"],
                                "postal_code": addr_data["postal_code"],
                                "country": addr_data["country"]
                            }
                        )

                # ==========================================
                # RESUMO
                # ==========================================
                total_subcategories = Category.objects.filter(parent__isnull=False).count()
                total_main_categories = Category.objects.filter(parent__isnull=True).count()

                self.stdout.write("\n" + "=" * 60)
                self.stdout.write(self.style.SUCCESS('🎉 SEEDING CONCLUÍDO COM SUCESSO!'))
                self.stdout.write("=" * 60)
                self.stdout.write(f"  📁 Categorias principais: {total_main_categories}")
                self.stdout.write(f"  📂 Subcategorias: {total_subcategories}")
                self.stdout.write(f"  📦 Produtos criados: {Product.objects.count()}")
                self.stdout.write(f"  👤 Clientes criados: {Customer.objects.count()}")
                self.stdout.write(f"  📍 Endereços criados: {Address.objects.count()}")
                self.stdout.write("=" * 60)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o seeding: {e}'))
