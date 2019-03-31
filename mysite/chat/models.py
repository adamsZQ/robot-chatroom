from django.db import models


class Robot(models.Model):
    name = models.CharField(max_length=32, default='robot')
    ip = models.GenericIPAddressField(default='127.0.0.1')
    port = models.IntegerField(default='9999')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=32, default='group')
    rcount = models.IntegerField(default='3')
    robots = models.ManyToManyField(Robot, through='chat.RobotGroup')

    def __str__(self):
        return self.name


class RobotGroup(models.Model):
    robot = models.ForeignKey('Robot', on_delete=models.CASCADE, default='', null=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, default='', null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return "[%s]<%s>" % (self.group.name, self.robot.name)
