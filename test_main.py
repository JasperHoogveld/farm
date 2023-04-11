from main import index, cow

def test_index(): 
    assert index() == 'Hello, world 6!'
    
def test_cow():
    assert cow() == 'MOoooOo!'