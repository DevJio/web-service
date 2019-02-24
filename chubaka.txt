docker exec -it flask-hello_flask_1 bash
docker exec -it flask-hello_flask_1 python train_model.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,4"}' \
  http://localhost:5000/iris_post


Вы от нас будете ждать: 
json{ «id»: [id], «text»: [text]}
Где id – id абзацев
Text   – текстовки абзацев
 
В ответ будем получать:
json{ «id»: [id], «class»: [class]}
Где id – id абзацев
class  – классификация по абзацам