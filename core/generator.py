import jinja2
import black

class CodeGenerator:
    def __init__(self, template_dir="templates"):
        # Şablonların bulunduğu klasörü Jinja'ya tanıtıyoruz
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    def generate_script(self, dataset_config, layer_config):
        # Şablonu yükle
        template = self.env.get_template("pytorch_script.jinja")
        
        # Değişkenleri şablona yerleştir (Render)
        raw_code = template.render(
            dataset=dataset_config,
            transform=dataset_config.transform,
            layer=layer_config
        )
        
        # Black kütüphanesi ile kodu pırıl pırıl formatla
        try:
            formatted_code = black.format_str(raw_code, mode=black.FileMode())
            return formatted_code
        except Exception as e:
            # Eğer Black formatlarken hata verirse (örneğin Jinja'da syntax hatası yaptık), ham kodu döndür
            print(f"Formatlama Hatası: {e}")
            return raw_code