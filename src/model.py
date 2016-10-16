# -*- coding: utf-8 -*-
import datetime
from conf import DBSTR, DBARGS
from sqlalchemy import Column, String, Sequence, Integer, DateTime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class VideoInfo(Base):
    # 表的名字:
    __tablename__ = 'video_info'

    # 表的结构:
    id = Column(Integer, Sequence('video_info_id_seq'), primary_key=True)
    v_id = Column(String(20))
    v_type = Column(String(20))
    video_size = Column(String(20))
    video_ext = Column(String(20))
    sina_video_id = Column(String(200))
    sina_video_url = Column(String(200))
    create_time = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<VideoInfo(v_id='%s', v_type='%s', id='%s', create_time='%s')>" % (
            self.v_id, self.v_type, self.id, self.create_time)


engine = sqlalchemy.create_engine(DBSTR, **DBARGS)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    session = DBSession()
    video = VideoInfo(v_type='hah', v_id='11')
    session.add(video)
    session.commit()
    session.close()
    # session = DBSession()
    # video_infos = session.query(VideoInfo).all()
    # print(video_infos)