from main import index, cow

def test_index(): 
    assert index() == 'Hello, world!'
    
def test_cow():
    assert cow() == 'MOoooOo!'