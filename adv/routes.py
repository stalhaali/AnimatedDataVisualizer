from flask import render_template, url_for, flash, redirect, request, abort
from adv import app, db, bcrypt, mail
from adv.forms import RegistrationForm, LoginForm, CreateGraphBarForm, CreateGraphNonBarForm, DeleteGraphForm, VideoForm, ContactForm
from adv.models import User, Post, Video
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from adv.Data_Visualizer import create_bar
import base64
from PIL import Image
from io import StringIO, BytesIO
import numpy as np
import cv2


#from adv.data_viz_2 import create_bar1
class DataStore():
    video =  "<h1>No Video Created Yet!</h1>"#' <video width="320" height="240" controls> <source src="movi1e.mp4" type="video/mp4"> <source src="black.ogg" type="video/ogg"> Your browser does not support the video tag. </video>'


data = DataStore()

@app.route("/")
@app.route("/home")
def home():
    return render_template("layout.html", title="home")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'danger')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You may login now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'danger')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    videos = Video.query.filter_by(author = current_user).all()
    return render_template('profile.html', title='Profile', videos=videos, number = len(videos))

@app.route("/choose")
@login_required
def choose():
    return render_template('choose.html', title='choose')

@app.route("/create/<graph_type>", methods=['GET', 'POST'])
@login_required
def create(graph_type):
    all_types = ['bar', 'line', 'scatter', 'pie']
    if graph_type not in all_types:
        abort(403)
    if graph_type == 'bar':
        form = CreateGraphBarForm()
    else:
        form = CreateGraphNonBarForm()
    if form.validate_on_submit():
        file = form.spreadsheet.data
        title = form.title.data
        if graph_type == 'bar':
            if form.sort.data == 'Highest':
                sort_by = 'asc'
            else:
                sort_by = 'desc'
            bars = form.bars_visible.data
            if form.orientation.data == 'Horizontal':
                orien = 'h'
            else:
                orien = 'v'
            #data.video = create_bar1(file, graph_type, title, sort_by, bars, orien)
        else:
            #data.video = create_bar1(file, graph_type, title)
            """do this"""
        data.video = create_bar(file)
        if not isinstance(data.video, str):
            data.video = data.video.data
        #data.video = create_bar(file, graph_type, 'hi')
        current_user.graphs_created += 1
        db.session.commit()
        flash(f'Your video has been created!', 'success')
        return redirect(url_for('video'))
    
    return render_template('creategraph.html', title='create', form = form, header=graph_type)

@app.route("/video", methods=['GET', 'POST'])
@login_required
def video():
    form = VideoForm()
    if form.validate_on_submit():
        if len(data.video) == 30:
            flash(f'There is no video to save!', 'danger')
        else:
            if len(Video.query.filter_by(htmlcode=data.video).all()) > 0:
                flash(f'You have already saved this video!', 'danger')
            else:
                video = Video(author = current_user, htmlcode = data.video)
                db.session.add(video)
                db.session.commit()
                flash(f'Your video has been saved!', 'success')
        

    return render_template('video.html', title='video', form = form, header = data.video)

@app.route("/delete/<int:vid_id>", methods=['GET', 'POST'])
def delete(vid_id):
    form = DeleteGraphForm()
    video = Video.query.get_or_404(vid_id)
    if video.author != current_user:
        abort(403)
    if form.validate_on_submit():
        db.session.delete(video)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('delete.html', title='delete', form = form, video=video.htmlcode)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Fan Mail From ' + form.name.data
            , sender = 'datavizassistance@gmail.com', recipients = ['datavizassistance@gmail.com'])
        msg.body = form.content.data + " From Email " + form.email.data
        mail.send(msg)
        flash('Message has been sent', 'success')
    return render_template('contact.html', title='Contact', form=form)


@app.route("/features", methods=['GET', 'POST'])
def features():
    if request.method == "POST":
        data_url = request.form["nm"]
        """
        response = urllib.request.urlopen(data_url)
        with open('image.jpg', 'wb') as f:
            f.write(response.file.read())
            img = cv2.imread('image.jpg')
            cv2.imshow('bob', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        """
        offset = data_url.index(',')+1
        img_bytes = base64.b64decode(data_url[offset:])
        img = Image.open(BytesIO(img_bytes))
        img  = np.array(img)
        differentiate(img)
        #cv2.imshow('bob', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        flash('Message has been sent', 'success')
        return render_template('features.html', title='features')
    else:
        return render_template('features.html', title='features')


def differentiate(img):
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayscaled, (7,7), 1)
    #canny = cv2.Canny(blur, 50, 50)
    thresh = cv2.threshold(blur, 110 ,255, cv2.THRESH_BINARY_INV)[1]
    img1 = img.copy()
    all_pics = []

    contours, Hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    for cnt in contours:
            i += 1
            #cv2.drawContours(img1, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            bob = thresh [y:y+h, x:x+w]
            all_pics.append((x, bob))
            cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            new_img = cv2.resize(bob, (28, 28))
            #cv2.imwrite("fruit" +str(i)+".jpg", new_img)

    cv2.imshow("title", img1)
    cv2.imshow("title2", thresh)
    cv2.waitKey(0)