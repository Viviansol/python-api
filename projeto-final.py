#!/usr/bin/env python
# coding: utf-8

# In[1]:


# projeto final


# In[24]:


import requests as r


# In[25]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[26]:


resp.status_code


# In[27]:


raw_data = resp.json()


# In[28]:


raw_data[0]


# In[29]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'], obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])


# In[30]:


final_data


# In[31]:


final_data.insert(0, ['Confirmados', 'Obitos', 'recuperados', 'Ativos', 'data'])


# In[32]:


final_data


# In[33]:


CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4


# In[34]:


for i in range(1, len(final_data)):
      final_data[i][DATA] = final_data[i][DATA][:10]         


# In[35]:


final_data


# In[36]:


import datetime as dt


# In[37]:


print(dt.time(12, 6, 21, 7), 'Hora:minuto:segundo.microsegundo')
print('----')
print(dt.date(2020, 4, 25), 'Ano-mês-dia')
print('----')
print(dt.datetime(2020, 4, 25, 12, 6, 21, 7), 'Anoe-mês-dia Hora:minuto:segundo.microsegundo')


# In[38]:


natal = dt.date(2020, 12, 25)
reveillon =dt.date(2021, 1, 1)

print(reveillon - natal)
print((reveillon - natal).days)
print((reveillon - natal).seconds)
print((reveillon - natal). microseconds)


# In[39]:


import csv


# In[40]:


with open('brasil-covid.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[41]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d')


# In[42]:


final_data


# In[43]:


def get_datasets(y, labels):
    if type(y[0])== list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]
        


# In[44]:


def set_title(title= ' '):
    if title != ' ':
        display = 'true'
    else:
        display = 'false'
    return{
        'title': title,
        'display': display
    }


# In[70]:


def create_chart(x, y, labels, kind= 'bar', title= ''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
        'type': kind,
        'data':{
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }
    
    return chart


# In[71]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


# In[78]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


# In[79]:


from PIL import Image

from IPython.display import display


# In[80]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[81]:



y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CONFIRMADOS])
    
y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[RECUPERADOS])
    
labels = ['Confirmados', 'Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))
      
chart = create_chart(x, [y_data_1, y_data_2], labels, title='Gráfico Confirmados x Recuperados')
chart_content = get_api_chart(chart)
save_image('meu-primeiro-grafico.png', chart_content)

display_image('meu-primeiro-grafico.png')
    


# In[88]:


from urllib.parse import quote


# In[89]:


def get_api_qrcode(link):
    text = quote(link) # parsing do link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


# In[90]:


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qr-code.png', get_api_qrcode(link))
display_image('qr-code.png')


# In[ ]:




