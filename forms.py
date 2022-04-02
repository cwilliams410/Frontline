from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, Regexp
from wtforms.widgets import TextArea
from wtforms.fields import EmailField



class UserRegistrationForm(FlaskForm):
	UserName = StringField('UserName', validators=[DataRequired()])
	Email = EmailField('Email Address', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
	FirstName = StringField('FirstName', validators=[DataRequired()])
	LastName = StringField('LastName', validators=[DataRequired()])
	PhoneNumber = StringField('PhoneNumber', validators=[DataRequired(), Length(min=10, max=16)])
	submit = SubmitField(' ')



class UserCreationForm(FlaskForm):
	UserName = StringField('UserName', validators=[DataRequired()])
	Email = EmailField('Email Address', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
	FirstName = StringField('FirstName', validators=[DataRequired()])
	LastName = StringField('LastName', validators=[DataRequired()])
	PhoneNumber = StringField('PhoneNumber', validators=[DataRequired(), Length(min=10, max=16)])
	UserRole = SelectField('Select A User Role', choices=[])
	submit = SubmitField(' ')


class LoginForm(FlaskForm):
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField(' ')

class AddDogForm(FlaskForm):
	DogName = StringField('Dog Name', validators=[DataRequired(), Email()])
	DogAgeYears = StringField('Dog Age Years', validators=[DataRequired()])
	DogAgeMonths = StringField('Dog Age Months', validators=[DataRequired()])
	DogSex = SelectField('Dog Sex', choices=[('', 'Select an Option'),('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
	SurrenderReason = StringField('Surrender Reason', validators=[DataRequired()])
	DogDescription = StringField('Dog Description', validators=[DataRequired()])
	MicrochipID = StringField('MicrochipID')	
	IsFixed = SelectField('Dog Altered Status (Fixed)', choices=[('', 'Select an Option'),('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
	SurrenderAnimalControl = SelectField('Surrendered By Animal Control?', choices=[('', 'Select an Option'),('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
	DogBreed = SelectField('Select Applicable Dog Breed(s)', choices=[])
	submit = SubmitField(' ')


class EditDogForm(FlaskForm):
	MicrochipID = StringField('MicrochipID')	
	IsFixed = SelectField('Dog Altered Status (Fixed)', choices=[('', 'Select an Option'),('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
	DogSex = SelectField('Dog Breed', choices=[('', 'Select an Option'),('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
	DogBreed = SelectField('Select Applicable Dog Breed(s)', validators=[DataRequired()], choices=[])
	submit = SubmitField('Complete Edit')


class EditUserForm(FlaskForm):
	MicrochipID = StringField('MicrochipID')
	IsFixed = SelectField('Dog Altered Status (Fixed)', choices=[('', 'Select an Option'),('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
	DogSex = SelectField('Dog Breed', choices=[('', 'Select an Option'),('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
	DogBreed = SelectField('Select Applicable Dog Breed(s)', validators=[DataRequired()], choices=[])
	submit = SubmitField('Complete Edit')



class AddExpenseForm(FlaskForm):
	ExpenseDescription = StringField('Enter an Expense Description', widget=TextArea())
	ExpenseAmount = StringField('Enter an Expense Amount $:', validators=[DataRequired()])
	VendorName = SelectField('Select A Vendor', validators=[DataRequired()], choices=[])
	submit = SubmitField(' ')


class AddUserForm(FlaskForm):
	Username = StringField('Enter an Expense Description', widget=TextArea())
	Email = StringField('Enter an Expense Amount $:', validators=[DataRequired()])
	Password = SelectField('Select A Vendor', validators=[DataRequired()], choices=[])
	submit = SubmitField(' ')
	

class AdoptionApplicationForm(FlaskForm):
	AdopterEmail = StringField('Enter Adopter\'s Email Address: ', validators=[DataRequired()])
	AdopterFName= StringField('Enter Adopter\'s First Name:', validators=[DataRequired()])
	AdopterLName = StringField('Enter Adopter\'s Last Name', validators=[DataRequired()])
	AdPhoneNumber = StringField('Enter Adopter\'s Phone Number', validators=[DataRequired()])
	Street = StringField('Street Address:', validators=[DataRequired()])
	City = StringField('City', validators=[DataRequired()])
	State = StringField('State', validators=[DataRequired()])
	Zip = StringField('ZipCode:', validators=[DataRequired()])
	Co_Fname = StringField('Co Applicant First Name', validators=[DataRequired()])
	Co_Lname = StringField('Co Applicant Last Name', validators=[DataRequired()])
	submit = SubmitField('Add Application ')

class appreviewform2 (FlaskForm):
    appreview = SelectField('Review App', choices = [('','Select an Option'),('Accept','Accept'),('Reject','Reject')], validators=[DataRequired()])
    submit = SubmitField('Complete Review')

class addadoptionForm(FlaskForm):
	AdopterLname = StringField('Applicant Last Name:')
	co_lname = StringField('CoApplicant Last Name:')
	submit = SubmitField('Find Applicant')
