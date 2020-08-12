from app import db
from datetime import datetime
from app.comm import utils

class History(db.Model):
    __tablename__ ='history'

    id = db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False,comment="id")
    timestamp = db.Column(db.String(20),nullable=False,default='',comment='时间戳')
    status = db.Column(db.String(10),nullable=False,default='',comment='状态')
    machine_id = db.Column(db.String(10),nullable=False,default='',comment='机器编号')
    create_at = db.Column(db.DateTime,default=datetime.now,nullable=False,comment='时间')
    result = db.Column(db.Integer,nullable=False,default=0,comment='结果')
    imgs = db.relationship('Imgs', backref='stu', lazy=True)


    def __init__(self,timestamp,status,machine_id,create_at,result):
        self.timestamp = timestamp
        self.status = status
        self.machine_id = machine_id
        self.create_at = create_at
        self.result = result

    def to_dict(self):
        imgs=[]
        if self.imgs:
            imgs =[x.img for x in self.imgs]
        return {
            "id":self.id,
            "timestamp": self.timestamp,
            "create_at": self.create_at.__str__(),
            "status": self.status,
            "machine_id": self.machine_id,
            "result": self.result,
            "imgs": imgs
        }
    @classmethod
    def add(cls, data):
        db.session.add(data)
        return cls

    @classmethod
    def flush(cls):
        db.session.flush()
        return cls

    @classmethod
    def update(cls):
        return cls.session_commit()

    @classmethod
    def session_commit(cls):
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @classmethod
    def add_all(cls, list_data):
        db.session.add_all(list_data)

    @classmethod
    def get_mes(cls,form):
        if form.data["date"] == None :
            if form.data["type"] =='all':
                query = cls.query.filter(cls.machine_id.like("%"+form.data["input"]+"%")).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
            elif form.data["type"] == 'good':
                query = cls.query.filter(cls.result == 0,cls.machine_id.like("%"+form.data["input"]+"%")).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
            else:
                query = cls.query.filter(cls.result != 0,cls.machine_id.like("%"+form.data["input"]+"%")).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
        else:
            time =form.date.data[:10]
            if form.data["type"] =='all':
                query = cls.query.filter(cls.create_at.contains(time),cls.machine_id.like("%"+form.data["input"]+"%")).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
            elif form.data["type"] == 'good':
                query = cls.query.filter(cls.result == 0,cls.machine_id.like("%"+form.data["input"]+"%"),cls.create_at.contains(time)).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
            else:
                query = cls.query.filter(cls.result != 0,cls.machine_id.like("%"+form.data["input"]+"%"),cls.create_at.contains(time)).order_by(cls.create_at.desc()).paginate(form.page_index.data, form.page_size.data, None)
        return query


    @classmethod
    def get_today(cls,today):
        query = cls.query.filter(cls.create_at.contains(today)).all()
        all =len(query)
        good = len(list(filter(lambda x:x.result == 0,query)))
        result ={
            "all":all,
            "good":good,
            "bad":all-good
        }
        return result


    @classmethod
    def get_chat(cls,date_list):
        data = []
        data1 =[]
        for i in date_list:
            data.append(len(cls.query.filter(cls.create_at.contains(i),cls.result == 0).all()))
            data1.append(len(cls.query.filter(cls.create_at.contains(i),cls.result != 0).all()))
        good =sum(data)
        bad =sum(data1)
        series1 =[
            {"value": good, "name": '合格'},
            {"value": bad, "name": '杂质'}
        ]
        series=[
            {
                "name": '合格',
                "data": data,
                "type": 'line'
            },
            {
                "name": '杂质',
                "data": data1,
                "type": 'line'
            }
        ]
        series2=[good+bad,good,bad]
        return series,series1,series2

    @classmethod
    def get_chat1(cls,today):
        data=[]
        data1=[]
        query = cls.query.filter(cls.create_at.contains(today)).all()
        for i in range(24):
            data.append(len(list(filter(lambda x:(x.result == 0 and x.create_at.hour == i),query))))
            data1.append(len(list(filter(lambda x:(x.result != 0 and x.create_at.hour == i),query))))
        good =sum(data)
        bad =sum(data1)
        series1 =[
            {"value": good, "name": '合格'},
            {"value": bad, "name": '杂质'}
        ]
        series=[
            {
                "name": '合格',
                "data": data,
                "type": 'line'
            },
            {
                "name": '杂质',
                "data": data1,
                "type": 'line'
            }
        ]
        series2=[good+bad,good,bad]
        return series,series1,series2