from main import index, cow

def test_index(): 
    assert index() == 'Hello, world 7!' 
    
def test_cow():
    assert cow() == 'MOoooOo!'