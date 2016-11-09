from bs4 import BeautifulSoup
import json

with open('zhenyuguo.html','r') as HTMLfile: 
    html_doc = HTMLfile.read()

    info_list = ["associated-people","published-in","venue","publish-date"]
    link_list = ["publication-link","download-link"]
    data_tree=[]

    soup = BeautifulSoup(html_doc,"lxml")



    for paper in soup.find_all('article','user-publication'):

        paper_node = {}
        paper_node['title'] = paper.find('a').string.replace('\t','').replace('\n','')
        paper_node['link'] = paper.find('a').get('href')
        
        for info in info_list:
            try:
                info_str = paper.find('span',info).string.replace('\t','').replace('\n','').replace('\\u','')
                if len(info_str)>2:
                    if info_str[-2:]==', ':
                        info_str = info_str[:-2]

                paper_node[info] = info_str
            except AttributeError:
                pass

        for link in link_list:
            try:
                paper_node[link] = paper.find('span',link).find('a').get('href')
            except AttributeError:
                pass

        data_tree.append(paper_node)

    with open('zhenyuguo.json','w') as JSONfile:
        print json.dumps(data_tree, indent=4, sort_keys=True)
        json.dump(data_tree,JSONfile, indent=4, sort_keys=True)
