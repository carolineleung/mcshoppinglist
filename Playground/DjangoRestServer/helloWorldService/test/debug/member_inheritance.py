
class Fruit(object):
    def __init__(self, message=''):
        object.__init__(self)
        self.message = message

    message_prop = property(lambda self: self.message, None, None, None)

class TreeFruit(Fruit):
    def __init__(self, message=''):
        Fruit.__init__(self, message)

class Apple(TreeFruit):
    def __init__(self, message=''):
        TreeFruit.__init__(self, message)

    def get_message(self):
#        return self.message
        return self.message_prop

def main():
    a = Apple('apple')
    b = TreeFruit('treefruit')
    print('apple:' + a.get_message())
    print('apple:' + a.message)
    print('treefruit:' + b.message)

if __name__ == "__main__":
    main()
