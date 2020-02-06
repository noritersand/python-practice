a = 'global'
def fn():
    print(a)
    a = 'assigned by local scope' # UnboundLocalError: local variable 'a' referenced before assignment
    print(a)
fn()
