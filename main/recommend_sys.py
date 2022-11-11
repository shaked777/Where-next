from matplotlib import use
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from django.conf import settings

"""

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗███╗   ███╗███████╗███╗   ██╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔════╝████╗  ██║██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔████╔██║██╔████╔██║█████╗  ██╔██╗ ██║██║  ██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║  ██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║ ╚████║██████╔╝██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                        

███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
                                                     

"""                                                                                                                                                                            
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

  # Translate the data to numbers(vectors) BERT
  text_data = X
  model = SentenceTransformer('distilbert-base-nli-mean-tokens')
  embeddings = model.encode(text_data, show_progress_bar=True)
  embed_data = embeddings

  X = np.array(embed_data)

  # Give reccomendation by the cosine simalrity of the vectors
  cos_sim_data = pd.DataFrame(cosine_similarity(X))
  def give_recommendations(index,print_recommendation = False):
    
    index_recomm =cos_sim_data.loc[index].sort_values(ascending=False).index.tolist()[1:4]
    trip_recomm =  data['city'].loc[index_recomm].values
    result = {'Countries':trip_recomm,'Index':index_recomm}
    if print_recommendation==True:
      k=1
      for trip in trip_recomm:
        genrs = data.loc[data['city']==str(trip)].index[0]
        k=k+1
    return result

  # Plot the recommendation
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
  plt.title('your preference')
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