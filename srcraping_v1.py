from bs4 import BeautifulSoup
import requests
import csv

# variavel que irá armezanar todo conteudo retirado das postagens
resultado = []

# os links de pesquisa do stackoverflow são compostos pela raiz https://stackoverflow.com/questions/tagged/ + o termo pesquisado
source = requests.get('https://stackoverflow.com/questions/tagged/python').text
soup = BeautifulSoup(source, 'lxml')

# variavel que irá receber os links das páginas
links = []

# o link da página 2 é retirado do código da primeira página
pagina2 = soup.find('div', class_='s-pagination pager fl').a['href']

paginas = ['https://stackoverflow.com/questions/tagged/python', 'https://stackoverflow.com'+pagina2]

# em cada página é retirado os links dos posts
for pagina in paginas:
    source = requests.get(pagina).text
    soup = BeautifulSoup(source, 'lxml')
    for n in soup.find_all('div', class_='question-summary'):
        link = n.h3.a['href']
        links.append(link)

# cada post então é acessado individualmente para leitura das informações
for link in links:

    # variavéis que irão receber os dados do post e ser adicionados ao resultado final
    respostas = []
    resposta = []
    pergunta = []


    source = requests.get('https://stackoverflow.com'+link).text
    soup = BeautifulSoup(source, 'lxml')
    pergunta.append(soup.find('div', id='question-header').h1.text)
    pergunta.append(soup.find('div', class_='post-text').text)
    # em algumas postagens essa pesquisa estava retornando nulo, por isso o tratamento da exceção
    try:
        pergunta.append(soup.find('div', itemprop='author').a.text)
    except Exception as e:
        pass
    pergunta.append(soup.find('div', class_='post-signature owner grid--cell').span.text)
    pergunta.append(soup.find('div', class_='post-taglist grid gs4 gsy fd-column').text)

    comentarios = []

    div_comentarios = soup.find('div', class_='comments js-comments-container bt bc-black-2 mt12')

    # como nem sempre os comentários estão presentes a pesquisa pode retornar nulo, por isso o tratamento da exceção
    try:
        for comentario in div_comentarios.find_all('div', class_='comment-body js-comment-edit-hide'):
            comentarios.append(comentario.find('span', class_='comment-copy').text)
            comentarios.append(comentario.find('a', class_='comment-user').text)
            comentarios.append(comentario.find('span', class_='comment-date').text)
    except Exception as e:
        comentarios.append('None')

    pergunta.append(comentarios)

    resultado.append(pergunta)

    div_respostas = soup.find('div', id='answers')
    
    # dentro da postagem da pergunta é feita um interação para a retirada de informação de cada resposta
    for post in div_respostas.find_all('div', class_='answer'):
        resposta.append(post.find('div', class_='post-text').text)
        resposta.append(post.find('div', class_='user-action-time').span.text)
        try:
            resposta.append(post.find('div', itemprop="author").a.text)
        except Exception as e:
            pass

        div_comentarios = post.find('div', class_='comments js-comments-container bt bc-black-2 mt12')

        comentarios = []

        # como nem sempre os comentários estão presentes a pesquisa pode retornar nulo, por isso o tratamento da exceção
        try:
            for comentario in div_comentarios.find_all('div', class_='comment-body js-comment-edit-hide'):
                comentarios.append(comentario.find('span', class_='comment-copy').text)
                comentarios.append(comentario.find('a', class_='comment-user').text)
                comentarios.append(comentario.find('span', class_='comment-date').text)
        except Exception as e:
            comentarios.append('None')

        resposta.append(comentarios)
        respostas.append(resposta)
        resultado.append(pergunta)
        resultado.append(resposta)

# O resultado é salvo em um arquivo CSV, porém a formatação não esta organizada. O ideal seria salvar essa informação em JSON já que pretende-se disponibiliza-la
# via API. Devido a falta de tempo e experiência em escrita com JSON estou enviando neste formato. Pretendo atualizar essa parte para integrar com a aplicação web.

file = open('resultado.csv', 'w+', newline ='', encoding='utf-8') 
  
with file:     
    write = csv.writer(file) 
    write.writerows(resultado) 
