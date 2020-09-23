from django.db import models

class temp1(models.Model):
    #1 id 自增长 int
    id = models.AutoField(primary_key=True)
    #2 位置
    position = models.FloatField(default=0,null=False)
    #3 温度
    temperature = models.FloatField(default=0,null=False)
    #4 时间
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #<Book:(name,author,price)>
        return "<temp1:({id},{position},{temperature},{date_added})>".format(id=self.id,position=self.position,
                                                       temperature=self.temperature,date_added=self.date_added)

class temp2(models.Model):
    #1 id 自增长 int
    id = models.AutoField(primary_key=True)
    #2 位置
    position = models.FloatField(default=0,null=False)
    #3 温度
    temperature = models.FloatField(default=0,null=False)
    #4 时间
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #<Book:(name,author,price)>
        return "<temp2:({id},{position},{temperature},{date_added})>".format(id=self.id,position=self.position,
                                                       temperature=self.temperature,date_added=self.date_added)