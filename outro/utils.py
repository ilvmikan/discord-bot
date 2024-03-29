import random
import requests
import imghdr

def greetings_imgs():
    greetings_imgs = ['https://i.pinimg.com/originals/17/43/59/174359d6c7e31330affd9322a828e20b.gif', 
            'https://i.pinimg.com/originals/1e/f7/cb/1ef7cb22a6c0a543d8e05ef0e254509c.gif', 
            'https://i.pinimg.com/originals/c3/fb/3f/c3fb3ffe25601bf96334eeb573fe94de.gif', 
            'https://i.pinimg.com/originals/cf/89/72/cf897205def7a6bb2ceccfdc32804475.gif', 
            'https://i.pinimg.com/originals/86/d7/5a/86d75a902dda5a4c6ac4b95d8a5afba4.gif' ]    
       
    choice = random.choice(greetings_imgs)
    return choice

def quotes():
    quotes = ['"A Cegueira também é isto, viver num mundo onde se tenha acabado a esperança."\nEnsaio sobre a Cegueira - Saramago',
            '"Que tempos penosos foram aqueles anos. Ter o desejo e necessidade de viver, mas não a habilidade."\nMisto Quente  – Charles Bukowski',
            '"Enquanto eles não se conscientizarem, não serão rebeldes autênticos e, enquanto não se rebelarem, não têm como se conscientizar."\n1984 – George Orwell',
            '"À força de tanto ler e imaginar, fui me distanciando da realidade ao ponto de já não poder distinguir em que dimensão vivo."\nDom Quixote - Cervantes',
            '"Não se preocupe. As melhores pessoas sempre carregam alguma cicatriz."\nA escolha - Kiera Cass']
        
    choice = random.choice(quotes)
    return choice


def is_valid_image(url):
    try:
        response = requests.get(url, stream=True)
        if 'image' not in response.headers['Content-Type']:
            return False
        image_type = imghdr.what(None, response.content)
        return image_type in ['jpeg', 'png']
    except Exception as e:
        print(f"Erro ao verificar a imagem: {e}")
        return False












