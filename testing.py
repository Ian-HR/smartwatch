import ujson

btData = ['to-do', '{"id":"f3fd81e0-bcd7-416d-b987-963454c42f60","madeby":null,"todomade":"2021-05-31T11:20:16.351522+02:00","name":"Test","time":"12:00:00","repeat":"Dagelijks","isComplete":false}', '{"id":"0216e67e-179b-418a-8b5a-42535e190604","madeby":"3","todomade":"2021-06-01T16:38:51.491601+02:00","name":"Activiteit","time":"11:00:00","repeat":"Dagelijks","isComplete":true}', '{"id":"2fd91376-acf1-4dcd-918d-84dd31ca3ff7","madeby":"6","todomade":"2021-06-01T17:55:54.922532+02:00","name":"sportschool","time":"12:00:00","repeat":"Dagelijks","isComplete":true}']

for i in range(1, len(btData)):
    btData[i] = ujson.loads(btData[i])

print(btData)

newDict = {}
for i in range(1, len(btData)):
    print(i)
    newDict[btData[i]["name"]] = "x" if btData[i]["isComplete"] else " "
    print(newDict)

print(newDict)
