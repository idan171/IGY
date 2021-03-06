from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'), primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    tel = db.Column(db.Text)
    permission = db.Column(db.Text)
    password_hash = db.Column(db.String(128))

    def __init__(self,id, email, username,firstname, lastname,tel,permission,password):
        self.id = id
        self.email = email
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.tel = tel
        self.permission = permission
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)
        
volunteers = db.relationship('volunteers',backref='users',lazy='dynamic')


class VolunteerDocuments(db.Model):
    IDD = db.Column(db.Integer,primary_key = True)

    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    Dname = db.Column(db.Text)
    DocDescription = db.Column(db.String(500))
    Document = db.Column(db.LargeBinary)
    DateAdded = db.Column(db.Text)

    def __init__(self,IDV,Dname,DocDescription,image,DateAdded):
       
        self.IDV = IDV
        self.Dname = Dname
        self.DocDescription = DocDescription
        self.image = image
        self.DateAdded = DateAdded

    def __repr__(self):
        return f"Document Name: {self.Dname}, Description: {self.DocDescription} "


class VolunteersInPoss(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    IDP = db.Column(db.Integer,db.ForeignKey('poss.IDP'))
    TimeS = db.Column(db.Text)
    Statusvp = db.Column(db.Text)
    #TimeF = db.Column(db.Text)

    def __init__(self,IDV,IDP,TimeS,Statusvp):
        self.IDV = IDV
        self.IDP = IDP
        self.TimeS = TimeS
        #self.TimeF = TimeF
        self.Statusvp = Statusvp

    def __repr__(self):
        return f"ID Volunteer: {self.IDV} , ID Poss: {self.IDP}"   

class MFile(db.Model):
    __tablename__ = 'mfile'

    IDF = db.Column(db.Integer,primary_key= True)
    IDM = db.Column(db.Integer,db.ForeignKey('meetings.IDM'))
    Filename = db.Column(db.Text)
    FileDescription = db.Column(db.Text)
    TheFile = db.Column(db.LargeBinary, nullable=True)
    AddTime = db.Column(db.Text)

    def __init__(self,IDM,FileName,FileDescription,image,AddTime):
        self.IDM = IDM
        self.FileName = FileName
        self.FileDescription = FileDescription
        self.image = image
        self.AddTime = AddTime

    def __repr__(self):
        return f"and ID of Meetings: {self.IDM}.."    


class Volunteers(db.Model):

    IDV = db.Column(db.Integer,primary_key= True, nullable=False,unique=True)
    emailv = db.Column(db.Text)
    FnameV = db.Column(db.Text)
    SnameV = db.Column(db.Text)
    DateOfBirthV = db.Column(db.Text)
    PronounsV = db.Column(db.Text)
    CityV = db.Column(db.Text)
    AdressV = db.Column(db.Text)
    NutritionV = db.Column(db.Text)
    PhoneNumV = db.Column(db.String(10))
    StatusV = db.Column(db.Text)
    DateAdded = db.Column(db.Text)
    
    Message = db.relationship('Message',backref='volunteers',lazy='dynamic')
    volunteersingroups = db.relationship('VolunteersInGroups',backref='volunteers',lazy='dynamic')
    volunteerDocuments = db.relationship('VolunteerDocuments',backref='volunteers',lazy='dynamic')
    volunteersinPoss = db.relationship('VolunteersInPoss',backref='volunteers',lazy='dynamic')


    def __init__(self,IDV,emailv,FnameV,SnameV,DateOfBirthV,PronounsV,CityV,AdressV,NutritionV,PhoneNumV,StatusV,DateAdded ):
        self.IDV = IDV
        self.emailv=emailv
        self.FnameV = FnameV
        self.SnameV = SnameV
        self.DateOfBirthV = DateOfBirthV
        self.PronounsV = PronounsV
        self.CityV = CityV
        self.AdressV = AdressV
        self.NutritionV = NutritionV
        self.PhoneNumV = PhoneNumV
        self.StatusV = StatusV
        self.DateAdded = DateAdded

    def __repr__(self):
        return f"Volunteer Name: {self.FnameV} {self.SnameV} Volunteer ID: {self.IDV} "

class Poss(db.Model):
    IDP = db.Column(db.Integer,primary_key= True)
    PossName = db.Column(db.Text)
    PossDescription = db.Column(db.Text)
    AddTime = db.Column(db.Text)

    volunteersinPoss = db.relationship('VolunteersInPoss',backref='poss',lazy='dynamic')

    def __init__(self,PossName,PossDescription,AddTime):
        #self.IDP = IDP
        self.PossName = PossName
        self.PossDescription = PossDescription
        self.AddTime = AddTime

    def __repr__(self):
        return f"Poss Name: {self.PossName}, ID Poss: {self.IDP}."



class Student(db.Model):

    __tablename__ = 'students'
    emails = db.Column(db.String(64),primary_key = True, nullable=False)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    dateofbirth = db.Column(db.Text)
    pronouns = db.Column(db.Text)
    citys = db.Column(db.Text)
    addresss = db.Column(db.Text)
    nutritions = db.Column(db.Text)
    phonenums = db.Column(db.String(10))
    schoolname = db.Column(db.Text)
    dateaddeds = db.Column(db.Text)
    statuss = db.Column(db.Text)
    parents = db.Column(db.Text)
    details = db.Column(db.String(500))

    studentsingroups = db.relationship('StudentInGroup',backref='student',lazy=False)
    Studentsinmeeting = db.relationship('StudentsInMeeting',backref='student',lazy=False)

    def __init__(self,emails,firstname,lastname,dateofbirth,pronouns,citys,addresss,nutritions,phonenums,schoolname,dateaddeds,statuss,parents,details):
        self.emails = emails
        self.firstname = firstname
        self.lastname = lastname
        self.dateofbirth = dateofbirth
        self.pronouns = pronouns
        self.citys = citys
        self.addresss = addresss
        self.nutritions = nutritions
        self.phonenums = phonenums
        self.schoolname = schoolname
        self.dateaddeds = dateaddeds
        self.statuss = statuss
        self.parents = parents
        self.details = details


 #  def __repr__(self):
  #      if self.studentingroup:
   #         return f"Student full  name is{self.emails},{self.firstname},{self.lastname}, {self.dateofbirth},{self.pronouns},{self.citys},{self.addresss},{self.nutritions},{self.phonenums},{self.schoolname}and group is {self.studentingroup.student_emails}"
    #    else:
     #       return f"Student full  name is{self.emails},{self.firstname},{self.lastname}, {self.dateofbirth},{self.pronouns},{self.citys},{self.addresss},{self.nutritions},{self.phonenums},{self.schoolname}and has no group assigned yet."

class Group(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.Text)
    regionorsubject = db.Column(db.Text)
    city = db.Column(db.Text)
    agesingroup = db.Column(db.String(500))

    condidates = db.relationship('Condidate',backref='condidate',lazy=False)
    volunteersinGroups = db.relationship('VolunteersInGroups',backref='group',lazy='dynamic')
    Meetings = db.relationship('Meetings',backref='group',lazy='dynamic')

    def __init__(self,name,regionorsubject,city,agesingroup):
        self.name = name
        self.regionorsubject = regionorsubject
        self.city = city
        self.agesingroup=agesingroup

    def __repr__(self):
        return f"Group Name: {self.name} Group ID: {self.id}"


class VolunteersInGroups(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    #IDV = db.relationship('Volunteers',backref='VolunteersInGroups',uselist=False)
    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    #IDG = db.relationship('Group',backref='VolunteersInGroups',uselist=False)
    IDG = db.Column(db.Integer,db.ForeignKey('groups.id'))
    TimeS = db.Column(db.Text)
    TimeF = db.Column(db.Text)
    statusV = db.Column(db.Text)

    def __init__(self,IDV,IDG,TimeS,TimeF,statusV):
        self.IDV = IDV
        self.IDG = IDG
        self.TimeS = TimeS
        self.TimeF = TimeF
        self.statusV = statusV



class Condidate(db.Model):

    __tablename__ = 'condidates'

    id = db.Column(db.Integer,primary_key= True)
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))
    emailc = db.Column(db.String(64), unique=True, index=True)
    pronounc = db.Column(db.Text)
    phonenumc = db.Column(db.String(10))
    stimes = db.Column(db.Text)
    text = db.Column(db.Text)
    status = db.Column(db.Text)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)


    def __init__(self,group_id,emailc,pronounc,phonenumc,stimes,text,status,firstname,lastname):
        self.group_id = group_id
        self.emailc = emailc
        self.pronounc = pronounc
        self.phonenumc = phonenumc
        self.stimes = stimes
        self.text = text
        self.status = status
        self.firstname =firstname
        self.lastname = lastname
        
class StudentInGroup(db.Model):

    __tablename__ = 'studentsingroups'

    id = db.Column(db.Integer,primary_key= True)
    student_emails = db.Column(db.String(64),db.ForeignKey('students.emails'))
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))
    stimes = db.Column(db.Text)
    ftimef = db.Column(db.Text)
    statusg = db.Column(db.Text)


    def __init__(self,stimes,ftimef,student_emails,group_id,statusg):
        self.stimes = stimes
        self.ftimef = ftimef
        self.student_emails = student_emails
        self.group_id = group_id
        self.statusg = statusg

class Meetings(db.Model):
    IDM = db.Column(db.Integer,primary_key= True)
    Mdate = db.Column(db.Text)
    Mtime = db.Column(db.Text)
    IDG = db.Column(db.Integer,db.ForeignKey('groups.id'))
    Occurence = db.Column(db.Text) 
    Platform = db.Column(db.Text)
    title = db.Column(db.Text)
    Rate = db.Column(db.Integer)
    Pros = db.Column(db.String(500))
    Cons = db.Column(db.String(500))
    attending = db.Column(db.String(500))
    DateAdded = db.Column(db.Text)

    studentsinMeeting = db.relationship('StudentsInMeeting',backref='meetings',lazy='dynamic')

    def __init__(self,Mdate,Mtime,IDG,Occurence,Platform,title,Rate,Pros,Cons,attending,DateAdded):
        self.Mdate = Mdate
        self.Mtime = Mtime
        self.IDG = IDG
        self.Occurence= Occurence
        self.Platform = Platform
        self.title = title
        self.Rate = Rate
        self.Pros = Pros
        self.Cons = Cons
        self.attending = attending
        self.DateAdded = DateAdded

class StudentsInMeeting(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    IDM = db.Column(db.Integer,db.ForeignKey('meetings.IDM'))
    EmailS = db.Column(db.String(64),db.ForeignKey('students.emails'))
    Attendance = db.Column(db.Text)

    def __init__(self,IDM,EmailS,Attendance):
        self.IDM = IDM
        self.EmailS = EmailS
        self.Attendance = Attendance

    def __repr__(self):
        return f"Student Email: {self.EmailS}, ID of Meeting: {self.IDM}. "   
        
class Message(db.Model):
    IDM = db.Column(db.Integer,primary_key=True)
    IDV = db.Column(db.Integer,db.ForeignKey('volunteers.IDV'))
    Mdate = db.Column(db.Text)
    Content = db.Column(db.Text)

    def _init_(self,IDV,Mdate,Content):
        #self.IDM = IDM       
        self.IDV = IDV
        self.Mdate = Mdate
        self.Content = Content
        
    def _repr_(self):
        return f"{Mdate} {Content}"
         
#user_test1 = User(id='d')
#db.session.add(user_test1)

db.create_all()
db.session.commit()