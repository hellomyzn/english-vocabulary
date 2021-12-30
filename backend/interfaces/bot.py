from views import console

class Bot(object):
    """Base model for Robot."""

    def __init__(self, speak_color='green'):
        self.speak_color = speak_color

    def hello(self):
        """Returns words to the user that the robot speaks at the beginning."""
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            print(template.substitute())
            break
