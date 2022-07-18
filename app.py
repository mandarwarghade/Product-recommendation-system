from flask import Flask,render_template,request
import pickle
import numpy as np

#popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def recommend_ui():
    return render_template('index.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    if request.method == "POST":
        id_input = request.form.get('id_input')
        date_input = request.form.get('date_input')
        print(id_input,date_input)
        
        index = np.where(pt.index==(float(id_input),str(date_input)))[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:12]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = df.loc[(df['CustomerID'] == pt.index[i[0]][0])&(df['Dates']==pt.index[i[0]][1]),'Description'].iloc[0]
            
            #item.extend(list(temp_df.drop_duplicates('Description')['Description'].values))       
            
            data.append(temp_df)
        
        print(list(set(data)))
     
        return render_template('index.html',data=list(set(data))[0:4])

     
if __name__ == '__main__':
    app.run(debug=True)