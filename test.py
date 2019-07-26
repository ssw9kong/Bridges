mylist = [1,2,3,4,5]

def function1(list):
    x = ['table', 'chair']
    list.clear()
    list.extend(x)
    
function1(mylist)

print(mylist)