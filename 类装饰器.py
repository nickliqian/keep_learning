'''
	@property的作用和用法。
	1. 可以当作属性来访问 s.score
	2. 可以设定 @score.setter，从而使用 's.score = 60' == 's.set_score(60)' 设定属性并检查值。
'''

from newclass import func
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

s = Student()
s.score = 60 # OK，实际转化为s.set_score(60)
s.score = 90
print(s.score) # OK，实际转化为s.get_score()


'''
	admin.site.urls

	@property
    def urls(self):
        return self.get_urls(), 'admin', self.name

    def include(arg, namespace=None, app_name=None):

'''