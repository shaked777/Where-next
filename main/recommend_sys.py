from io import BytesIO
import base64
from sqlalchemy import create_engine
from IPython.display import display
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from matplotlib import use
import matplotlib.pyplot as plt
from django.conf import settings

def main():
  engine = create_engine(settings.DATABASE_URL)




  # The data
  data = pd.read_sql('main_trip', engine)
  print(data.columns)
  data = data.rename(columns={'info': 'description', 'name': 'city', 'id': 'population'})
  X = np.array(data.description)


  # View the data
  data = data[['population','description','city']].astype(str)
  a = data.head()
  # display(a)

  # Translate the data to numbers(vectors) BERT
  text_data = X
  model = SentenceTransformer('distilbert-base-nli-mean-tokens')
  embeddings = model.encode(text_data, show_progress_bar=True)
  embed_data = embeddings

  # PCA
  X = np.array(embed_data)
  n_comp = 5
  pca = PCA(n_components=n_comp)
  pca.fit(X)
  pca_data = pd.DataFrame(pca.transform(X))
  b = pca_data.head()


  # Give reccomendatio by the cosine simalrity of the vectors
  cos_sim_data = pd.DataFrame(cosine_similarity(X))
  def give_recommendations(index,print_recommendation = False,print_recommendation_plots= False):
    
    index_recomm =cos_sim_data.loc[index].sort_values(ascending=False).index.tolist()[1:4]
    movies_recomm =  data['city'].loc[index_recomm].values
    result = {'Countries':movies_recomm,'Index':index_recomm}
    if print_recommendation==True:
      print('The liked country is: %s \n'%(data['city'].loc[index]))
      k=1
      for movie in movies_recomm:
        print('The number %i recommended country is: %s \n'%(k,movie))
        genrs = data.loc[data['city']==str(movie)].index[0]
        print('The popultion of that country is: '+data['population'].loc[genrs])
        k=k+1
        print("----------------------")
    if print_recommendation_plots==True:
      print('The description of the country is this one:\n %s \n'%(data['description'].loc[index]))
      k=1
      for q in range(len(movies_recomm)):
        plot_q = data['description'].loc[index_recomm[q]]
        print('The description of the number %i recommended country is this one:\n %s \n'%(k,plot_q))
        k=k+1
    return result

  # Plot random reccomendation
  plt.style.use('bmh')
  use('Agg')
  plt.figure(figsize=(5,5))

  plt.subplot()
  index = 20
  to_plot_data = cos_sim_data.drop(index,axis=1)
  plt.plot(to_plot_data.loc[index],'.',color='firebrick')
  recomm_index = give_recommendations(index)
  x = recomm_index['Index']
  y = cos_sim_data.loc[index][x].tolist()
  m = recomm_index['Countries']
  plt.plot(x,y,'.',color='navy',label='Recommended trips')
  plt.title('your preference: '+data['city'].loc[index])
  plt.xlabel('Country Index')
  k=0
  for x_i in x:
      plt.annotate('%s'%(m[k]),(x_i,y[k]),fontsize=10)
      k=k+1

  plt.ylabel('Cosine Similarity')
  plt.ylim(0,1)
  plt.show()
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  plt.close()
  buffer.seek(0)
  image_png = buffer.getvalue()
  buffer.close()

  graphic = base64.b64encode(image_png)
  graphic = graphic.decode('utf-8')


  return give_recommendations(20,True), graphic
if __name__ == '__main__':
  main()